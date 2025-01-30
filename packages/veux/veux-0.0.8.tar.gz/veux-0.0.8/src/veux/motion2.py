import numpy as np
import pygltflib
from scipy.spatial.transform import Rotation
from pygltflib import FLOAT
from veux.config import MeshStyle, LineStyle
from veux.canvas.gltf import GLTF_T
from collections import defaultdict

from shps.frame.extrude import Extrusion

def skin_frames(model, canvas, config=None):
    """
    Builds a single skinned mesh for all frame elements in the reference (undeformed) configuration.
    Returns a dictionary mapping (element_name, j) -> glTF node index,
    so you can update those node transforms later.

    It's almost the same as your original code, but the ring-building loops & earcut calls
    are extracted into the `Extrusion` class. We then just bind each ring's vertex range
    to one joint in the glTF skin, same as before.
    """
    gltf = canvas.gltf
    if not gltf.scenes:
        gltf.scenes = [pygltflib.Scene(nodes=[])]

    scene = gltf.scenes[0]
    EYE4 = np.eye(4, dtype=canvas.float_t)

    if config is None:
        config = {
            "style": MeshStyle(color="gray"),
            "scale": 1.0,
            "outline": "",
        }

    #------------------------------------------------------
    # 1) Build all geometry using the Extrusion class
    #------------------------------------------------------
    scale = config.get("scale", 1.0)
    extr = Extrusion(model, scale=scale, do_end_caps=True)

    # gather the results
    positions   = extr.vertices()   # Nx3
    texcoords   = None #extr.texcoords()  # Nx2
    indices     = extr.triangles()  # Mx3
    ring_ranges = extr.ring_ranges()# e.g. [((elem, j), start,end), ...]

    if len(positions)==0 or len(indices)==0:
        # No geometry => bail
        return {}

    # We'll accumulate JOINTS_0 and WEIGHTS_0 for all vertices
    num_vertices = len(positions)
    joints_0    = np.zeros((num_vertices,4), dtype=canvas.index_t)
    weights_0   = np.zeros((num_vertices,4), dtype=canvas.float_t)

    #------------------------------------------------------
    # 2) Create a skeleton root node
    #------------------------------------------------------
    skeleton_root_node = pygltflib.Node(name="FrameExtrusionSkeletonRoot", children=[])
    skeleton_root_idx = _append_index(gltf.nodes, skeleton_root_node)
    scene.nodes.append(skeleton_root_idx)

    # We'll store a list of joint node indices, and their inverseBindMatrices
    joint_nodes = skeleton_root_node.children
    inverse_bind_matrices = []
    skin_nodes = {}

    def _make_matrix(translation, rotmat):
        M = np.eye(4, dtype=canvas.float_t)
        M[:3,:3] = rotmat
        M[:3, 3] = translation
        return M

    #------------------------------------------------------
    # 3) For each ring, create a glTF Node (joint),
    #    and assign ring vertices to that joint
    #------------------------------------------------------
    for ((element_name, j), start_idx, end_idx) in ring_ranges:
        el = model["assembly"][element_name]
        # get reference position from el["crd"][j]
        pos_ref = np.array(el["crd"][j], dtype=canvas.float_t)

        # orientation from model.frame_orientation(...).T
        # (If your code uses the same orientation for all rings, that’s fine.)
        rot_mat = model.frame_orientation(element_name).T
        qx, qy, qz, qw = Rotation.from_matrix(rot_mat).as_quat()

        # create the node
        node = pygltflib.Node()
        node.translation = pos_ref.tolist()
        node.rotation    = [qx, qy, qz, qw]

        this_node_idx = _append_index(gltf.nodes, node)
        # add to skeleton root
        joint = _append_index(joint_nodes, this_node_idx)

        # store in the returned dict
        skin_nodes[(element_name, j)] = this_node_idx

        # compute inverse bind matrix
        M_bind = _make_matrix(pos_ref, rot_mat)
        M_bind_inv = np.linalg.inv(M_bind)
        inverse_bind_matrices.append(M_bind_inv)

        # Mark all vertices in [start_idx : end_idx] as belonging 100% to this joint
        joints_0[start_idx:end_idx, 0]  = joint
        weights_0[start_idx:end_idx, 0] = 1.0

    #------------------------------------------------------
    # 4) Create the Skin referencing these joints
    #------------------------------------------------------
    skin = _create_skin(canvas, inverse_bind_matrices, joint_nodes, skeleton_root_idx)

    #------------------------------------------------------
    # 5) build the Mesh
    #------------------------------------------------------
    _create_mesh(canvas,
                 positions,
                 texcoords,
                 joints_0,
                 weights_0,
                 indices,
                 skin_idx=skin,
                 material=canvas._get_material(config["style"])
    )

    return skin_nodes


def _append_index(container, item):
    """Helper: appends item to container, returns the new index."""
    container.append(item)
    return len(container) - 1


def _create_skin(canvas, inverse_bind_matrices, joint_nodes, skeleton_root_idx):
    """
    Create a glTF Skin object, references the given joint_nodes, 
    uploads inverseBindMatrices, returns the skin index.
    (This matches logic in your original code.)
    """
    import pygltflib
    gltf = canvas.gltf

    # Convert inverse_bind_matrices to float32 Nx4x4
    ibm_np = np.array(inverse_bind_matrices, dtype=canvas.float_t).reshape(-1,4,4)

    # Make a buffer + accessor for them
    ibm_bytes = ibm_np.tobytes()
    ibm_buffer_view_idx = canvas._push_data(ibm_bytes, target=None)  # user-defined method
    ibm_accessor_idx = _append_index(gltf.accessors, pygltflib.Accessor(
        bufferView=ibm_buffer_view_idx,
        componentType=GLTF_T[canvas.float_t],  # e.g. pygltflib.FLOAT
        count=len(ibm_np),
        type="MAT4"
    ))

    # Build the Skin object
    skin = pygltflib.Skin(
        inverseBindMatrices=ibm_accessor_idx,
        joints=joint_nodes,
        skeleton=skeleton_root_idx,
        name="FrameExtrusionSkin"
    )
    if not gltf.skins:
        gltf.skins = []
    return _append_index(gltf.skins, skin)


def _create_skin(canvas, ibms, joint_nodes, skeleton):
    "Create a Skin referencing given joints and add to skeleton"
    gltf = canvas.gltf

    # Flatten the inverse bind matrices into an Nx16 float32 array
    ibm_array = np.array(ibms, dtype=canvas.float_t).reshape(-1,16)

    # Create accessor to inverse bind matrices and skin
    skin = pygltflib.Skin(
        inverseBindMatrices=_append_index(gltf.accessors, pygltflib.Accessor(
            bufferView=canvas._push_data(ibm_array.tobytes(), target=None),
            componentType=GLTF_T[canvas.float_t],
            count=len(ibms),
            type="MAT4"
        )),
        joints=joint_nodes,
        skeleton=skeleton,
        name="FrameExtrusionSkin"
    )

    if not gltf.skins:
        gltf.skins = []

    return _append_index(gltf.skins, skin)


def _create_mesh(canvas,
                  positions,
                  texcoords,
                  joints_0,
                  weights_0,
                  indices,
                  skin_idx=None,
                  material=None):
    
    gltf = canvas.gltf
    joints_0  = np.array(joints_0,  dtype=canvas.index_t)
    weights_0 = np.array(weights_0, dtype=canvas.float_t)
    indices   = np.array(indices,   dtype=canvas.index_t).reshape(-1)

    jnt_bytes = joints_0.tobytes()
    wts_bytes = weights_0.tobytes()

    # Accessors
    positions = np.array(positions, dtype=canvas.float_t)
    ver_accessor = _append_index(gltf.accessors, pygltflib.Accessor(
        bufferView=canvas._push_data(positions.tobytes(), pygltflib.ARRAY_BUFFER),
        componentType=GLTF_T[canvas.float_t],
        count=len(positions),
        type="VEC3",
        min=positions.min(axis=0).tolist(),
        max=positions.max(axis=0).tolist()
    ))

    if texcoords is not None:
        texcoords = np.array(texcoords, dtype=canvas.float_t)
        tex_accessor = _append_index(gltf.accessors, pygltflib.Accessor(
            bufferView=canvas._push_data(texcoords.tobytes(), pygltflib.ARRAY_BUFFER),
            componentType=GLTF_T[canvas.float_t],
            count=len(texcoords),
            type="VEC2"
        ))

    jnt_accessor = _append_index(gltf.accessors, pygltflib.Accessor(
        bufferView=canvas._push_data(jnt_bytes, pygltflib.ARRAY_BUFFER),
        componentType=GLTF_T[canvas.index_t],
        count=len(joints_0),
        type="VEC4"
    ))

    wts_accessor = _append_index(gltf.accessors, pygltflib.Accessor(
        bufferView=canvas._push_data(wts_bytes, pygltflib.ARRAY_BUFFER),
        componentType=GLTF_T[canvas.float_t],
        count=len(weights_0),
        type="VEC4"
    ))


    idx_accessor = _append_index(gltf.accessors, pygltflib.Accessor(
        bufferView=canvas._push_data(indices.tobytes(), pygltflib.ELEMENT_ARRAY_BUFFER),
        componentType=GLTF_T[canvas.index_t],
        count=len(indices),
        type="SCALAR",
        min=[int(indices.min())],
        max=[int(indices.max())]
    ))

    # Create the Mesh
    mesh = pygltflib.Mesh(
        primitives=[
            pygltflib.Primitive(
                attributes=pygltflib.Attributes(
                    POSITION=ver_accessor,
                    JOINTS_0=jnt_accessor,
                    WEIGHTS_0=wts_accessor
                ),
                material=material,
                indices=idx_accessor,
                mode=pygltflib.TRIANGLES
            )
        ],
        name="FrameSkinMesh"
    )

    if texcoords is not None:
        mesh.primitives[0].attributes.TEXCOORD_0 = tex_accessor

    mesh_idx = _append_index(gltf.meshes, mesh)

    #---------------------------------------------
    # 4) Create a Node referencing the mesh + skin
    #---------------------------------------------
    mesh_node_idx = _append_index(gltf.nodes, pygltflib.Node(
        mesh=mesh_idx,
        skin=skin_idx,
        name="FrameSkinMeshNode"
    ))

    # Put it in the scene
    if not gltf.scenes or len(gltf.scenes)==0:
        gltf.scenes = [pygltflib.Scene(nodes=[])]

    gltf.scenes[0].nodes.append(mesh_node_idx)



def deform_extrusion(model, canvas, state, skin_nodes, config=None):
    """
    Given a 'state' that contains the updated (displaced/rotated) coordinates for each element’s cross section,
    update the glTF nodes' translation/rotation accordingly.

    :param model:    The same structural model used in draw_extrusions_ref.
    :param gltf:     The glTF2 object that already has nodes, a skin, etc.
    :param state:    Some data structure that can provide displacements & rotations for each (element, cross section).
    :param skin_nodes: Dict returned by draw_extrusions_ref -> {(element_name, j): node_index, ...}
    :param config:   Optional dict for additional settings (e.g. scale, etc).


    The skinned mesh in glTF will automatically show the new shape
    as the viewer or engine processes the node transforms.
    """
    gltf = canvas.gltf 

    if config is None:
        config = {}

    for element_name, el in model["assembly"].items():

        # Number of cross sections
        nen = len(el["nodes"])

        # Displacements and rotations from 'state' for each cross-section
        pos_all = state.cell_array(el["name"], state.position)  # shape (nen, 3?)
        rot_all = state.cell_array(el["name"], state.rotation)  # shape (nen, 3x3) ?

        # Original coordinates
        X_ref = np.array(el["crd"])  # shape (nen, 3)

        for j in range(nen):
            # Look up the node index in glTF
            if (element_name, j) not in skin_nodes:
                continue
            node_idx = skin_nodes[(element_name, j)]

            # Deformed translation
            x_def = X_ref[j,:] + pos_all[j,:]
            gltf.nodes[node_idx].translation = x_def.tolist()

            # Deformed rotation
            R_def = rot_all[j]  # presumably a 3x3 array
            qx, qy, qz, qw = Rotation.from_matrix(R_def).as_quat()
            gltf.nodes[node_idx].rotation = [qx, qy, qz, qw]


class Motion:
    """
    A helper class that accumulates multiple "states" (deformed configurations)
    and creates a time-based glTF Animation. Each call to add_state() adds
    a new keyframe at the next time step.
    """

    def __init__(self, model=None, time_step=1.0, name="BeamDeformations"):
        """
        :param canvas:   An instance of your GltfCanvas (with .gltf).
        :param extrusion: Dict {(element_name, j): gltf_node_index, ...}
                         returned by draw_extrusions_ref().
        :param time_step: The time increment for each added state (seconds, or frames).
        :param name: The name of the final glTF animation.
        """
        self.model = model

        self.time_step = time_step
        self.current_time = 0.0
        self.anim_name = name

        # Store keyframes in a dictionary:
        #   self._keyframes[node_idx]["translation"] = [(t0, (x,y,z)), (t1, (x,y,z)), ...]
        #   self._keyframes[node_idx]["rotation"]    = [(t0, (qx,qy,qz,qw)), (t1, ...), ...]
        self._keyframes = defaultdict(lambda: {"translation": [], "rotation": []})
    

    def advance(self):
        self.current_time += self.time_step

    def set_mode_state():
        pass

    def set_node_position(self, node, position, time=None):
        if time is None: 
            time = self.current_time

        self._keyframes[node]["translation"].append((time, position))

    def set_node_rotation(self, node, rotation, time=None):
        if time is None: 
            time = self.current_time

        self._keyframes[node]["rotation"].append((time, rotation))

    def set_field(self):
        pass

    def set_skin_state(self, state, skin_nodes, time=None):
        """
        Given a 'state' that has deformed positions and rotations for each element’s cross-section,
        record a new keyframe at the current time.

        :param state:  Some data structure that can provide displacements & rotations
                       for each (element, cross_section_index).
        """
        model = self.model
        # For each element in the model
        for element_name, el in model["assembly"].items():

            # number of cross sections
            nen = len(el["nodes"])

            # Original reference coordinates (before deformation)
            X_ref = np.array(el["crd"])  # (nen, 3)

            # Displacements & rotations from 'state'
            pos_all = state.cell_array(el["name"], state.position)   # shape (nen,3?)
            rot_all = state.cell_array(el["name"], state.rotation)   # shape (nen,3x3)?

            for j in range(nen):
                # look up the glTF node index
                key = (element_name, j)
                if key not in skin_nodes:
                    continue

                # compute final position for cross section j
                x_def = X_ref[j] + pos_all[j]
                # convert rotation matrix -> quaternion
                qx, qy, qz, qw = Rotation.from_matrix(rot_all[j]).as_quat()

                # store a keyframe
                self.set_node_position(skin_nodes[key], (x_def[0], x_def[1], x_def[2]))
                self.set_node_rotation(skin_nodes[key], (qx, qy, qz, qw))


    def add_to(self, canvas):
        """
        Build a glTF Animation from the accumulated keyframes and
        then let the canvas write the final file.
        """
        gltf = canvas.gltf
    
        if not self._keyframes:
            return

        # 1) Create an Animation object
        anim = pygltflib.Animation(name=self.anim_name,
                                   samplers=[],
                                   channels=[])

        # Create multiple samplers and channels:
        #   - For each node, we have two samplers (translation, rotation)
        #   - Then two channels referencing those samplers

        # We'll need to record the *sampler index* for each node property as we build them
        # so we can attach channels referencing the correct sampler.
        node_position_sampler_index = {}
        node_rotation_sampler_index = {}

        # 2) Flatten and encode data for each node
        # We do them all in a single big set of buffers—time values and output values.
        # However, each node gets its own Sampler, because it has distinct times/values
        # in this implementation. (We could share times if they match exactly.)
        for node_idx, track_dict in self._keyframes.items():
            pos_keyframes = track_dict["translation"]  # list of (time, (x,y,z))
            rot_keyframes = track_dict["rotation"]     # list of (time, (qx,qy,qz,qw))

            if not pos_keyframes and not rot_keyframes:
                continue

            # Sort them by time just in case user added states out of order
            pos_keyframes.sort(key=lambda x: x[0])
            rot_keyframes.sort(key=lambda x: x[0])


            if pos_keyframes:
                # Create Sampler for translation
                sampler_index_t = _append_index(anim.samplers, pygltflib.AnimationSampler(
                    input=-1,    # placeholder, we fill them after we create Accessors
                    output=-1,   # also placeholder
                    interpolation="LINEAR"
                ))
                node_position_sampler_index[node_idx] = sampler_index_t
                # Temporarily store the arrays so we can embed them in the glTF buffer
                # after building all samplers.
                anim.samplers[sampler_index_t].extras = {
                    "times_array": np.array([k[0] for k in pos_keyframes], dtype=canvas.float_t),
                    "vals_array":  np.array([k[1] for k in pos_keyframes], dtype=canvas.float_t)  # shape (N,3)
                }
            
            if rot_keyframes:
                # Create Sampler for rotation
                sampler_index_r = _append_index(anim.samplers, pygltflib.AnimationSampler(
                    input=-1,
                    output=-1,
                    interpolation="LINEAR"
                ))
                node_rotation_sampler_index[node_idx] = sampler_index_r

                # Temporarily store the arrays so we can embed them in the glTF buffer
                # after building all samplers.
                anim.samplers[sampler_index_r].extras = {
                    "times_array": np.array([k[0] for k in rot_keyframes],   dtype=canvas.float_t),
                    "vals_array":  np.array([k[1] for k in rot_keyframes],   dtype=canvas.float_t)  # shape (N,4)
                }

        # 3) Now create Channels referencing each sampler
        for node_idx in self._keyframes:
            if node_idx in node_position_sampler_index:
                # Create a channel for translation
                anim.channels.append(pygltflib.AnimationChannel(
                    sampler=node_position_sampler_index[node_idx],
                    target=pygltflib.AnimationChannelTarget(
                        node=node_idx,
                        path="translation"
                    )
                ))

            if node_idx in node_rotation_sampler_index:
                # Create a channel for rotation
                anim.channels.append(pygltflib.AnimationChannel(
                    sampler=node_rotation_sampler_index[node_idx],
                    target=pygltflib.AnimationChannelTarget(
                        node=node_idx,
                        path="rotation"
                    )
                ))


        # 4) Insert the actual time / value data into glTF buffers.
        #    We'll create BufferViews and Accessors, then fix up each sampler's input/output
        #    to reference the newly created accessor indices.
        #    We'll do this "in bulk," iterating over new_animation.samplers
        for sampler in anim.samplers:

            # Accessors
            time_accessor_idx = _append_index(gltf.accessors, pygltflib.Accessor(
                bufferView=canvas._push_data(sampler.extras["times_array"].tobytes()),
                byteOffset=0,
                componentType=FLOAT,
                count=len(sampler.extras["times_array"]),
                type="SCALAR",
                min=[float(sampler.extras["times_array"].min())],
                max=[float(sampler.extras["times_array"].max())]
            ))

            # If path=="translation" we have 3 floats, if path=="rotation" we have 4.
            # But we already know shape from sampler.extras["vals_array"].shape
            val_type = "VEC3" if sampler.extras["vals_array"].shape[1]==3 else "VEC4"

            vals_accessor_idx = _append_index(gltf.accessors, pygltflib.Accessor(
                bufferView=canvas._push_data(sampler.extras["vals_array"].tobytes()),
                byteOffset=0,
                componentType=FLOAT,
                count=len(sampler.extras["vals_array"]),
                type=val_type
            ))

            # Now fix the sampler's input/output
            sampler.input  = time_accessor_idx
            sampler.output = vals_accessor_idx

            # remove extras so it won't try to JSON-serialize large arrays
            del sampler.extras["times_array"]
            del sampler.extras["vals_array"]


        # 5) Attach this new Animation to the glTF
        if not gltf.animations:
            gltf.animations = []

        i = _append_index(gltf.animations, anim)


def create_animation(artist, states, skin_nodes=None):

    # 1) Draw reference configuration with extrusions -> returns extrusion
    if skin_nodes is None:
        skin_nodes = skin_frames(artist.model, artist.canvas)

    # 2) Create the animation helper
    animation = Motion(artist.model, time_step=1)

    # 3) For each state, record a new keyframe
    for time in states.times:
        animation.set_skin_state(states[time], skin_nodes)
        animation.advance()

    animation.add_to(artist.canvas)
    return animation



def animate(sam_file, res_file=None, **opts):
    # Configuration is determined by successively layering
    # from sources with the following priorities:
    #      defaults < file configs < kwds
    from veux.frame import FrameArtist
    import veux.canvas.gltf
    from veux.model import read_model

    config = veux.config.Config()


    if sam_file is None:
        raise RenderError("Expected positional argument <sam-file>")

    if isinstance(sam_file, (str,)):
        model = read_model(sam_file)

    elif hasattr(sam_file, "asdict"):
        # Assuming an opensees.openseespy.Model
        model = sam_file.asdict()

    elif hasattr(sam_file, "read"):
        model = read_model(sam_file)


    if "RendererConfiguration" in model:
        veux.apply_config(model["RendererConfiguration"], config)

    veux.apply_config(opts, config)

    artist = FrameArtist(model, ndf=6,
                         config=config["artist_config"],
                         model_config=config["model_config"],
                         canvas=veux.canvas.gltf.GltfLibCanvas())

    skin_nodes = skin_frames(artist.model, artist.canvas, 
                                  config=artist._config_sketch("default")["surface"]["frame"])

    if res_file is not None:
        if isinstance(res_file, str):
            soln = veux.state.read_state(res_file, artist.model, **opts["state_config"])
        else:
            from veux.state import GroupSeriesSE3, StateSeries
            series = StateSeries(res_file, artist.model,
                transform = artist.dofs2plot,
                recover_rotations="conv"
            )
            soln = GroupSeriesSE3(series, artist.model, recover_rotations="conv", transform=artist.dofs2plot)
        if "time" not in opts:
            create_animation(artist, soln, skin_nodes)
        else:
            deform_extrusion(artist.model, artist.canvas, soln, skin_nodes)

    # artist.draw()
    return artist


if __name__ == "__main__":
    import sys
    from veux.errors import RenderError
    import veux.parser
    config = veux.parser.parse_args(sys.argv)

    try:
        artist = animate(**config)

        # write plot to file if output file name provided
        if config["write_file"]:
            artist.save(config["write_file"])

        elif hasattr(artist.canvas, "to_glb"):
            import veux.server
            server = veux.server.Server(glb=artist.canvas.to_glb(),
                                        viewer=config["viewer_config"].get("name", None))

            server.run(config["server_config"].get("port", None))


        elif hasattr(artist.canvas, "to_html"):
            import veux.server
            server = veux.server.Server(html=artist.canvas.to_html())
            server.run(config["server_config"].get("port", None))

    except (FileNotFoundError, RenderError) as e:
        # Catch expected errors to avoid printing an ugly/unnecessary stack trace.
        print(e, file=sys.stderr)
        print("         Run '{NAME} --help' for more information".format(NAME=sys.argv[0]), file=sys.stderr)
        sys.exit()

