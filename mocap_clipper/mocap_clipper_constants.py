class ModuleConstants:
    extension_file_prefix = "mocap_clipper_ext"


class SceneConstants:
    pose_anim_layer_name = "PoseLayer"
    mocap_top_node_name = "mocap_top_node"
    mocap_ctrl_name = "mocap_ctrl"
    mocap_ctrl_offset_name = "mocap_ctrl_reverse_offset"


class ClipDataConstants:
    start_frame = "start_frame"
    end_frame = "end_frame"
    frame_duration = "frame_duration"
    node = "node"
    clip_parent = "clip_parent"
    namespace = "namespace"

    # mocap_clipper attributes
    start_pose_path = "start_pose"
    start_pose_enabled = "start_pose_enabled"
    end_pose_path = "end_pose"
    end_pose_enabled = "end_pose_enabled"
    end_pose_same_as_start = "end_pose_same_as_start"

    # derive from ui
    clip_name = "clip_name"
    target_rig = "target_rig"
    output_folder = "output_folder"


class BakeConfig:
    def __init__(self):
        self.align_mocap_to_pose = False
        self.align_mocap_to_start_pose = False
        self.align_mocap_to_end_pose = False
        self.mocap_alignment_name = ""

        self.project_root_from_hips = False
        self.run_euler_filter = False
        self.set_time_range = False
        self.run_adjustment_blend = False
        self.save_clip = False


cdc = ClipDataConstants
