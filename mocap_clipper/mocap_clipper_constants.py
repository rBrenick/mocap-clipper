class ModuleConstants:
    extension_file_prefix = "mocap_clipper_ext"


class SceneConstants:
    pose_anim_layer_name = "PoseLayer"
    mocap_top_node_name = "mocap_top_node"
    mocap_ctrl_name = "mocap_ctrl"
    mocap_ctrl_offset_name = "mocap_ctrl_reverse_offset"
    skeleton_root = "root"

    mocap_clipper_data = "mocap_clipper_data"


class ClipData(object):
    def __init__(self):
        self.start_frame = None
        self.frame_duration = None
        self.end_frame = None
        self.node = None
        self.namespace = ""
        self.clip_parent = None
        self.clip_name = ""
        self.clip_color = (0, 0, 0)

        # MocapClipper attributes
        self.start_pose_enabled = False
        self.start_pose_path = ""
        self.end_pose_enabled = False
        self.end_pose_path = ""
        self.end_pose_same_as_start = False
        self.end_pose_match_method = None

    def to_dict(self):
        out_dict = {}
        for k, v in self.__dict__.items():
            if v == self.node:
                v = str(self.node)
            out_dict[k] = v
        return out_dict

    def from_dict(self, input_dict):
        for k, v in input_dict.items():
            if hasattr(self, k):
                setattr(self, k, v)


class BakeConfig(object):
    def __init__(self):
        self.align_mocap_to_pose = False
        self.align_mocap_to_start_pose = False
        self.align_mocap_to_end_pose = False
        self.mocap_alignment_name = ""

        self.run_euler_filter = False
        self.set_time_range = False
        self.run_adjustment_blend = False
        self.save_clip = False

        self.target_rig = None
        self.output_folder = ""
