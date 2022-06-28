import json
import os

from . import mocap_clipper_logger
from . import mocap_clipper_constants as k

log = mocap_clipper_logger.get_logger()

with open(os.path.join(os.path.dirname(__file__), "resources", "fake_data.json"), "r") as fp:
    FAKE_DATA = json.load(fp)


class MocapClipperCoreInterface(object):

    def __init__(self):
        self.tool_window = None
        self.allow_ui = False

        # noinspection PyUnreachableCode
        if 0:
            from . import mocap_clipper_ui
            self.tool_window = mocap_clipper_ui.MocapClipperWindow()  # for auto complete

        self.match_via_pose_file = "Using Pose File"
        self.match_via_attributes = "Using Attribute Values"

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

    def bake_to_rig(self, mocap_ns, rig_name, start_frame, end_frame):
        self.log_missing_implementation(self.bake_to_rig)
        return []  # rig controls, gets sent to rebuild_pose_anim_layer

    def save_pose(self, rig_name, on_frame=None):
        self.log_missing_implementation(self.save_pose)
        return ""  # pose file path

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
        pass  # method that runs after the clip has been baked to the rig

    def post_all_clips_bake(self):
        pass  # method that runs after all the clips have been processed

    def save_clip(self, clip_data, bake_config):
        self.log_missing_implementation(self.save_clip)

    def get_project_settings_widgets(self):
        return []  # optional list of qwidgets

    def get_project_action_widgets(self):
        return []  # optional list of qwidgets

    def get_pose_icon(self, pose_path=None):
        return None  # qicon

    def get_mocap_icon(self):
        return None  # qicon

    def get_rig_icon(self):
        return None  # qicon

    def get_default_output_folder(self):
        return ""

    ######################################################################################
    # Implementations comes pre-built
    
    def main_bake_function(self, clip_data, bake_config):
        """

        The big bake function that runs when pressing Bake To Rig

        Args:
            clip_data (k.ClipData): Result of self.get_scene_time_editor_data with some extra keys from the UI
            bake_config (k.BakeConfig):

        Returns:

        """

        cd = clip_data

        rig_name = bake_config.target_rig
        mocap_namespace = cd.namespace

        apply_start_pose = cd.start_pose_enabled
        apply_end_pose = cd.end_pose_enabled
        end_pose_same_as_start = cd.end_pose_same_as_start
        pose_layer_should_be_created = any([apply_start_pose, apply_end_pose, end_pose_same_as_start])

        start_frame = cd.start_frame
        end_frame = cd.end_frame
        log.info("Baking range: '{} - {}' to rig: '{}'".format(start_frame, end_frame, rig_name))

        log.debug("Running PreBake: {}".format(self.pre_bake))
        self.pre_bake()

        if bake_config.align_mocap_to_pose:

            pose_path = None
            if bake_config.align_mocap_to_start_pose:
                alignment_frame = start_frame

                if apply_start_pose:
                    pose_path = cd.start_pose_path
            else:
                alignment_frame = end_frame

                if apply_end_pose:
                    pose_path = cd.end_pose_path

            if pose_path:
                log.info("Applying pose for alignment: {}".format(pose_path))
                self.apply_pose(pose_path, rig_name)

            self.align_mocap_to_rig(
                mocap_namespace,
                rig_name,
                alignment_name=bake_config.mocap_alignment_name,
                on_frame=alignment_frame,
            )

        log.debug("Removing existing pose anim layer(s)")
        self.remove_pose_anim_layer()

        log.info("Baking mocap: '{}', to rig: '{}'".format(mocap_namespace, rig_name))
        rig_controls = self.bake_to_rig(
            mocap_ns=mocap_namespace,
            rig_name=rig_name,
            start_frame=start_frame,
            end_frame=end_frame,
        )

        if bake_config.run_euler_filter:
            log.debug("Running Euler Filter on {} control(s)".format(len(rig_controls)))
            self.run_euler_filter(rig_controls)

        if pose_layer_should_be_created:
            log.info("Re-building pose anim layer for: '{}' control(s)".format(len(rig_controls)))
            self.rebuild_pose_anim_layer(rig_controls)

            # create border keys on either end. might get overridden by poses below
            self.set_key_on_pose_layer(rig_controls, on_frame=start_frame)
            self.set_key_on_pose_layer(rig_controls, on_frame=end_frame)

            if apply_start_pose:
                start_pose_path = cd.start_pose_path
                log.info("Applying start pose: {}".format(start_pose_path))
                self.apply_pose(
                    pose_path=start_pose_path,
                    rig_name=rig_name,
                    on_frame=start_frame,
                )
                self.set_key_on_pose_layer(rig_controls)

            if apply_end_pose:
                end_pose_path = cd.end_pose_path
                log.info("Applying end pose: {}".format(end_pose_path))
                self.apply_pose(
                    pose_path=end_pose_path,
                    rig_name=rig_name,
                    on_frame=end_frame,
                )
                self.set_key_on_pose_layer(rig_controls)

            if end_pose_same_as_start:
                if not apply_end_pose:
                    if cd.end_pose_match_method == self.match_via_pose_file:
                        # save the first frame pose and re-apply it at the end
                        temp_pose_path = self.save_pose(
                            rig_name=rig_name,
                            on_frame=start_frame
                        )
                        self.apply_pose(
                            pose_path=temp_pose_path,
                            rig_name=rig_name,
                            on_frame=end_frame,
                        )

                    if cd.end_pose_match_method == self.match_via_attributes:
                        self.match_attribute_values_between_frames(rig_controls, start_frame, end_frame)

                    self.set_key_on_pose_layer(rig_controls)

            if bake_config.run_adjustment_blend:
                log.info("Running Adjustment Blend")
                self.run_adjustment_blend(k.SceneConstants.pose_anim_layer_name)

        if bake_config.set_time_range:
            log.info("Setting time range to '{} - {}'".format(start_frame, end_frame))
            self.set_time_range((start_frame, end_frame))

        self.post_bake()

        if bake_config.save_clip:
            self.save_clip(clip_data, bake_config)

    def get_alignment_joint_names(self):
        return "root", "pelvis"

    def get_pose_match_methods(self):
        return self.match_via_pose_file, self.match_via_attributes

    def get_clip_icon(self):
        return None  # qicon

    def get_scene_time_editor_data(self):
        self.log_missing_implementation(self.get_scene_time_editor_data)
        return {}  # {example in 'MocapClipperMaya'}

    def set_mocap_visibility(self, mocap_namespace, state=True):
        self.log_missing_implementation(self.get_scene_time_editor_data)

    def set_random_color_on_clip(self, clip_node):
        self.log_missing_implementation(self.set_random_color_on_clip)

    def import_mocap(self, file_path):
        self.log_missing_implementation(self.import_mocap)

    def rename_clip(self, node, new_clip_name=None):
        self.log_missing_implementation(self.rename_clip)
        return True  # clip was successfully renamed

    def delete_clips(self, clip_data, namespace_usage):
        self.log_missing_implementation(self.delete_clips)

    def align_mocap_to_rig(self, mocap_namespace, rig_name, root_name="root", alignment_name="pelvis", on_frame=None):
        self.log_missing_implementation(self.align_mocap_to_rig)

    def align_mocap_to_world_origin(self, mocap_namespace, root_name="root", alignment_name="pelvis"):
        self.log_missing_implementation(self.align_mocap_to_rig)

    def remove_pose_anim_layer(self):
        self.log_missing_implementation(self.remove_pose_anim_layer)

    def rebuild_pose_anim_layer(self, controls):
        self.log_missing_implementation(self.rebuild_pose_anim_layer)

    def project_root_animation_from_hips(self, mocap_namespace):
        self.log_missing_implementation(self.project_root_animation_from_hips)

    def toggle_root_aim(self, mocap_namespace):
        self.log_missing_implementation(self.toggle_root_aim)

    def run_euler_filter(self, controls):
        self.log_missing_implementation(self.run_euler_filter)

    def run_adjustment_blend(self, layer_name=None):
        self.log_missing_implementation(self.run_adjustment_blend)

    def set_time_range(self, time_range):
        self.log_missing_implementation(self.set_time_range)

    def set_key_on_pose_layer(self, controls, on_frame=None):
        self.log_missing_implementation(self.set_key_on_pose_layer)

    def match_attribute_values_between_frames(self, controls, src_frame, tgt_frame):
        self.log_missing_implementation(self.match_attribute_values_between_frames)

    def select_node(self, node):
        self.log_missing_implementation(self.select_node)

    def set_attr(self, node, attr_name, value):
        self.log_missing_implementation(self.set_attr)

    def get_attr(self, node, attr_name, default=None):
        self.log_missing_implementation(self.get_attr)
        return  # some value

    def get_random_color(self):
        import random
        import colorsys

        hue = random.random()
        light = 0.6
        saturation = 0.25 + ((random.random() - 0.5) * 0.2)  # 0.2 + (random.random() / 3.0)

        random_color = colorsys.hls_to_rgb(hue, light, saturation)
        return random_color
