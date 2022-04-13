import os.path
import sys

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
        self.ui.connect_mocap_to_rig_BTN.setIcon(rig_icon)
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

        self.ui.connect_mocap_to_rig_BTN.clicked.connect(self.toggle_mocap_constraint)
        self.ui.bake_BTN.clicked.connect(self.bake_to_rig)

    def update_from_project(self):
        pose_files = mcs.dcc.get_pose_files()
        pose_icon = mcs.dcc.get_pose_icon() or QtGui.QIcon()
        for pose_file in pose_files:
            pose_name = os.path.splitext(os.path.basename(pose_file))[0]
            self.ui.start_pose_CB.addItem(pose_icon, pose_name, pose_file)
            self.ui.end_pose_CB.addItem(pose_icon, pose_name, pose_file)

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
        if len(selected_clips) == 1:
            clip_lw = selected_clips[0]  # type: QtWidgets.QListWidgetItem
            clip_name = clip_lw.text()
            clip_data = self.scene_data.get(clip_name)

        elif len(selected_clips) > 1:
            clip_name = "[Multiple Clips Selected]"
            clip_data = dict()
            clip_data[k.cdc.start_frame] = "[...]"
            clip_data[k.cdc.end_frame] = "[...]"
            clip_data[k.cdc.frame_duration] = "[...]"

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

        start_pose_path = self.ui.end_pose_CB.currentData(QtCore.Qt.UserRole)
        end_pose_path = self.ui.end_pose_CB.currentData(QtCore.Qt.UserRole)
        start_pose_enabled = self.ui.start_pose_CHK.isChecked()
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

    def toggle_mocap_constraint(self):
        print(self.mocap_bind_result)
        if self.mocap_bind_result:
            self.unbind_mocap_from_rig()
        else:
            self.bind_mocap_to_rig()
            self.mocap_bind_result = None

    def match_end_pose_to_start(self):
        if not self.ui.end_pose_same_CHK.isChecked():
            return
        start_pose_path = self.ui.start_pose_CB.currentData(QtCore.Qt.UserRole)
        ui_utils.set_combo_box_by_data(self.ui.end_pose_CB, start_pose_path)

    def bind_mocap_to_rig(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            return
        rig_name = self.ui.scene_actor_CB.currentText()
        self.mocap_bind_result = mcs.dcc.connect_mocap_to_rig(
            mocap_ns=clip_data.get(k.cdc.namespace),
            rig_name=rig_name
        )
        self.ui.connect_mocap_to_rig_BTN.setText("Detach from Mocap")
        self.ui.connect_mocap_to_rig_BTN.setStyleSheet("background-color:rgb(150, 100, 80)")

    def unbind_mocap_from_rig(self):
        mcs.dcc.disconnect_mocap_from_rig(self.mocap_bind_result)
        self.ui.connect_mocap_to_rig_BTN.setText("Preview Mocap On Rig")
        self.ui.connect_mocap_to_rig_BTN.setStyleSheet("")

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

        rig_name = self.ui.scene_actor_CB.currentText()
        start_frame = clip_data.get(k.cdc.start_frame)
        end_frame = clip_data.get(k.cdc.end_frame)

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
            )

        if self.ui.end_pose_CHK.isChecked():
            end_pose_path = self.ui.end_pose_CB.currentData(QtCore.Qt.UserRole)
            mcs.dcc.apply_pose(
                pose_path=end_pose_path,
                rig_name=rig_name,
                on_frame=end_frame,
            )

        if self.ui.adjustment_blend_CHK.isChecked():
            mcs.dcc.run_adjustment_blend()


def main(refresh=False):
    win = MocapClipperWindow()
    win.main(refresh=refresh)

    if standalone_app:
        ui_utils.standalone_app_window = win
        sys.exit(standalone_app.exec_())

    return win


if __name__ == "__main__":
    main()
