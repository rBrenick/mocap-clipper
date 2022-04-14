import json
import os

with open(os.path.join(os.path.dirname(__file__), "resources", "fake_data.json"), "r") as fp:
    FAKE_DATA = json.load(fp)


class MocapClipperCoreInterface(object):

    def __init__(self):
        self.tool_window = None

        # noinspection PyUnreachableCode
        if 0:
            from . import mocap_clipper_ui
            self.tool_window = mocap_clipper_ui.MocapClipperWindow()  # for auto complete

    def get_scene_time_editor_data(self):
        return {}  # {example in 'MocapClipperMaya'}

    def get_rigs_in_scene(self):
        return {}  # {rig_name: rig_node}

    def get_pose_icon(self):
        return None  # qicon

    def get_mocap_icon(self):
        return None  # qicon

    def get_rig_icon(self):
        return None  # qicon

    def get_pose_files(self):
        return FAKE_DATA.get("pose_files")  # list of paths

    def import_mocap(self, file_path):
        pass

    def connect_mocap_to_rig(self, mocap_ns, rig_name):
        return []  # this return value gets sent to disconnect_mocap_from_rig

    def disconnect_mocap_from_rig(self, connect_result):
        pass

    def pre_bake(self):
        pass  # optional method that runs before baking to the rig

    def bake_to_rig(self, mocap_ns, rig_name, start_frame, end_frame, euler_filter=False):
        return []  # rig controls, gets sent to rebuild_pose_anim_layer

    def align_mocap_to_rig(self, mocap_ns, rig_name, root_name="root", pelvis_name="pelvis"):
        pass

    def rebuild_pose_anim_layer(self, controls):
        pass

    def apply_pose(self, pose_path, rig_name, on_frame=None, on_selected=False, set_key=True):
        pass

    def run_adjustment_blend(self):
        pass

    def set_time_range(self, time_range):
        pass

    def get_project_widgets(self):
        return []  # optional list of qwidgets
