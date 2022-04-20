import json
import os

from . import mocap_clipper_logger

log = mocap_clipper_logger.get_logger()

with open(os.path.join(os.path.dirname(__file__), "resources", "fake_data.json"), "r") as fp:
    FAKE_DATA = json.load(fp)


class MocapClipperCoreInterface(object):

    def __init__(self):
        self.tool_window = None

        # noinspection PyUnreachableCode
        if 0:
            from . import mocap_clipper_ui
            self.tool_window = mocap_clipper_ui.MocapClipperWindow()  # for auto complete

    def log_missing_implementation(self, func):
        log.error("'{}.{}()' has not been implemented".format(self.__class__.__name__, func.__name__))

    ######################################################################################
    # Required Project/Studio implementations

    def get_rigs_in_scene(self):
        self.log_missing_implementation(self.get_rigs_in_scene)
        return {}  # {rig_name: rig_node}

    def get_pose_files(self):
        self.log_missing_implementation(self.get_pose_files)
        return FAKE_DATA.get("pose_files")  # list of paths

    def bake_to_rig(self, mocap_ns, rig_name, start_frame, end_frame, euler_filter=False):
        self.log_missing_implementation(self.bake_to_rig)
        return []  # rig controls, gets sent to rebuild_pose_anim_layer

    def apply_pose(self, pose_path, rig_name, on_frame=None, on_selected=False):
        self.log_missing_implementation(self.apply_pose)

    def connect_mocap_to_rig(self, mocap_ns, rig_name):
        self.log_missing_implementation(self.connect_mocap_to_rig)
        return []  # this return value gets sent to disconnect_mocap_from_rig

    def disconnect_mocap_from_rig(self, connect_result):
        self.log_missing_implementation(self.disconnect_mocap_from_rig)

    ######################################################################################
    # Optional Project/Studio implementations

    def pre_bake(self):
        pass  # method that runs before baking to the rig

    def post_bake(self):
        pass  # method that runs after everything has been baked

    def get_project_settings_widgets(self):
        return []  # optional list of qwidgets

    def get_project_action_widgets(self):
        return []  # optional list of qwidgets

    def get_pose_icon(self):
        return None  # qicon

    def get_mocap_icon(self):
        return None  # qicon

    def get_rig_icon(self):
        return None  # qicon

    ######################################################################################
    # Implementations comes pre-built

    def get_scene_time_editor_data(self):
        self.log_missing_implementation(self.get_scene_time_editor_data)
        return {}  # {example in 'MocapClipperMaya'}

    def import_mocap(self, file_path):
        self.log_missing_implementation(self.import_mocap)

    def align_mocap_to_rig(self, mocap_ns, rig_name, root_name="root", pelvis_name="pelvis", on_frame=None):
        self.log_missing_implementation(self.align_mocap_to_rig)

    def remove_pose_anim_layer(self):
        self.log_missing_implementation(self.remove_pose_anim_layer)

    def rebuild_pose_anim_layer(self, controls):
        self.log_missing_implementation(self.rebuild_pose_anim_layer)

    def run_adjustment_blend(self):
        self.log_missing_implementation(self.run_adjustment_blend)

    def set_time_range(self, time_range):
        self.log_missing_implementation(self.set_time_range)

    def set_key_on_pose_layer(self, controls, on_frame=None):
        self.log_missing_implementation(self.set_key_on_pose_layer)

    def select_node(self, node):
        self.log_missing_implementation(self.select_node)

    def set_attr(self, node, attr_name, value):
        self.log_missing_implementation(self.set_attr)

    def get_attr(self, node, attr_name, default=None):
        self.log_missing_implementation(self.get_attr)
        return  # some value
