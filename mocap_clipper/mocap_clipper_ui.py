import json
import os.path
import sys
from functools import partial, wraps
from collections import defaultdict

from . import mocap_clipper_constants as k
from . import mocap_clipper_logger
from . import mocap_clipper_system as mcs
from . import resources
from . import ui_utils
from .ui import mocap_clipper_widget
from .ui_utils import QtCore, QtWidgets, QtGui

standalone_app = None
if not QtWidgets.QApplication.instance():
    standalone_app = QtWidgets.QApplication(sys.argv)
log = mocap_clipper_logger.get_logger()


class MocapClipperWindow(ui_utils.ToolWindow):
    def __init__(self):
        super(MocapClipperWindow, self).__init__()
        log.debug("Window __init__")

        self.ui = mocap_clipper_widget.Ui_MocapClipperWidget()
        clipper_ui_widget = QtWidgets.QWidget()
        self.ui.setupUi(clipper_ui_widget)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.addWidget(clipper_ui_widget)
        main_ui_widget = QtWidgets.QWidget()
        main_ui_widget.setLayout(main_layout)
        self.setCentralWidget(main_ui_widget)

        self.setWindowTitle("Mocap Clipper")
        self.setWindowIcon(QtGui.QIcon(resources.get_image_path("mocap_clipper_icon")))

        mcs.dcc.tool_window = self
        mcs.dcc.allow_ui = True

        self.mocap_connect_result = None
        self.clip_data_refresh_is_active = False

        # set UI
        self.scene_data = None
        self.ui.main_splitter.setSizes([1, 2])
        self.ui_refresh_from_project()
        self.ui_refresh_from_scene()

        self.set_ui_from_dcc_settings()
        self.connect_ui_to_actions()
        self.connect_layout_visbilities()
        self.connect_marking_menus_and_shortcuts()

        ui_utils.set_combo_box_searchable(self.ui.start_pose_CB)
        ui_utils.set_combo_box_searchable(self.ui.end_pose_CB)

        # Menu bar
        menu_bar = QtWidgets.QMenuBar()
        ui_utils.build_log_level_menu(menu_bar, log_cls=log)
        self.setMenuBar(menu_bar)

        if not mcs.dcc.mocap_preview_available:
            self.ui.connect_mocap_to_rig_BTN.hide()

    def set_ui_from_dcc_settings(self):
        # set icons
        mocap_icon = mcs.dcc.get_mocap_icon() or QtGui.QIcon()
        refresh_icon = QtGui.QIcon(resources.get_image_path("refresh_icon"))
        self.ui.refresh_BTN.setIcon(refresh_icon)
        self.ui.refresh_project_BTN.setIcon(refresh_icon)
        self.ui.import_mocap_BTN.setIcon(mocap_icon)
        self.ui.bake_BTN.setIcon(mocap_icon)

        # add project options
        self.ui.align_mocap_CB.addItems(mcs.dcc.get_alignment_joint_names())
        self.ui.end_pose_match_method_CB.addItems(mcs.dcc.get_pose_match_methods())

        # set output folder
        self.ui.output_path_W.path_dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        default_project_folder = mcs.dcc.get_default_output_folder()
        if not self.ui.output_path_W.path() and default_project_folder:
            self.ui.output_path_W.set_path(default_project_folder)

        # add project specific widgets and actions
        for project_settings_widget in mcs.dcc.get_project_settings_widgets():
            self.ui.project_settings_layout.addWidget(project_settings_widget)

        for project_action_widget in mcs.dcc.get_project_action_widgets():
            self.ui.project_widgets_layout.addWidget(project_action_widget)

    def connect_ui_to_actions(self):
        # buttons above clip list
        self.ui.import_mocap_BTN.clicked.connect(self.import_mocap)
        self.ui.refresh_BTN.clicked.connect(self.ui_refresh_from_scene)
        self.ui.refresh_project_BTN.clicked.connect(self.ui_refresh_from_project)

        # clip list
        self.ui.clips_LW.itemSelectionChanged.connect(self.ui_update_clip_display_info)
        self.ui.clips_LW.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.clips_LW.customContextMenuRequested.connect(self.build_clip_list_ctx_menu)

        # preprocess actions
        self.ui.reproject_root_anim_BTN.clicked.connect(self.project_root_animation_from_hips)
        self.ui.reproject_mocap_ctrl_BTN.clicked.connect(self.reproject_mocap_control_under_hips)
        self.ui.align_root_to_rig_BTN.clicked.connect(self.align_mocap_with_rig)
        self.ui.align_root_to_origin_BTN.clicked.connect(self.align_mocap_to_world_origin)
        self.ui.toggle_root_aim_BTN.clicked.connect(self.toggle_root_aim)

        # clip data
        self.ui.rename_clip_BTN.clicked.connect(self.rename_selected_clip)

        # pose configuration
        self.ui.start_pose_CHK.stateChanged.connect(self.set_active_clip_data)
        self.ui.start_pose_CHK.stateChanged.connect(self.ui.start_pose_CB.setEnabled)
        self.ui.start_pose_CB.currentIndexChanged.connect(self.set_active_clip_data)
        self.ui.start_pose_CB.currentIndexChanged.connect(self.match_end_pose_to_start)

        self.ui.end_pose_CHK.stateChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_CHK.stateChanged.connect(self.ui.end_pose_CB.setEnabled)
        self.ui.end_pose_CB.currentIndexChanged.connect(self.set_active_clip_data)

        self.ui.end_pose_same_CHK.stateChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_same_CHK.stateChanged.connect(self.ui.end_pose_match_method_CB.setEnabled)
        self.ui.end_pose_match_method_CB.currentIndexChanged.connect(self.set_active_clip_data)

        # bake configuration
        self.ui.align_mocap_CHK.stateChanged.connect(self.ui.align_to_start_pose_RB.setEnabled)
        self.ui.align_mocap_CHK.stateChanged.connect(self.ui.align_to_end_pose_RB.setEnabled)
        self.ui.save_clip_CHK.stateChanged.connect(self.ui.output_path_W.setEnabled)

        # bake actions
        self.ui.connect_mocap_to_rig_BTN.clicked.connect(self.toggle_mocap_constraint)
        self.ui.bake_BTN.clicked.connect(self.bake_to_rig)

    def connect_layout_visbilities(self):
        self.ui.pose_configuration_BTN.toggled.connect(self.ui.pose_configuration_widget.setVisible)
        self.ui.preprocess_mocap_actions_BTN.toggled.connect(self.ui.preprocess_mocap_actions_widget.setVisible)
        self.ui.bake_configuration_BTN.toggled.connect(self.ui.bake_configuration_widget.setVisible)
        self.ui.bake_actions_BTN.toggled.connect(self.ui.bake_actions_widget.setVisible)
        self.ui.project_widgets_BTN.toggled.connect(self.ui.project_widgets_widget.setVisible)

    def connect_marking_menus_and_shortcuts(self):
        widget_run_actions = {
            self.ui.start_pose_CB: self.apply_start_pose,
            self.ui.start_pose_CHK: self.apply_start_pose,
            self.ui.end_pose_CB: self.apply_end_pose,
            self.ui.end_pose_CHK: self.apply_end_pose,
            self.ui.end_pose_same_CHK: self.apply_end_pose,
            self.ui.align_mocap_CHK: self.align_mocap_with_rig,
            self.ui.align_to_start_pose_RB: self.align_mocap_with_rig,
            self.ui.align_to_end_pose_RB: self.align_mocap_with_rig,
            self.ui.set_time_range_CHK: self.set_time_range,
            self.ui.adjustment_blend_CHK: mcs.dcc.run_adjustment_blend,
        }
        for widget, run_action in widget_run_actions.items():
            action_list = [
                {"Apply": run_action}
            ]
            widget_ctx_menu = partial(self.build_widget_ctx_menu, action_list)
            widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            widget.customContextMenuRequested.connect(widget_ctx_menu)

        # shortcuts
        del_hotkey = QtWidgets.QShortcut(
            QtGui.QKeySequence("DEL"),
            self.ui.clips_LW,
            self.delete_selected_clips,
        )
        del_hotkey.setContext(QtCore.Qt.WidgetShortcut)

    def deco_disable_clip_data_set_signals(func):
        """Decorator for disabling the scene node attribute setting while we're refreshing the UI"""

        @wraps(func)
        def inner(self, *args, **kwargs):
            self.clip_data_refresh_is_active = True
            try:
                return func(self, *args, **kwargs)
            finally:
                self.clip_data_refresh_is_active = False
        return inner

    def build_widget_ctx_menu(self, action_list, *args, **kwargs):
        return ui_utils.build_menu_from_action_list(action_list)

    def build_clip_list_ctx_menu(self):
        action_list = [
            {"Assign Random Color": self.set_random_clip_color},
            {"Rename Clip": self.rename_selected_clip},
            {"Delete Clip(s)": self.delete_selected_clips},
            {"Re-Project Mocap Control under Hips": self.reproject_mocap_control_under_hips},
            {"Re-Project Root Joint Anim from Hips": self.project_root_animation_from_hips},
        ]
        ui_utils.build_menu_from_action_list(action_list)

    def rename_selected_clip(self):
        cd = self.get_active_clip_data()
        if not cd:
            return
        rename_success = mcs.dcc.rename_clip(cd.node)
        if rename_success:
            self.ui_refresh_from_scene()

    def set_random_clip_color(self):
        for cd in self.get_selected_clip_data():  # type: k.ClipData
            mcs.dcc.set_random_color_on_clip(cd.node)
        self.ui_refresh_from_scene()

    def delete_selected_clips(self):
        # find all namespaces used by each clip node
        namespace_usage = defaultdict(list)
        for cd in self.scene_data.values():  # type: k.ClipData
            namespace_usage[cd.namespace].append(cd.node)

        mcs.dcc.delete_clips(
            self.get_selected_clip_data(),
            namespace_usage,
        )

        self.ui_refresh_from_scene()

    @deco_disable_clip_data_set_signals
    def ui_refresh_from_project(self):
        self.ui.start_pose_CB.clear()
        self.ui.end_pose_CB.clear()

        pose_files = mcs.dcc.get_pose_files()

        for pose_file in pose_files:
            pose_icon = mcs.dcc.get_pose_icon(pose_file) or QtGui.QIcon()
            pose_name = os.path.splitext(os.path.basename(pose_file))[0]
            self.ui.start_pose_CB.addItem(pose_icon, pose_name, pose_file)
            self.ui.end_pose_CB.addItem(pose_icon, pose_name, pose_file)

    def ui_refresh_from_scene(self):
        self.scene_data = mcs.dcc.get_scene_time_editor_data()
        log.debug("Scene data refresh: {}".format(self.scene_data))

        clip_icon = mcs.dcc.get_clip_icon() or None

        # update clip list
        self.ui.clips_LW.clear()
        for clip_name, clip_data in self.scene_data.items():  # type: str, k.ClipData
            lw = QtWidgets.QListWidgetItem()
            lw.setText(clip_name)
            lw.setIcon(clip_icon)

            # background color
            if clip_data.clip_color:
                rgb_color = QtGui.QColor(*[x * 256 for x in clip_data.clip_color])
                lw.setBackgroundColor(rgb_color)

            # text color
            lw.setForeground(QtGui.QColor(0, 0, 0))

            # font styling
            f = lw.font() # type: QtGui.QFont
            f.setItalic(True)
            lw.setFont(f)

            self.ui.clips_LW.addItem(lw)

        # update actor list
        rig_names = mcs.dcc.get_rigs_in_scene().keys()
        rig_icon = mcs.dcc.get_rig_icon() or QtGui.QIcon()
        self.ui.scene_actor_CB.clear()
        for rig_name in rig_names:
            self.ui.scene_actor_CB.addItem(rig_icon, rig_name)

    @deco_disable_clip_data_set_signals
    def ui_update_clip_display_info(self):
        selected_clips = self.ui.clips_LW.selectedItems()

        valid_selection = False
        if len(selected_clips) == 1:
            clip_lwi = selected_clips[0]  # type: QtWidgets.QListWidgetItem
            clip_name = clip_lwi.text()
            active_cd = self.scene_data.get(clip_name)
            valid_selection = True

        elif len(selected_clips) > 1:
            clip_name = "[Multiple Clips Selected]"
            active_cd = k.ClipData()
            valid_selection = True
        else:
            clip_name = ""
            active_cd = k.ClipData()
            self.ui.start_pose_CHK.setChecked(False)
            self.ui.end_pose_CHK.setChecked(False)
            self.ui.end_pose_same_CHK.setChecked(False)
            log.debug("No clips found in selection, resetting data")

        if not active_cd:
            log.warning("Clip data could not be extracted from UI, exiting UI update early")
            return

        self.ui.clip_name_LE.setText(clip_name)
        self.ui.frame_start.setText(str(active_cd.start_frame))
        self.ui.frame_end.setText(str(active_cd.end_frame))
        self.ui.frame_duration.setText(str(active_cd.frame_duration))

        clip_node = active_cd.node
        if clip_node:
            log.debug("Parsing data from: {}".format(clip_node))

            mcs.dcc.select_node(clip_node)

            self.ui.start_pose_CHK.setChecked(active_cd.start_pose_enabled)
            self.ui.end_pose_CHK.setChecked(active_cd.end_pose_enabled)
            self.ui.end_pose_same_CHK.setChecked(active_cd.end_pose_same_as_start)

            if active_cd.start_pose_path:
                ui_utils.set_combo_box_by_data(self.ui.start_pose_CB, active_cd.start_pose_path)

            if active_cd.end_pose_path:
                ui_utils.set_combo_box_by_data(self.ui.end_pose_CB, active_cd.end_pose_path)

            if active_cd.end_pose_match_method:
                ui_utils.set_combo_box_by_text(self.ui.end_pose_match_method_CB, active_cd.end_pose_match_method)

        if valid_selection:
            self.ui.bake_BTN.setStyleSheet("background-color:rgb(80, 120, 80)")

            # hide all other mocap skeletons in the scene
            namespaces_to_show = []
            for clip_lwi in ui_utils.get_list_widget_items(self.ui.clips_LW):
                cd = self.scene_data.get(clip_lwi.text())  # type: k.ClipData
                if not cd:
                    continue

                if clip_lwi in selected_clips:
                    namespaces_to_show.append(cd.namespace)

                mcs.dcc.set_mocap_visibility(cd.namespace, False)

            # re-enable the selected mocap
            [mcs.dcc.set_mocap_visibility(ns, True) for ns in namespaces_to_show]

        else:
            self.ui.bake_BTN.setStyleSheet("background-color:rgb(80, 80, 80)")

        self.ui.reproject_mocap_ctrl_BTN.setEnabled(valid_selection)
        self.ui.reproject_root_anim_BTN.setEnabled(valid_selection)
        self.ui.align_root_to_rig_BTN.setEnabled(valid_selection)
        self.ui.align_root_to_origin_BTN.setEnabled(valid_selection)
        self.ui.toggle_root_aim_BTN.setEnabled(valid_selection)

    def get_active_clip_data(self):
        """

        Returns: k.ClipData

        """
        selected_clips = self.ui.clips_LW.selectedItems()
        if selected_clips:
            clip_lw = selected_clips[0]  # type: QtWidgets.QListWidgetItem
            clip_name = clip_lw.text()

            cd = self.scene_data.get(clip_name)  # type: k.ClipData

            return cd

    def get_selected_clip_data(self):
        """

        Returns: [k.ClipData]

        """
        selected_clips = self.ui.clips_LW.selectedItems()
        sel_clip_data = []
        for clip_lwi in selected_clips:
            clip_name = clip_lwi.text()
            clip_data = self.scene_data.get(clip_name)  # type: k.ClipData
            sel_clip_data.append(clip_data)
        return sel_clip_data

    def set_active_clip_data(self):
        """
        Apply UI data to scene node
        """
        if self.clip_data_refresh_is_active:
            return

        selected_clips = self.ui.clips_LW.selectedItems()
        if not selected_clips or len(selected_clips) > 1:
            return

        clip_lw = selected_clips[0]
        clip_name = clip_lw.text()
        cd = self.scene_data.get(clip_name)  # type: k.ClipData

        cd.start_pose_path = self.ui.start_pose_CB.currentData(QtCore.Qt.UserRole)
        cd.start_pose_enabled = self.ui.start_pose_CHK.isChecked()
        cd.end_pose_path = self.ui.end_pose_CB.currentData(QtCore.Qt.UserRole)
        cd.end_pose_enabled = self.ui.end_pose_CHK.isChecked()
        cd.end_pose_same_as_start = self.ui.end_pose_same_CHK.isChecked()
        cd.end_pose_match_method = self.ui.end_pose_match_method_CB.currentText()

        if cd.end_pose_enabled:
            if cd.end_pose_same_as_start:
                self.match_end_pose_to_start()

        cd_dict = cd.to_dict()
        clip_data_str = json.dumps(cd_dict)
        mcs.dcc.set_attr(cd.node, k.SceneConstants.mocap_clipper_data, clip_data_str)

    def get_active_rig(self):
        return self.ui.scene_actor_CB.currentText()

    def toggle_mocap_constraint(self):
        if self.mocap_connect_result:
            self.disconnect_mocap_from_rig()
            self.mocap_connect_result = None

            # update UI display
            self.ui.connect_mocap_to_rig_BTN.setText("Preview Mocap On Rig")
            self.ui.connect_mocap_to_rig_BTN.setStyleSheet("")
            self.ui.bake_BTN.setEnabled(True)
        else:
            if self.connect_mocap_to_rig():
                self.ui.connect_mocap_to_rig_BTN.setText("Detach from Mocap")
                self.ui.connect_mocap_to_rig_BTN.setStyleSheet("background-color:rgb(150, 100, 80)")
                self.ui.bake_BTN.setEnabled(False)

    def match_end_pose_to_start(self):
        if not self.ui.end_pose_same_CHK.isChecked():
            return
        start_pose_path = self.ui.start_pose_CB.currentData(QtCore.Qt.UserRole)
        ui_utils.set_combo_box_by_data(self.ui.end_pose_CB, start_pose_path)

    def connect_mocap_to_rig(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            log.warning("No Mocap found in selection")
            return

        rig_name = self.get_active_rig()

        self.mocap_connect_result = mcs.dcc.connect_mocap_to_rig(
            mocap_ns=clip_data.namespace,
            rig_name=rig_name
        )

        return True

    def disconnect_mocap_from_rig(self):
        mcs.dcc.disconnect_mocap_from_rig(self.mocap_connect_result)

    def import_mocap(self):
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(caption="Choose .FBX file(s)", filter="FBX (*.fbx)")
        if not file_paths:
            return
        for file_path in file_paths:
            mcs.dcc.import_mocap(file_path)

        self.ui_refresh_from_scene()

    def bake_to_rig(self):
        active_clip_data = self.get_active_clip_data()
        if not active_clip_data:
            log.warning("Clip not found in selection")
            return

        if not active_clip_data.namespace:
            log.warning("Could not find namespace of driven objects of clip.")
            return

        # Gather bake configuration from the current UI settings
        bake_config = k.BakeConfig()
        bake_config.align_mocap_to_pose = self.ui.align_mocap_CHK.isChecked()
        bake_config.align_mocap_to_start_pose = self.ui.align_to_start_pose_RB.isChecked()
        bake_config.align_mocap_to_end_pose = self.ui.align_to_end_pose_RB.isChecked()
        bake_config.mocap_alignment_name = self.ui.align_mocap_CB.currentText()

        bake_config.run_euler_filter = self.ui.euler_filter_CHK.isChecked()
        bake_config.set_time_range = self.ui.set_time_range_CHK.isChecked()
        bake_config.run_adjustment_blend = self.ui.adjustment_blend_CHK.isChecked()
        bake_config.save_clip = self.ui.save_clip_CHK.isChecked()

        bake_config.target_rig = self.get_active_rig()
        bake_config.output_folder = self.ui.output_path_W.path()

        try:
            # set window to semi-transparent while it's working
            self.window().setWindowOpacity(0.6)

            # run bake on all selected clips
            for clip_lw in self.ui.clips_LW.selectedItems():  # type: QtWidgets.QListWidgetItem
                clip_name = clip_lw.text()
                clip_data = self.scene_data.get(clip_name)  # type: k.ClipData
                mcs.dcc.main_bake_function(clip_data, bake_config)

            mcs.dcc.post_all_clips_bake()

        finally:
            self.window().setWindowOpacity(1.0)

    def apply_start_pose(self):
        start_pose_path = self.ui.start_pose_CB.currentData(QtCore.Qt.UserRole)
        mcs.dcc.apply_pose(start_pose_path, rig_name=self.get_active_rig())

    def apply_end_pose(self):
        end_pose_path = self.ui.end_pose_CB.currentData(QtCore.Qt.UserRole)
        mcs.dcc.apply_pose(end_pose_path, rig_name=self.get_active_rig())

    def project_root_animation_from_hips(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            log.warning("Clip not found in selection")
            return
        mcs.dcc.project_root_animation_from_hips(clip_data.namespace)

    def reproject_mocap_control_under_hips(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            return
        mcs.dcc.project_mocap_ctrl_to_ground_under_hips(clip_data.namespace)

    def align_mocap_with_rig(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            log.warning("Clip not found in selection")
            return

        rig_name = self.get_active_rig()
        mcs.dcc.align_mocap_to_rig(
            clip_data.namespace,
            rig_name,
            alignment_name=self.ui.align_mocap_CB.currentText(),
        )

    def align_mocap_to_world_origin(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            log.warning("Clip not found in selection")
            return

        mcs.dcc.align_mocap_to_world_origin(
            clip_data.namespace,
            alignment_name=self.ui.align_mocap_CB.currentText(),
        )

    def toggle_root_aim(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            log.warning("Clip not found in selection")
            return
        mcs.dcc.toggle_root_aim(clip_data.namespace)

    def set_time_range(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            log.warning("Clip not found in selection")
            return
        mcs.dcc.set_time_range(
            (clip_data.start_frame, clip_data.end_frame),
        )


def main(refresh=False):
    log.debug("Main function triggered")

    win = MocapClipperWindow()
    win.main(refresh=refresh)

    if standalone_app:
        ui_utils.standalone_app_window = win
        sys.exit(standalone_app.exec_())

    return win


if __name__ == "__main__":
    main()
