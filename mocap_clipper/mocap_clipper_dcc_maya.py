import pymel.core as pm
from maya import cmds
from . import adjustment_blend_maya
from . import mocap_clipper_constants as k
from . import mocap_clipper_dcc_core


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

        # parent nodes under group
        mocap_grp_name = "{}:{}".format(nspace, k.SceneConstants.mocap_top_grp_name)
        mocap_grp = pm.createNode('transform', n=mocap_grp_name)
        mocap_grp.overrideEnabled.set(True)
        pm.parent(mocap_top_nodes, mocap_grp)

        # get all transforms from fbx
        mocap_nodes = []
        mocap_nodes.extend(mocap_top_nodes)
        for mocap_top_node in mocap_top_nodes:
            for mocap_node in pm.listRelatives(mocap_top_node, ad=True):
                mocap_nodes.append(mocap_node)

        pm.select(mocap_nodes)
        pm.optionVar["ctePopulateIncludeRoot"] = 0
        cmds.TimeEditorCreateClip()

    def rebuild_pose_anim_layer(self, controls):
        self.remove_pose_anim_layer()

        pm.select(controls, replace=True)
        new_anim_layer = pm.animLayer(k.SceneConstants.pose_anim_layer_name, addSelectedObjects=True)
        select_anim_layer(new_anim_layer)

    def remove_pose_anim_layer(self):
        if pm.objExists(k.SceneConstants.pose_anim_layer_name):
            pm.delete(k.SceneConstants.pose_anim_layer_name)

    def align_mocap_to_rig(self, mocap_ns, rig_name, root_name="root", pelvis_name="pelvis"):
        target_rig = self.get_rigs_in_scene().get(rig_name)
        rig_ns = target_rig.namespace()

        top_grp = pm.PyNode(mocap_ns + k.SceneConstants.mocap_top_grp_name)
        root = mocap_ns + root_name
        pelvis = mocap_ns + pelvis_name
        rig_root = rig_ns + root_name
        rig_pelvis = rig_ns + pelvis_name

        # reset top node
        top_grp.setMatrix(pm.dt.Matrix.identity)

        # align with rig hips
        pelvis_matrix = pm.dt.Matrix(pm.xform(pelvis, q=True, matrix=True, worldSpace=True))
        rig_pelvis_matrix = pm.dt.Matrix(pm.xform(rig_pelvis, q=True, matrix=True, worldSpace=True))

        diff_pos = rig_pelvis_matrix.translate - pelvis_matrix.translate
        top_grp.setTranslation(diff_pos)

        # create new root that's aligned with the rig (since the mocap one might be a bit off)
        imported_root_name = root + "_RAW_IMPORT"
        if pm.objExists(imported_root_name):
            new_root = pm.PyNode(root)
        else:
            imported_root = pm.rename(root, imported_root_name)
            new_root = pm.createNode("transform", name=root)
            new_root.setParent(imported_root)

        rig_root_matrix = pm.dt.Matrix(pm.xform(rig_root, q=True, matrix=True, worldSpace=True))
        new_root.setMatrix(rig_root_matrix, worldSpace=True)

    def run_adjustment_blend(self):
        return adjustment_blend_maya.adjustment_blend(k.SceneConstants.pose_anim_layer_name)

    def set_time_range(self, time_range):
        pm.playbackOptions(animationStartTime=time_range[0])
        pm.playbackOptions(animationEndTime=time_range[1])
        pm.playbackOptions(minTime=time_range[0])
        pm.playbackOptions(maxTime=time_range[1])


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
