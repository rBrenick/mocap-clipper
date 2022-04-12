import pprint

from . import mocap_clipper_dcc_core
from . import mocap_clipper_constants as k
import pymel.core as pm


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

        pprint.pprint(clip_hierarchy)

        for te_clip in scene_clips:
            # not sure how to handle multiple clips in a clip
            i = te_clip.clip.getArrayIndices()[0]

            clip_name = te_clip.getAttr(f"clip[{i}].clipName")
            clip_parent = clip_hierarchy.get(clip_name)

            # depth limit of 30
            start_frame_offset = 0
            parent_clip_node = clip_parent
            while parent_clip_node:
                parent_i = parent_clip_node.clip.getArrayIndices()[0]
                parent_clip_name = parent_clip_node.getAttr(f"clip[{parent_i}].clipName")
                start_frame_offset += parent_clip_node.getAttr(f"clip[{parent_i}].clipStart")
                print(clip_name, parent_clip_node, parent_clip_name, start_frame_offset)
                parent_clip_node = clip_hierarchy.get(parent_clip_name)

            clip_data = dict()
            clip_data[k.cdc.start_frame] = te_clip.getAttr(f"clip[{i}].clipStart") + start_frame_offset
            clip_data[k.cdc.frame_duration] = te_clip.getAttr(f"clip[{i}].clipDuration")
            clip_data[k.cdc.end_frame] = clip_data[k.cdc.start_frame] + clip_data[k.cdc.frame_duration]
            clip_data[k.cdc.end_frame] = clip_data[k.cdc.start_frame] + clip_data[k.cdc.frame_duration]
            clip_data[k.cdc.node] = te_clip
            clip_data[k.cdc.clip_parent] = clip_parent
            all_clip_data[clip_name] = clip_data

        return all_clip_data

    def select_node(self, node):
        pm.select(node)

    def get_attr(self, node, attr_name):
        if node.hasAttr(attr_name):
            return node.getAttr(attr_name)

    def set_attr(self, node, attr_name, value):
        if not node.hasAttr(attr_name):
            node.addAttr(attr_name, dataType='string')
        node.setAttr(attr_name, value)