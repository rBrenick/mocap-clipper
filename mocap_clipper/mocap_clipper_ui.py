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

        self.constrain_values = None

        # set UI
        self.scene_data = None
        self.ui.main_splitter.setSizes([1, 2])
        self.update_from_project()
        self.update_from_scene()
        self.ui.refresh_BTN.setIcon(QtGui.QIcon(resources.get_image_path("refresh_icon")))

        # connect UI
        self.ui.refresh_BTN.clicked.connect(self.update_from_scene)
        self.ui.clips_LW.itemSelectionChanged.connect(self.update_clip_display_info)

        self.ui.end_pose_CHK.stateChanged.connect(self.toggle_end_pose)
        self.ui.end_pose_CB.currentIndexChanged.connect(self.toggle_end_pose)
        self.ui.end_pose_same_CHK.stateChanged.connect(self.toggle_end_pose)
        self.ui.end_pose_same_CHK.stateChanged.connect(self.ui.end_pose_CB.setDisabled)
        self.ui.start_pose_CHK.stateChanged.connect(self.toggle_start_pose)
        self.ui.start_pose_CHK.stateChanged.connect(self.ui.start_pose_CB.setEnabled)
        self.ui.start_pose_CB.currentIndexChanged.connect(self.match_end_pose_to_start)

        self.ui.attach_to_rig_BTN.clicked.connect(self.toggle_mocap_constraint)
        self.ui.bake_BTN.clicked.connect(self.bake_to_rig)

    def update_from_project(self):
        pose_files = mcs.dcc.get_pose_files()
        pose_icon = mcs.dcc.get_pose_icon()
        pose_icon = pose_icon if pose_icon else QtGui.QIcon()
        for pose_file in pose_files:
            pose_name = os.path.splitext(os.path.basename(pose_file))[0]
            self.ui.start_pose_CB.addItem(pose_icon, pose_name, pose_file)
            self.ui.end_pose_CB.addItem(pose_icon, pose_name, pose_file)

    def update_from_scene(self):
        self.ui.clips_LW.clear()
        self.scene_data = mcs.dcc.get_scene_time_editor_data()
        for clip_name in self.scene_data.keys():
            lw = QtWidgets.QListWidgetItem()
            lw.setText(clip_name)
            self.ui.clips_LW.addItem(lw)

        self.ui.scene_actor_CB.clear()
        rig_names = mcs.dcc.get_rigs_in_scene().keys()
        self.ui.scene_actor_CB.addItems(rig_names)

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
            start_pose_path = mcs.dcc.get_attr(clip_node, "start_pose_path")
            if start_pose_path:
                self.ui.start_pose_CHK.setChecked(True)
                ui_utils.set_combo_box_by_data(self.ui.start_pose_CB, start_pose_path)
            else:
                self.ui.start_pose_CHK.setChecked(False)

            end_pose_path = mcs.dcc.get_attr(clip_node, "end_pose_path")
            if end_pose_path:
                self.ui.end_pose_same_CHK.setChecked(False)
                ui_utils.set_combo_box_by_data(self.ui.end_pose_CB, end_pose_path)
            else:
                self.ui.end_pose_same_CHK.setChecked(True)

    def get_active_clip_data(self):
        selected_clips = self.ui.clips_LW.selectedItems()
        if selected_clips:
            clip_lw = selected_clips[0]  # type: QtWidgets.QListWidgetItem
            clip_name = clip_lw.text()
            return self.scene_data.get(clip_name)

    def toggle_start_pose(self, state):
        if not state:
            self.ui.start_pose_CB.setEnabled(False)
            return

        clip_data = self.get_active_clip_data()
        if not clip_data:
            return

        clip_node = clip_data.get(k.cdc.node)

        self.ui.start_pose_CB.setEnabled(True)
        pose_path = self.ui.start_pose_CB.currentData(QtCore.Qt.UserRole)
        mcs.dcc.set_attr(
            node=clip_node,
            attr_name="start_pose_path",
            value=pose_path,
        )

    def toggle_end_pose(self):
        self.match_end_pose_to_start()

        clip_data = self.get_active_clip_data()
        if not clip_data:
            return

        clip_node = clip_data.get(k.cdc.node)
        if self.ui.end_pose_same_CHK.isChecked():
            mcs.dcc.set_attr(node=clip_node, attr_name="end_pose_path", value="")
            return

        self.ui.end_pose_CB.setEnabled(True)
        pose_path = self.ui.end_pose_CB.currentData(QtCore.Qt.UserRole)
        mcs.dcc.set_attr(
            node=clip_node,
            attr_name="end_pose_path",
            value=pose_path,
        )

    def toggle_mocap_constraint(self):
        if self.constrain_values:
            self.unbind_mocap_from_rig()
        else:
            self.bind_mocap_to_rig()
            self.constrain_values = None

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
        self.constrain_values = mcs.dcc.constrain_mocap_to_rig(
            mocap_ns=clip_data.get(k.cdc.namespace),
            rig_name=rig_name
        )
        self.ui.attach_to_rig_BTN.setText("Detach from Mocap")
        self.ui.attach_to_rig_BTN.setStyleSheet("background-color:rgb(150, 100, 80)")

    def unbind_mocap_from_rig(self):
        mcs.dcc.disconnect_mocap_from_rig(self.constrain_values)
        self.ui.attach_to_rig_BTN.setText("Attach to Rig")
        self.ui.attach_to_rig_BTN.setStyleSheet("")

    def bake_to_rig(self):
        clip_data = self.get_active_clip_data()
        if not clip_data:
            return
        rig_name = self.ui.scene_actor_CB.currentText()
        start_frame = float(self.ui.frame_start.text())
        end_frame = float(self.ui.frame_end.text())

        rig_controls = mcs.dcc.bake_to_rig(
            mocap_ns=clip_data.get(k.cdc.namespace),
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
                frame=start_frame,
            )

        if self.ui.end_pose_CHK.isChecked():
            end_pose_path = self.ui.end_pose_CB.currentData(QtCore.Qt.UserRole)
            mcs.dcc.apply_pose(
                pose_path=end_pose_path,
                rig_name=rig_name,
                frame=end_frame,
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
