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
        main_ui_widget = QtWidgets.QWidget()
        self.ui.setupUi(main_ui_widget)
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

        # Menu bar
        menu_bar = QtWidgets.QMenuBar()
        ui_utils.build_log_level_menu(menu_bar, log_cls=log)
        self.setMenuBar(menu_bar)

    def set_ui_from_dcc_settings(self):
        # set icons
        mocap_icon = mcs.dcc.get_mocap_icon() or QtGui.QIcon()
        refresh_icon = QtGui.QIcon(resources.get_image_path("refresh_icon"))
        self.ui.refresh_BTN.setIcon(refresh_icon)
        self.ui.refresh_project_BTN.setIcon(refresh_icon)
        self.ui.import_mocap_BTN.setIcon(mocap_icon)
        self.ui.bake_BTN.setIcon(mocap_icon)

        # add project specfic alignment joints
        alignment_options = mcs.dcc.get_alignment_joint_names()
        self.ui.align_mocap_CB.addItems(alignment_options)

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
        # connect UI
        self.ui.import_mocap_BTN.clicked.connect(self.import_mocap)
        self.ui.refresh_BTN.clicked.connect(self.ui_refresh_from_scene)
        self.ui.refresh_project_BTN.clicked.connect(self.ui_refresh_from_project)
        self.ui.clips_LW.itemSelectionChanged.connect(self.ui_update_clip_display_info)

        self.ui.clips_LW.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.clips_LW.customContextMenuRequested.connect(self.build_clip_list_ctx_menu)

        self.ui.rename_clip_BTN.clicked.connect(self.rename_selected_clip)
        self.ui.end_pose_CHK.stateChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_CHK.stateChanged.connect(self.ui.end_pose_CB.setEnabled)
        self.ui.end_pose_CB.currentIndexChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_same_CHK.stateChanged.connect(self.set_active_clip_data)
        self.ui.start_pose_CHK.stateChanged.connect(self.set_active_clip_data)
        self.ui.start_pose_CHK.stateChanged.connect(self.ui.start_pose_CB.setEnabled)
        self.ui.start_pose_CB.currentIndexChanged.connect(self.match_end_pose_to_start)
        self.ui.start_pose_CB.currentIndexChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_CB.currentIndexChanged.connect(self.set_active_clip_data)

        self.ui.reproject_root_anim_BTN.clicked.connect(self.project_root_animation_from_hips)
        self.ui.reproject_mocap_ctrl_BTN.clicked.connect(self.reproject_mocap_control_under_hips)
        self.ui.align_root_to_rig_BTN.clicked.connect(self.align_mocap_with_rig)
        self.ui.toggle_root_aim_BTN.clicked.connect(self.toggle_root_aim)

        self.ui.align_mocap_CHK.stateChanged.connect(self.ui.align_to_start_pose_RB.setEnabled)
        self.ui.align_mocap_CHK.stateChanged.connect(self.ui.align_to_end_pose_RB.setEnabled)

        self.ui.save_clip_CHK.stateChanged.connect(self.ui.output_path_W.setEnabled)

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
            {"Rename Clip": self.rename_selected_clip},
            {"Delete Clip(s)": self.delete_selected_clips},
            {"Re-Project Mocap Control under Hips": self.reproject_mocap_control_under_hips},
            {"Re-Project Root Joint Anim from Hips": self.project_root_animation_from_hips},
        ]
        ui_utils.build_menu_from_action_list(action_list)

    def rename_selected_clip(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            return

        clip_node = clip_data.get(k.cdc.node)
        rename_success = mcs.dcc.rename_clip(clip_node)
        if rename_success:
            self.ui_refresh_from_scene()

    def delete_selected_clips(self):
        # find all namespaces used by each clip node
        namespace_usage = defaultdict(list)
        for scene_clip_data in self.scene_data.values():  # type: dict
            clip_ns = scene_clip_data.get(k.cdc.namespace)
            clip_node = scene_clip_data.get(k.cdc.node)
            namespace_usage[clip_ns].append(clip_node)

        selected_clip_data = self.get_selected_clip_data()  # type: list

        mcs.dcc.delete_clips(selected_clip_data, namespace_usage)

        self.ui_refresh_from_scene()

    @deco_disable_clip_data_set_signals
    def ui_refresh_from_project(self):
        self.ui.start_pose_CB.clear()
        self.ui.end_pose_CB.clear()

        pose_files = mcs.dcc.get_pose_files()
        pose_icon = mcs.dcc.get_pose_icon() or QtGui.QIcon()

        for pose_file in pose_files:
            pose_name = os.path.splitext(os.path.basename(pose_file))[0]
            self.ui.start_pose_CB.addItem(pose_icon, pose_name, pose_file)
            self.ui.end_pose_CB.addItem(pose_icon, pose_name, pose_file)

    def ui_refresh_from_scene(self):
        self.scene_data = mcs.dcc.get_scene_time_editor_data()
        log.debug("Scene data refresh: {}".format(self.scene_data))

        clip_icon = mcs.dcc.get_clip_icon() or None

        # update clip list
        self.ui.clips_LW.clear()
        for clip_name in self.scene_data.keys():
            lw = QtWidgets.QListWidgetItem()
            lw.setText(clip_name)
            lw.setIcon(clip_icon)
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
            active_clip_data = self.scene_data.get(clip_name)
            valid_selection = True

        elif len(selected_clips) > 1:
            clip_name = "[Multiple Clips Selected]"
            active_clip_data = dict()
            active_clip_data[k.cdc.start_frame] = ""
            active_clip_data[k.cdc.end_frame] = ""
            active_clip_data[k.cdc.frame_duration] = ""
            valid_selection = True
        else:
            clip_name = ""
            active_clip_data = dict()
            active_clip_data[k.cdc.start_frame] = ""
            active_clip_data[k.cdc.end_frame] = ""
            active_clip_data[k.cdc.frame_duration] = ""
            self.ui.start_pose_CHK.setChecked(False)
            self.ui.end_pose_CHK.setChecked(False)
            self.ui.end_pose_same_CHK.setChecked(False)
            log.debug("No clips found in selection, resetting data")

        if not active_clip_data:
            log.warning("Clip data could not be extracted from UI, exiting UI update early")
            return

        self.ui.clip_name_LE.setText(clip_name)
        self.ui.frame_start.setText(str(active_clip_data.get(k.cdc.start_frame)))
        self.ui.frame_end.setText(str(active_clip_data.get(k.cdc.end_frame)))
        self.ui.frame_duration.setText(str(active_clip_data.get(k.cdc.frame_duration)))

        clip_node = active_clip_data.get(k.cdc.node)
        if clip_node:
            log.debug("Parsing data from: {}".format(clip_node))

            mcs.dcc.select_node(clip_node)

            self.ui.start_pose_CHK.setChecked(active_clip_data.get(k.cdc.start_pose_enabled))
            self.ui.end_pose_CHK.setChecked(active_clip_data.get(k.cdc.end_pose_enabled))
            self.ui.end_pose_same_CHK.setChecked(active_clip_data.get(k.cdc.end_pose_same_as_start))

            start_pose_path = active_clip_data.get(k.cdc.start_pose_path)
            end_pose_path = active_clip_data.get(k.cdc.end_pose_path)

            if start_pose_path:
                ui_utils.set_combo_box_by_data(self.ui.start_pose_CB, start_pose_path)

            if end_pose_path:
                ui_utils.set_combo_box_by_data(self.ui.end_pose_CB, end_pose_path)

        if valid_selection:
            self.ui.bake_BTN.setStyleSheet("background-color:rgb(80, 120, 80)")

            # hide all other mocap skeletons in the scene
            namespaces_to_show = []
            for clip_lwi in ui_utils.get_list_widget_items(self.ui.clips_LW):
                clip_data = self.scene_data.get(clip_lwi.text())
                if not clip_data:
                    continue

                mocap_namespace = clip_data.get(k.cdc.namespace)
                if clip_lwi in selected_clips:
                    namespaces_to_show.append(mocap_namespace)

                mcs.dcc.set_mocap_visibility(mocap_namespace, False)

            # re-enable the selected mocap
            [mcs.dcc.set_mocap_visibility(ns, True) for ns in namespaces_to_show]

        else:
            self.ui.bake_BTN.setStyleSheet("background-color:rgb(80, 80, 80)")

        self.ui.reproject_mocap_ctrl_BTN.setEnabled(valid_selection)
        self.ui.reproject_root_anim_BTN.setEnabled(valid_selection)
        self.ui.align_root_to_rig_BTN.setEnabled(valid_selection)
        self.ui.toggle_root_aim_BTN.setEnabled(valid_selection)

    def get_active_clip_data(self):
        selected_clips = self.ui.clips_LW.selectedItems()
        if selected_clips:
            clip_lw = selected_clips[0]  # type: QtWidgets.QListWidgetItem
            clip_name = clip_lw.text()
            clip_data = self.scene_data.get(clip_name)

            # update from UI if only one clip is selected
            if len(selected_clips) == 1:
                clip_data[k.cdc.start_frame] = float(self.ui.frame_start.text())
                clip_data[k.cdc.end_frame] = float(self.ui.frame_end.text())
            clip_data[k.cdc.target_rig] = self.get_active_rig()

            return clip_data

    def get_selected_clip_data(self):
        selected_clips = self.ui.clips_LW.selectedItems()
        sel_clip_data = []
        for clip_lwi in selected_clips:
            clip_name = clip_lwi.text()
            clip_data = self.scene_data.get(clip_name)
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
        clip_data = self.scene_data.get(clip_name)
        clip_node = clip_data.get(k.cdc.node)

        start_pose_path = self.ui.start_pose_CB.currentData(QtCore.Qt.UserRole)
        start_pose_enabled = self.ui.start_pose_CHK.isChecked()
        end_pose_path = self.ui.end_pose_CB.currentData(QtCore.Qt.UserRole)
        end_pose_enabled = self.ui.end_pose_CHK.isChecked()
        end_pose_same_as_start = self.ui.end_pose_same_CHK.isChecked()

        mcs.dcc.set_attr(clip_node, k.cdc.start_pose_enabled, start_pose_enabled)
        mcs.dcc.set_attr(clip_node, k.cdc.end_pose_enabled, end_pose_enabled)
        mcs.dcc.set_attr(clip_node, k.cdc.end_pose_same_as_start, end_pose_same_as_start)

        if start_pose_enabled:
            mcs.dcc.set_attr(clip_node, k.cdc.start_pose_path, start_pose_path)
            clip_data[k.cdc.start_pose_path] = start_pose_path

        if end_pose_enabled:
            if end_pose_same_as_start:
                end_pose_path = start_pose_path
                self.match_end_pose_to_start()
            mcs.dcc.set_attr(clip_node, k.cdc.end_pose_path, end_pose_path)
            clip_data[k.cdc.end_pose_path] = end_pose_path

        # set internal clip data for this clip
        clip_data[k.cdc.start_pose_enabled] = start_pose_enabled
        clip_data[k.cdc.end_pose_enabled] = end_pose_enabled
        clip_data[k.cdc.end_pose_same_as_start] = end_pose_same_as_start

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
            mocap_ns=clip_data.get(k.cdc.namespace),
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
            clip_name = os.path.splitext(os.path.basename(file_path))[0]

            mocap_nodes = mcs.dcc.import_mocap(file_path)
            mcs.dcc.create_time_editor_clip(mocap_nodes, clip_name)

        self.ui_refresh_from_scene()

    def bake_to_rig(self):
        active_clip_data = self.get_active_clip_data()
        if not active_clip_data:
            log.warning("Clip not found in selection")
            return

        mocap_namespace = active_clip_data.get(k.cdc.namespace)
        if not mocap_namespace:
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

        # run bake on all selected clips
        for clip_lw in self.ui.clips_LW.selectedItems():  # type: QtWidgets.QListWidgetItem
            clip_name = clip_lw.text()
            clip_data = self.scene_data.get(clip_name)

            clip_data[k.cdc.target_rig] = self.get_active_rig()
            clip_data[k.cdc.output_folder] = self.ui.output_path_W.path()

            mcs.dcc.main_bake_function(clip_data, bake_config)

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
        mocap_namespace = clip_data.get(k.cdc.namespace)
        mcs.dcc.project_root_animation_from_hips(mocap_namespace)

    def reproject_mocap_control_under_hips(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            return
        mocap_namespace = clip_data.get(k.cdc.namespace)
        mcs.dcc.project_mocap_ctrl_to_ground_under_hips(mocap_namespace)

    def align_mocap_with_rig(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            log.warning("Clip not found in selection")
            return
        mocap_namespace = clip_data.get(k.cdc.namespace)
        rig_name = self.get_active_rig()
        mcs.dcc.align_mocap_to_rig(
            mocap_namespace,
            rig_name,
            alignment_name=self.ui.align_mocap_CB.currentText(),
        )

    def toggle_root_aim(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            log.warning("Clip not found in selection")
            return
        mocap_namespace = clip_data.get(k.cdc.namespace)
        mcs.dcc.toggle_root_aim(mocap_namespace)

    def set_time_range(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            log.warning("Clip not found in selection")
            return
        mcs.dcc.set_time_range((
            clip_data.get(k.cdc.start_frame),
            clip_data.get(k.cdc.end_frame),
        ))


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
