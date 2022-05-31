import os.path
import sys
from functools import partial, wraps

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
        self.update_from_project()
        self.update_from_scene()
        self.ui.refresh_BTN.setIcon(QtGui.QIcon(resources.get_image_path("refresh_icon")))
        mocap_icon = mcs.dcc.get_mocap_icon() or QtGui.QIcon()
        rig_icon = mcs.dcc.get_rig_icon() or QtGui.QIcon()
        self.ui.import_mocap_BTN.setIcon(mocap_icon)
        self.ui.bake_BTN.setIcon(mocap_icon)

        # set output folder
        self.ui.output_path_W.path_dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        default_project_folder = mcs.dcc.get_default_output_folder()
        if not self.ui.output_path_W.path() and default_project_folder:
            self.ui.output_path_W.set_path(default_project_folder)

        # connect UI
        self.ui.import_mocap_BTN.clicked.connect(self.import_mocap)
        self.ui.refresh_BTN.clicked.connect(self.update_from_scene)
        self.ui.clips_LW.itemSelectionChanged.connect(self.update_clip_display_info)

        self.ui.clips_LW.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.clips_LW.customContextMenuRequested.connect(self.build_clip_list_ctx_menu)

        self.ui.rename_clip_BTN.clicked.connect(self.rename_selected_clip)
        self.ui.end_pose_CHK.stateChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_CB.currentIndexChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_same_CHK.stateChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_same_CHK.stateChanged.connect(self.ui.end_pose_CB.setDisabled)
        self.ui.start_pose_CHK.stateChanged.connect(self.set_active_clip_data)
        self.ui.start_pose_CHK.stateChanged.connect(self.ui.start_pose_CB.setEnabled)
        self.ui.start_pose_CB.currentIndexChanged.connect(self.match_end_pose_to_start)
        self.ui.start_pose_CB.currentIndexChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_CB.currentIndexChanged.connect(self.set_active_clip_data)

        self.ui.align_mocap_CHK.stateChanged.connect(self.ui.align_to_start_pose_RB.setEnabled)
        self.ui.align_mocap_CHK.stateChanged.connect(self.ui.align_to_end_pose_RB.setEnabled)

        self.ui.save_clip_CHK.stateChanged.connect(self.ui.output_path_W.setEnabled)

        self.ui.connect_mocap_to_rig_BTN.clicked.connect(self.toggle_mocap_constraint)
        self.ui.bake_BTN.clicked.connect(self.bake_to_rig)

        # right click menus
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

        # Menu bar
        menu_bar = QtWidgets.QMenuBar()
        ui_utils.build_log_level_menu(menu_bar, log_cls=log)
        self.setMenuBar(menu_bar)

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
            {"Rename Clip": self.rename_selected_clip}
        ]
        ui_utils.build_menu_from_action_list(action_list)

    def rename_selected_clip(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            return

        clip_node = clip_data.get(k.cdc.node)
        rename_success = mcs.dcc.rename_clip(clip_node)
        if rename_success:
            self.update_from_scene()

    def update_from_project(self):
        pose_files = mcs.dcc.get_pose_files()
        pose_icon = mcs.dcc.get_pose_icon() or QtGui.QIcon()
        for pose_file in pose_files:
            pose_name = os.path.splitext(os.path.basename(pose_file))[0]
            self.ui.start_pose_CB.addItem(pose_icon, pose_name, pose_file)
            self.ui.end_pose_CB.addItem(pose_icon, pose_name, pose_file)

        for project_settings_widget in mcs.dcc.get_project_settings_widgets():
            self.ui.project_settings_layout.addWidget(project_settings_widget)

        for project_action_widget in mcs.dcc.get_project_action_widgets():
            self.ui.project_widgets_layout.addWidget(project_action_widget)

    def update_from_scene(self):
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
    def update_clip_display_info(self):
        selected_clips = self.ui.clips_LW.selectedItems()

        valid_selection = False
        if len(selected_clips) == 1:
            clip_lwi = selected_clips[0]  # type: QtWidgets.QListWidgetItem
            clip_name = clip_lwi.text()
            clip_data = self.scene_data.get(clip_name)
            valid_selection = True

        elif len(selected_clips) > 1:
            all_clip_data = []
            for clip_lwi in selected_clips:
                clip_name = clip_lwi.text()
                all_clip_data.append(self.scene_data.get(clip_name))

            smallest_start_frame = min([cd.get(k.cdc.start_frame) for cd in all_clip_data])
            highest_start_frame = max([cd.get(k.cdc.end_frame) for cd in all_clip_data])

            clip_name = "[Multiple Clips Selected]"
            clip_data = dict()
            clip_data[k.cdc.start_frame] = smallest_start_frame
            clip_data[k.cdc.end_frame] = highest_start_frame
            clip_data[k.cdc.frame_duration] = highest_start_frame - smallest_start_frame
            valid_selection = True

        else:
            clip_name = ""
            clip_data = dict()
            clip_data[k.cdc.start_frame] = ""
            clip_data[k.cdc.end_frame] = ""
            clip_data[k.cdc.frame_duration] = ""
            self.ui.start_pose_CHK.setChecked(False)
            self.ui.end_pose_CHK.setChecked(False)
            self.ui.end_pose_same_CHK.setChecked(True)
            log.debug("No clips found in selection, resetting data")

        self.ui.clip_name_LE.setText(clip_name)
        self.ui.frame_start.setText(str(clip_data.get(k.cdc.start_frame)))
        self.ui.frame_end.setText(str(clip_data.get(k.cdc.end_frame)))
        self.ui.frame_duration.setText(str(clip_data.get(k.cdc.frame_duration)))

        clip_node = clip_data.get(k.cdc.node)
        if clip_node:
            log.debug("Parsing data from: {}".format(clip_node))

            mcs.dcc.select_node(clip_node)

            self.ui.start_pose_CHK.setChecked(clip_data.get(k.cdc.start_pose_enabled))
            self.ui.end_pose_CHK.setChecked(clip_data.get(k.cdc.end_pose_enabled))
            self.ui.end_pose_same_CHK.setChecked(clip_data.get(k.cdc.end_pose_same_as_start))

            start_pose_path = clip_data.get(k.cdc.start_pose_path)
            end_pose_path = clip_data.get(k.cdc.end_pose_path)

            if start_pose_path:
                ui_utils.set_combo_box_by_data(self.ui.start_pose_CB, start_pose_path)

            if end_pose_path:
                ui_utils.set_combo_box_by_data(self.ui.end_pose_CB, end_pose_path)

        if valid_selection:
            self.ui.bake_BTN.setStyleSheet("background-color:rgb(80, 120, 80)")
        else:
            self.ui.bake_BTN.setStyleSheet("background-color:rgb(80, 80, 80)")

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
            mcs.dcc.import_mocap(file_path)
        self.update_from_scene()

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

    def align_mocap_with_rig(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            log.warning("Clip not found in selection")
            return
        mocap_namespace = clip_data.get(k.cdc.namespace)
        rig_name = self.get_active_rig()
        mcs.dcc.align_mocap_to_rig(mocap_namespace, rig_name)

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
