import json
import os

with open(os.path.join(os.path.dirname(__file__), "resources", "fake_data.json"), "r") as fp:
    FAKE_DATA = json.load(fp)


class MocapClipperCoreInterface(object):

    def get_scene_time_editor_data(self):
        return {}

    def get_rigs_in_scene(self):
        return []

    def get_pose_icon(self):
        return None

    def get_pose_files(self):
        return FAKE_DATA.get("pose_files")

    def apply_pose(self, pose_path, rig_ns, only_apply_to_selection=False):
        return