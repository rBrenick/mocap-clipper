import json
import os

with open(os.path.join(os.path.dirname(__file__), "resources", "fake_data.json"), "r") as fp:
    FAKE_DATA = json.load(fp)


class MocapClipperCoreInterface(object):

    def get_scene_time_editor_data(self):
        return {}  # {example in 'MocapClipperMaya'}

    def get_rigs_in_scene(self):
        return {}  # {rig_name: rig_node}

    def get_pose_icon(self):
        return None  # qicon

    def get_pose_files(self):
        return FAKE_DATA.get("pose_files")  # list of paths

    def bake_to_rig(self, mocap_ns, rig_name, start_frame, end_frame):
        return

    def constrain_mocap_to_rig(self, mocap_ns, rig_name):
        return []

    def disconnect_mocap_from_rig(self, constrain_values):
        return True

    def apply_pose(self, pose_path, rig_name, frame=None, only_apply_to_selection=False):
        return
