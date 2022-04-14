import os.path
import sys
from functools import partial

from . import mocap_clipper_constants as k
from . import mocap_clipper_system as mcs
from . import resources
from . import ui_utils
from .ui import mocap_clipper_widget
from .ui_utils import QtCore, QtWidgets, QtGui

standalone_app = None
if not QtWidgets.QApplication.instance():
    standalone_app = QtWidgets.QApplication(sys.argv)


class MocapClipperWindow(ui_utils.ToolWindow):
    def __init__(self):
        super(MocapClipperWindow, self).__init__()

        self.ui = mocap_clipper_widget.Ui_MocapClipperWidget()
        main_ui_widget = QtWidgets.QWidget()
        self.ui.setupUi(main_ui_widget)
        self.setCentralWidget(main_ui_widget)
        self.setWindowTitle("Mocap Clipper")
        self.setWindowIcon(QtGui.QIcon(resources.get_image_path("mocap_clipper_icon")))

        mcs.dcc.tool_window = self

        self.mocap_bind_result = None

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

        # connect UI
        self.ui.import_mocap_BTN.clicked.connect(self.import_mocap)
        self.ui.refresh_BTN.clicked.connect(self.update_from_scene)
        self.ui.clips_LW.itemSelectionChanged.connect(self.update_clip_display_info)

        self.ui.end_pose_CHK.stateChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_CB.currentIndexChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_same_CHK.stateChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_same_CHK.stateChanged.connect(self.ui.end_pose_CB.setDisabled)
        self.ui.start_pose_CHK.stateChanged.connect(self.set_active_clip_data)
        self.ui.start_pose_CHK.stateChanged.connect(self.ui.start_pose_CB.setEnabled)
        self.ui.start_pose_CB.currentIndexChanged.connect(self.match_end_pose_to_start)
        self.ui.start_pose_CB.currentIndexChanged.connect(self.set_active_clip_data)
        self.ui.end_pose_CB.currentIndexChanged.connect(self.set_active_clip_data)

        self.ui.connect_mocap_to_rig_BTN.clicked.connect(self.toggle_mocap_constraint)
        self.ui.bake_BTN.clicked.connect(self.bake_to_rig)

        # right click menus
        widget_run_actions = {
            self.ui.start_pose_CB: self.apply_start_pose,
            self.ui.start_pose_CHK: self.apply_start_pose,
            self.ui.end_pose_CB: self.apply_end_pose,
            self.ui.end_pose_CHK: self.apply_end_pose,
            self.ui.end_pose_same_CHK: self.apply_end_pose,
            self.ui.align_to_start_pose_CHK: self.align_mocap_with_rig,
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

    def build_widget_ctx_menu(self, action_list, *args, **kwargs):
        return ui_utils.build_menu_from_action_list(action_list)

    def update_from_project(self):
        pose_files = mcs.dcc.get_pose_files()
        pose_icon = mcs.dcc.get_pose_icon() or QtGui.QIcon()
        for pose_file in pose_files:
            pose_name = os.path.splitext(os.path.basename(pose_file))[0]
            self.ui.start_pose_CB.addItem(pose_icon, pose_name, pose_file)
            self.ui.end_pose_CB.addItem(pose_icon, pose_name, pose_file)

        for project_settings_widget in mcs.dcc.get_project_settings_widgets():
            self.ui.project_settings_layout.addWidget(project_settings_widget)

        for project_widget in mcs.dcc.get_project_widgets():
            self.ui.project_widgets_layout.addWidget(project_widget)

    def update_from_scene(self):
        self.scene_data = mcs.dcc.get_scene_time_editor_data()

        # update clip list
        self.ui.clips_LW.clear()
        for clip_name in self.scene_data.keys():
            lw = QtWidgets.QListWidgetItem()
            lw.setText(clip_name)
            self.ui.clips_LW.addItem(lw)

        # update actor list
        rig_names = mcs.dcc.get_rigs_in_scene().keys()
        rig_icon = mcs.dcc.get_rig_icon() or QtGui.QIcon()
        self.ui.scene_actor_CB.clear()
        for rig_name in rig_names:
            self.ui.scene_actor_CB.addItem(rig_icon, rig_name)

    def update_clip_display_info(self):
        selected_clips = self.ui.clips_LW.selectedItems()

        valid_selection = False
        if len(selected_clips) == 1:
            clip_lw = selected_clips[0]  # type: QtWidgets.QListWidgetItem
            clip_name = clip_lw.text()
            clip_data = self.scene_data.get(clip_name)
            valid_selection = True

        elif len(selected_clips) > 1:
            clip_name = "[Multiple Clips Selected]"
            clip_data = dict()
            clip_data[k.cdc.start_frame] = "[...]"
            clip_data[k.cdc.end_frame] = "[...]"
            clip_data[k.cdc.frame_duration] = "[...]"
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

        self.ui.clip_name_LE.setText(clip_name)
        self.ui.frame_start.setText(str(clip_data.get(k.cdc.start_frame)))
        self.ui.frame_end.setText(str(clip_data.get(k.cdc.end_frame)))
        self.ui.frame_duration.setText(str(clip_data.get(k.cdc.frame_duration)))

        clip_node = clip_data.get(k.cdc.node)
        if clip_node:
            mcs.dcc.select_node(clip_node)
            start_pose_enabled = mcs.dcc.get_attr(clip_node, "start_pose_enabled", default=False)
            start_pose_path = mcs.dcc.get_attr(clip_node, "start_pose_path")
            end_pose_enabled = mcs.dcc.get_attr(clip_node, "end_pose_enabled", default=False)
            end_pose_path = mcs.dcc.get_attr(clip_node, "end_pose_path")
            end_pose_same_as_start = mcs.dcc.get_attr(clip_node, "end_pose_same_as_start", default=True)

            self.ui.start_pose_CHK.setChecked(start_pose_enabled)
            self.ui.end_pose_CHK.setChecked(end_pose_enabled)
            self.ui.end_pose_same_CHK.setChecked(end_pose_same_as_start)

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

            return clip_data

    def set_active_clip_data(self):
        """
        Apply UI data to scene node
        """
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

        mcs.dcc.set_attr(clip_node, "start_pose_enabled", start_pose_enabled)
        mcs.dcc.set_attr(clip_node, "end_pose_enabled", end_pose_enabled)
        mcs.dcc.set_attr(clip_node, "end_pose_same_as_start", end_pose_same_as_start)

        if start_pose_enabled:
            mcs.dcc.set_attr(clip_node, "start_pose_path", start_pose_path)

        if end_pose_enabled:
            if end_pose_same_as_start:
                end_pose_path = start_pose_path
                self.match_end_pose_to_start()
            mcs.dcc.set_attr(clip_node, "end_pose_path", end_pose_path)

    def get_active_rig(self):
        return self.ui.scene_actor_CB.currentText()

    def toggle_mocap_constraint(self):
        if self.mocap_bind_result:
            self.unbind_mocap_from_rig()
            self.mocap_bind_result = None

            # update UI display
            self.ui.connect_mocap_to_rig_BTN.setText("Preview Mocap On Rig")
            self.ui.connect_mocap_to_rig_BTN.setStyleSheet("")
            self.ui.bake_BTN.setEnabled(True)
        else:
            if self.bind_mocap_to_rig():
                self.ui.connect_mocap_to_rig_BTN.setText("Detach from Mocap")
                self.ui.connect_mocap_to_rig_BTN.setStyleSheet("background-color:rgb(150, 100, 80)")
                self.ui.bake_BTN.setEnabled(False)

    def match_end_pose_to_start(self):
        if not self.ui.end_pose_same_CHK.isChecked():
            return
        start_pose_path = self.ui.start_pose_CB.currentData(QtCore.Qt.UserRole)
        ui_utils.set_combo_box_by_data(self.ui.end_pose_CB, start_pose_path)

    def bind_mocap_to_rig(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            print("No Mocap found in selection")
            return

        rig_name = self.get_active_rig()

        self.mocap_bind_result = mcs.dcc.connect_mocap_to_rig(
            mocap_ns=clip_data.get(k.cdc.namespace),
            rig_name=rig_name
        )

        return True

    def unbind_mocap_from_rig(self):
        mcs.dcc.disconnect_mocap_from_rig(self.mocap_bind_result)

    def import_mocap(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(caption="Open picker layout", filter="FBX (*.fbx)")
        if file_path:
            mcs.dcc.import_mocap(file_path)
            self.update_from_scene()

    def bake_to_rig(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            print("Clip not found in selection")
            return

        mocap_namespace = clip_data.get(k.cdc.namespace)
        if not mocap_namespace:
            print("WARNING: could not find namespace of driven objects of clip.")
            return

        rig_name = self.get_active_rig()
        start_frame = clip_data.get(k.cdc.start_frame)
        end_frame = clip_data.get(k.cdc.end_frame)

        mcs.dcc.pre_bake()

        if self.ui.align_to_start_pose_CHK.isChecked():
            start_pose_path = self.ui.start_pose_CB.currentData(QtCore.Qt.UserRole)
            mcs.dcc.apply_pose(start_pose_path, rig_name)
            mcs.dcc.align_mocap_to_rig(mocap_namespace, rig_name)

        rig_controls = mcs.dcc.bake_to_rig(
            mocap_ns=mocap_namespace,
            rig_name=rig_name,
            start_frame=start_frame,
            end_frame=end_frame,
            euler_filter=self.ui.euler_filter_CHK.isChecked(),
        )

        if self.ui.start_pose_CHK.isChecked() or self.ui.end_pose_CHK.isChecked():
            mcs.dcc.rebuild_pose_anim_layer(rig_controls)

        if self.ui.start_pose_CHK.isChecked():
            start_pose_path = self.ui.start_pose_CB.currentData(QtCore.Qt.UserRole)
            mcs.dcc.apply_pose(
                pose_path=start_pose_path,
                rig_name=rig_name,
                on_frame=start_frame,
                set_key=True,
            )

        if self.ui.end_pose_CHK.isChecked():
            end_pose_path = self.ui.end_pose_CB.currentData(QtCore.Qt.UserRole)
            mcs.dcc.apply_pose(
                pose_path=end_pose_path,
                rig_name=rig_name,
                on_frame=end_frame,
                set_key=True,
            )

        if self.ui.adjustment_blend_CHK.isChecked():
            mcs.dcc.run_adjustment_blend()

        if self.ui.set_time_range_CHK.isChecked():
            mcs.dcc.set_time_range((start_frame, end_frame))

    def apply_start_pose(self):
        start_pose_path = self.ui.start_pose_CB.currentData(QtCore.Qt.UserRole)
        mcs.dcc.apply_pose(start_pose_path, rig_name=self.get_active_rig())

    def apply_end_pose(self):
        end_pose_path = self.ui.end_pose_CB.currentData(QtCore.Qt.UserRole)
        mcs.dcc.apply_pose(end_pose_path, rig_name=self.get_active_rig())

    def align_mocap_with_rig(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            print("Clip not found in selection")
            return
        mocap_namespace = clip_data.get(k.cdc.namespace)
        rig_name = self.get_active_rig()
        mcs.dcc.align_mocap_to_rig(mocap_namespace, rig_name)

    def set_time_range(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            print("Clip not found in selection")
            return
        mcs.dcc.set_time_range((
            clip_data.get(k.cdc.start_frame),
            clip_data.get(k.cdc.end_frame),
        ))


def main(refresh=False):
    win = MocapClipperWindow()
    win.main(refresh=refresh)

    if standalone_app:
        ui_utils.standalone_app_window = win
        sys.exit(standalone_app.exec_())

    return win


if __name__ == "__main__":
    main()
