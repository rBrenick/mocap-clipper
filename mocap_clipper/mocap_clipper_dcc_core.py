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

    ######################################################################################
    # Required Project/Studio implementations

    def get_rigs_in_scene(self):
        log.error(f"'{self.__class__.__name__}.{self.get_rigs_in_scene.__name__}' has not been implemented")
        return {}  # {rig_name: rig_node}

    def get_pose_files(self):
        log.error(f"'{self.__class__.__name__}.{self.get_pose_files.__name__}' has not been implemented")
        return FAKE_DATA.get("pose_files")  # list of paths

    def bake_to_rig(self, mocap_ns, rig_name, start_frame, end_frame, euler_filter=False):
        log.error(f"'{self.__class__.__name__}.{self.bake_to_rig.__name__}' has not been implemented")
        return []  # rig controls, gets sent to rebuild_pose_anim_layer

    def apply_pose(self, pose_path, rig_name, on_frame=None, on_selected=False, set_key=False):
        log.error(f"'{self.__class__.__name__}.{self.apply_pose.__name__}' has not been implemented")
        pass

    def connect_mocap_to_rig(self, mocap_ns, rig_name):
        log.error(f"'{self.__class__.__name__}.{self.connect_mocap_to_rig.__name__}' has not been implemented")
        return []  # this return value gets sent to disconnect_mocap_from_rig

    def disconnect_mocap_from_rig(self, connect_result):
        log.error(f"'{self.__class__.__name__}.{self.disconnect_mocap_from_rig.__name__}' has not been implemented")
        pass

    ######################################################################################
    # Optional Project/Studio implementations

    def pre_bake(self):
        pass  # method that runs before baking to the rig

    def get_project_settings_widgets(self):
        return []  # optional list of qwidgets

    def get_project_widgets(self):
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
        log.error(f"'{self.__class__.__name__}.{self.get_scene_time_editor_data.__name__}' has not been implemented")
        return {}  # {example in 'MocapClipperMaya'}

    def import_mocap(self, file_path):
        log.error(f"'{self.__class__.__name__}.{self.import_mocap.__name__}' has not been implemented")

    def align_mocap_to_rig(self, mocap_ns, rig_name, root_name="root", pelvis_name="pelvis"):
        log.error(f"'{self.__class__.__name__}.{self.align_mocap_to_rig.__name__}' has not been implemented")

    def remove_pose_anim_layer(self):
        log.error(f"'{self.__class__.__name__}.{self.remove_pose_anim_layer.__name__}' has not been implemented")

    def rebuild_pose_anim_layer(self, controls):
        log.error(f"'{self.__class__.__name__}.{self.rebuild_pose_anim_layer.__name__}' has not been implemented")

    def run_adjustment_blend(self):
        log.error(f"'{self.__class__.__name__}.{self.run_adjustment_blend.__name__}' has not been implemented")

    def set_time_range(self, time_range):
        log.error(f"'{self.__class__.__name__}.{self.set_time_range.__name__}' has not been implemented")

    def select_node(self, node):
        log.error(f"'{self.__class__.__name__}.{self.select_node.__name__}' has not been implemented")

    def set_attr(self, node, attr_name, value):
        log.error(f"'{self.__class__.__name__}.{self.set_attr.__name__}' has not been implemented")

    def get_attr(self, node, attr_name, default=None):
        log.error(f"'{self.__class__.__name__}.{self.get_attr.__name__}' has not been implemented")
        return  # some value
