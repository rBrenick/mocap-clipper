import os.path

import pymel.core as pm
from maya import cmds
from . import adjustment_blend_maya
from . import mocap_clipper_constants as k
from . import mocap_clipper_dcc_core
from . import mocap_clipper_logger
from PySide2 import QtWidgets, QtGui

log = mocap_clipper_logger.get_logger()


class MocapClipperMaya(mocap_clipper_dcc_core.MocapClipperCoreInterface):
    def get_scene_time_editor_data(self):
        all_clip_data = dict()
        scene_clips = pm.ls(type="timeEditorClip")

        # acquire grouping hierarchy
        clip_hierarchy = {}
        for te_clip in scene_clips:
            # not sure how to handle multiple clips in a clip
            i = te_clip.clip.getArrayIndices()[0]
            clip_name = te_clip.getAttr(f"clip[{i}].clipName")

            parent_attr = pm.listConnections(te_clip + f".clip[{i}].clipParent", plugs=True)
            if parent_attr:
                parent_clip_node = parent_attr[0].node()
                clip_hierarchy[clip_name] = parent_clip_node

        for te_clip in scene_clips:
            # not sure how to handle multiple clips in a clip
            i = te_clip.clip.getArrayIndices()[0]

            clip_name = te_clip.getAttr(f"clip[{i}].clipName")
            clip_parent = clip_hierarchy.get(clip_name)

            start_frame_offset = 0
            parent_clip_node = clip_parent
            while parent_clip_node:
                parent_i = parent_clip_node.clip.getArrayIndices()[0]
                parent_clip_name = parent_clip_node.getAttr(f"clip[{parent_i}].clipName")
                start_frame_offset += parent_clip_node.getAttr(f"clip[{parent_i}].clipStart")
                parent_clip_node = clip_hierarchy.get(parent_clip_name)

            clip_data = dict()
            clip_data[k.cdc.start_frame] = te_clip.getAttr(f"clip[{i}].clipStart") + start_frame_offset
            clip_data[k.cdc.frame_duration] = te_clip.getAttr(f"clip[{i}].clipDuration")
            clip_data[k.cdc.end_frame] = clip_data[k.cdc.start_frame] + clip_data[k.cdc.frame_duration]
            clip_data[k.cdc.node] = te_clip
            clip_data[k.cdc.clip_parent] = clip_parent
            clip_data[k.cdc.namespace] = get_namespace_from_time_clip(te_clip)
            clip_data[k.cdc.clip_name] = clip_name

            # mocap_clipper attributes
            clip_data[k.cdc.start_pose_enabled] = self.get_attr(te_clip, k.cdc.start_pose_enabled, default=False)
            clip_data[k.cdc.start_pose_path] = self.get_attr(te_clip, k.cdc.start_pose_path, default="")
            clip_data[k.cdc.end_pose_enabled] = self.get_attr(te_clip, k.cdc.end_pose_enabled, default=False)
            clip_data[k.cdc.end_pose_path] = self.get_attr(te_clip, k.cdc.end_pose_path, default="")
            clip_data[k.cdc.end_pose_same_as_start] = self.get_attr(te_clip, k.cdc.end_pose_same_as_start, default=False)

            all_clip_data[clip_name] = clip_data

        return all_clip_data

    def select_node(self, node):
        pm.select(node)

    def get_attr(self, node, attr_name, default=None):
        if node.hasAttr(attr_name):
            attr_val = node.getAttr(attr_name)

            if attr_val == "True":
                attr_val = True

            if attr_val == "False":
                attr_val = False

            return attr_val
        return default

    def set_attr(self, node, attr_name, value):
        if not node.hasAttr(attr_name):
            node.addAttr(attr_name, dataType='string')
        node.setAttr(attr_name, value, type="string")

    def import_mocap(self, file_path):
        nspace = 'mocapImport'
        i = 0
        while pm.namespace(exists=nspace + str(i)):
            i += 1
        nspace += str(i)

        pm.FBXResetImport()
        pm.mel.eval('FBXImportMode -v add')
        pm.mel.eval('FBXImportSetTake -ti -1')
        pm.mel.file(file_path, i=True, type='FBX', ra=True, namespace=nspace, options='fbx', importTimeRange='override')
        mocap_top_nodes = pm.ls(pm.namespaceInfo(nspace, listNamespace=True, recurse=True), assemblies=True)

        # parent nodes under two controllers
        mocap_top_name = "{}:{}".format(nspace, k.SceneConstants.mocap_top_node_name)
        mocap_top_node = create_triangle_ctrl(mocap_top_name, radius=75, sections=5)
        mocap_top_node.setAttr("visibility", keyable=False, channelBox=True)

        mocap_ctrl_name = "{}:{}".format(nspace, k.SceneConstants.mocap_ctrl_name)
        mocap_ctrl_node = create_triangle_ctrl(mocap_ctrl_name)
        mocap_ctrl_node.setParent(mocap_top_node)
        mocap_ctrl_node.setAttr("visibility", keyable=False, channelBox=True)

        # create a reverse transform so the parenting can be relative to the world again
        mocap_ctrl_offset_name = "{}:{}".format(nspace, k.SceneConstants.mocap_ctrl_offset_name)
        mocap_ctrl_offset = pm.createNode("transform", name=mocap_ctrl_offset_name)
        mocap_ctrl_offset.setParent(mocap_ctrl_node)

        self.project_mocap_ctrl_to_ground_under_hips(nspace + ":")

        pm.parent(mocap_top_nodes, mocap_ctrl_offset)

        # get all transforms from fbx
        mocap_nodes = []
        mocap_nodes.extend(mocap_top_nodes)
        for mocap_top_node in mocap_top_nodes:
            for mocap_node in pm.listRelatives(mocap_top_node, ad=True, type="joint"):
                mocap_nodes.append(mocap_node)

        return mocap_nodes

    def project_mocap_ctrl_to_ground_under_hips(self, namespace):
        mocap_ctrl_name = "{}{}".format(namespace, k.SceneConstants.mocap_ctrl_name)
        mocap_ctrl_offset_name = "{}{}".format(namespace, k.SceneConstants.mocap_ctrl_offset_name)
        mocap_top_name = "{}{}".format(namespace, k.SceneConstants.mocap_top_node_name)

        mocap_top_node = pm.PyNode(mocap_top_name)
        mocap_ctrl_node = pm.PyNode(mocap_ctrl_name)
        mocap_ctrl_offset_node = pm.PyNode(mocap_ctrl_offset_name)
        mocap_pelvis = pm.PyNode(namespace + ":pelvis")

        offset_world_matrix = mocap_ctrl_offset_node.getMatrix(worldSpace=True)

        pelvis_matrix = mocap_pelvis.getAttr("worldMatrix")
        relative_matrix = pelvis_matrix * mocap_top_node.getAttr("worldMatrix").inverse()

        mocap_ctrl_node.setTranslation([relative_matrix.translate.x, 0, relative_matrix.translate.z])

        # set Y rotation from pelvis X direction
        rot = relative_matrix.rotate.asEulerRotation()
        rot.setDisplayUnit(pm.dt.Angle.Unit.degrees)
        mocap_ctrl_node.rotateY.set(rot.x + 90)

        # reset the offset transform to invert this offset
        mocap_ctrl_offset_node.setMatrix(offset_world_matrix, worldSpace=True)

    def clear_root_rotation_keys(self, namespace):
        mocap_root_name = "{}root".format(namespace)
        pm.cutKey(mocap_root_name, attribute=["rotateX", "rotateY", "rotateZ"], clear=True)
        log.info("Cleared rotation keys from: {}".format(mocap_root_name))
        pm.select(mocap_root_name)

    def set_mocap_visibility(self, mocap_ns, state=True):
        mocap_top_name = "{}{}".format(mocap_ns, k.SceneConstants.mocap_top_node_name)
        mocap_top_node = pm.PyNode(mocap_top_name)
        mocap_top_node.visibility.set(state)

    def create_time_editor_clip(self, mocap_nodes, clip_name):
        return create_time_editor_clip(mocap_nodes, clip_name)

    def rename_clip(self, node, new_clip_name=None):
        if not new_clip_name:
            current_clip_name = self.get_attr(node, "clip[0].clipName")
            new_clip_name = self.get_new_clip_name_from_dialog(current_clip_name)

        if not new_clip_name:
            return

        if not node.hasAttr("clip[0].clipName"):
            log.warning("Unable to find clipName attribute on node: {}".format(node))
            return

        node.setAttr("clip[0].clipName", new_clip_name, type="string")
        return True

    def delete_clips(self, clip_datas, namespace_usage):
        to_delete = []
        for clip_data in clip_datas:
            time_clip_node = clip_data.get(k.cdc.node)

            mocap_ns = clip_data.get(k.cdc.namespace)
            amount_of_clips_with_this_namespace = len(namespace_usage.get(mocap_ns))

            if amount_of_clips_with_this_namespace == 1:
                log.info("Only one clip found using this namespace, removing skeleton from scene: {}".format(mocap_ns))
                pm.namespace(removeNamespace=mocap_ns.rstrip(":"), deleteNamespaceContent=True)

            to_delete.append(time_clip_node)
            namespace_usage[mocap_ns].remove(time_clip_node)

        pm.delete(to_delete)

    def get_new_clip_name_from_dialog(self, current_clip_name):
        from . import ui_utils
        clip_name, _ = QtWidgets.QInputDialog.getText(
            ui_utils.get_app_window(),
            "New Clip Name",
            "Enter the new name of the clip: ",
            QtWidgets.QLineEdit.Normal,
            current_clip_name,
        )
        return clip_name

    def rebuild_pose_anim_layer(self, controls):
        self.remove_pose_anim_layer()

        pm.select(controls, replace=True)
        new_anim_layer = pm.animLayer(k.SceneConstants.pose_anim_layer_name, addSelectedObjects=True)
        select_anim_layer(new_anim_layer)

    def remove_pose_anim_layer(self):
        if pm.objExists(k.SceneConstants.pose_anim_layer_name):
            pm.delete(k.SceneConstants.pose_anim_layer_name)

    def align_mocap_to_rig(self, mocap_ns, rig_name, root_name="root", alignment_name="root", on_frame=None, match_transform=True):
        mocap_ctrl_name = "{}{}".format(mocap_ns, k.SceneConstants.mocap_ctrl_name)
        mocap_ctrl_node = pm.PyNode(mocap_ctrl_name)

        target_rig = self.get_rigs_in_scene().get(rig_name)
        rig_ns = target_rig.namespace()

        root = mocap_ns + root_name
        alignment_node_name = mocap_ns + alignment_name
        rig_root = rig_ns + root_name
        rig_alignment = rig_ns + alignment_name

        # align with rig joint
        if on_frame:
            alignment_matrix = pm.getAttr(alignment_node_name + ".worldMatrix", time=on_frame)
        else:
            alignment_matrix = pm.getAttr(alignment_node_name + ".worldMatrix")
        rig_align_matrix = pm.getAttr(rig_alignment + ".worldMatrix")

        if match_transform:

            # calculate relative matrix between controller and alignment joint
            reverse_alignment = mocap_ctrl_node.getMatrix(worldSpace=True) * alignment_matrix.inverse()

            # add that relative matrix to target world matrix
            out_matrix = reverse_alignment * rig_align_matrix

            # set final parent matrix
            mocap_ctrl_node.setMatrix(out_matrix, worldSpace=True)

        else:
            # match position
            diff_pos = rig_align_matrix.translate - alignment_matrix.translate
            mocap_ctrl_node.setTranslation(diff_pos)

        # create new root that's aligned with the rig (since the mocap one might be a bit off)
        mocap_ctrl = get_mocap_root_ctrl(mocap_root=pm.PyNode(root))

        rig_root_matrix = pm.getAttr(rig_root + ".worldMatrix")
        mocap_ctrl.setMatrix(rig_root_matrix, worldSpace=True)

    def project_root_animation_from_hips(self, mocap_namespace):
        with pm.UndoChunk():
            project_new_root(
                mocap_namespace + "root",
                mocap_namespace + "pelvis",
            )

    def run_euler_filter(self, controls):
        pm.select(controls)
        pm.filterCurve()

    def run_adjustment_blend(self, layer_name=None):
        # ignore layer_name variable value when called via the right click menu
        if isinstance(layer_name, bool):
            layer_name = None
        return adjustment_blend_maya.run_adjustment_blend(layer_name, allow_ui=self.allow_ui)

    def set_time_range(self, time_range):
        pm.playbackOptions(animationStartTime=time_range[0])
        pm.playbackOptions(animationEndTime=time_range[1])
        pm.playbackOptions(minTime=time_range[0])
        pm.playbackOptions(maxTime=time_range[1])

    def set_key_on_pose_layer(self, controls, on_frame=None):
        if on_frame is not None:
            pm.currentTime(on_frame)
        pm.setKeyframe(controls, animLayer=k.SceneConstants.pose_anim_layer_name)

    def get_clip_icon(self):
        return QtGui.QIcon(":adjustTimeline.png")


def get_namespace_from_time_clip(te_clip):
    i = te_clip.clip.getArrayIndices()[0]
    clip_id = te_clip.getAttr(f"clip[{i}].clipid")

    namespaces = set()
    for driven_node in pm.timeEditorClip(clip_id, q=True, drivenObjects=True):  # type: str
        namespaces.add(get_namespace(driven_node))

    if namespaces:
        return list(namespaces)[0]


def get_namespace(node):
    return ":".join(node.split(":")[:-1]) + ":"


def select_anim_layer(layer_name):
    [pm.animLayer(al, edit=True, selected=False) for al in pm.ls(type="animLayer")]
    pm.animLayer(layer_name, edit=True, selected=True)


def create_time_editor_clip(nodes, clip_name="SpecialClip"):
    composition_name = "MocapImport"

    if composition_name not in (cmds.timeEditorComposition(q=True, allCompositions=True) or []):
        cmds.timeEditorComposition(composition_name)

    cmds.timeEditor(mute=True)

    existing_tracks = cmds.timeEditorTracks(composition_name, q=True, allTracks=True) or []
    track_name = composition_name + "Track_{}".format(len(existing_tracks))
    cmds.timeEditorTracks(composition_name, edit=True, addTrack=-1, trackName=track_name)

    pm.select(nodes)
    cmds.timeEditorClip(
        clip_name,
        track='{}|{}'.format(composition_name, track_name),
        addSelectedObjects=True
    )

    cmds.timeEditor(mute=False)


def project_new_root(mocap_root, mocap_pelvis):
    mocap_root = pm.PyNode(mocap_root)
    mocap_pelvis = pm.PyNode(mocap_pelvis)

    pelvis_keys = pm.keyframe(mocap_pelvis, query=True, timeChange=True)
    if pelvis_keys:
        time_range = pelvis_keys[0], pelvis_keys[-1]
    else:
        print("Key data not found on {}. Using scene time range instead.".format(mocap_pelvis))
        time_range = pm.playbackOptions(q=True, min=True), pm.playbackOptions(q=True, max=True)

    new_root = get_mocap_root_ctrl(mocap_root)

    point_const = pm.pointConstraint(mocap_pelvis, new_root, skip=["y"])

    pelvis_aim_offset = pm.createNode("transform", name=mocap_pelvis + "_aim_offset")
    pelvis_aim_offset.setParent(mocap_pelvis, relative=True)
    pelvis_aim_offset.translateY.set(-50)
    aim_const = pm.aimConstraint(
        mocap_pelvis,
        new_root,
        aimVector=[0, 0, 1],
        upVector=[0, -1, 0],
        worldUpType='object',
        worldUpObject=pelvis_aim_offset,
    )

    # mocap_locs = {}
    # for mocap_root_child in pm.listRelatives(mocap_root, children=True):
    #     temp_loc = pm.createNode("transform", name=mocap_root_child + "_projection_bake")
    #     temp_loc.setParent(new_root)
    #     pm.parentConstraint(mocap_root_child, temp_loc)
    #     mocap_locs[mocap_root_child] = temp_loc

    # bake the animation data to our projected locators
    bake_locators = [new_root]
    # bake_locators.extend(list(mocap_locs.values()))
    try:
        pm.refresh(suspend=True)
        pm.bakeResults(bake_locators, t=time_range, simulation=True)
    finally:
        pm.refresh(suspend=False)

    # constrain joints to the projected locators
    # for mocap_jnt, bake_loc in mocap_locs.items():
    #     pm.parentConstraint(bake_loc, mocap_jnt)

    # bake on the original joints
    # pm.bakeResults(list(mocap_locs.keys()), t=time_range, sm=False)

    # delete temp bake nodes
    # to_delete = list(mocap_locs.values())
    # to_delete.append(pelvis_aim_offset)
    pm.delete([point_const, aim_const])

    if pm.objExists(new_root+".blendPoint1"):
        pm.deleteAttr(new_root+".blendPoint1")

    if pm.objExists(new_root+".blendAim1"):
        pm.deleteAttr(new_root+".blendAim1")

    pm.select(new_root)


def get_mocap_root_ctrl(mocap_root):
    root_name = mocap_root.nodeName()  # includes namespace

    raw_import_name = root_name + "_RAW_IMPORT"
    if pm.objExists(raw_import_name):
        root_ctrl = mocap_root
    else:
        existing_root_parent = mocap_root.getParent().getParent()
        mocap_root.rename(raw_import_name)
        root_ctrl = create_triangle_ctrl(root_name, shape_normal=(0, 0, -1), radius=25)
        root_ctrl.setAttr("displayHandle", 1)
        root_ctrl.setAttr("visibility", keyable=False, channelBox=True)

        root_grp = pm.createNode("transform", name=root_name+"_counter_rotation")
        root_grp.inheritsTransform.set(False)

        decomp_root_grp = pm.createNode("decomposeMatrix", name=root_grp+"_decomposeMat")
        existing_root_parent.attr("worldMatrix").connect(decomp_root_grp.inputMatrix)
        decomp_root_grp.outputTranslate.connect(root_grp.translate)

        rot_blend = pm.createNode("pairBlend", name=root_grp+"_rot_blend")
        decomp_root_grp.outputRotate.connect(rot_blend.inRotate2)
        rot_blend.outRotate.connect(root_grp.rotate)

        root_ctrl.addAttr("inheritParentRotation", min=0, max=1, keyable=True)
        root_ctrl.attr("inheritParentRotation").connect(rot_blend.weight)

        root_grp.setParent(existing_root_parent)
        root_ctrl.setParent(root_grp)

    return root_ctrl


def create_triangle_ctrl(ctrl_name, shape_normal=(0, -1, 0), radius=50, sections=3):
    ctrl_node, _ = pm.circle(sections=sections, degree=1, normal=shape_normal, radius=radius, name=ctrl_name)
    ctrl_node.overrideEnabled.set(True)
    ctrl_node.overrideColor.set(16)
    return ctrl_node
