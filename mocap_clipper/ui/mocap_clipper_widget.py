# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\git\mocap-clipper\mocap_clipper\ui\mocap_clipper_widget.ui',
# licensing of 'D:\git\mocap-clipper\mocap_clipper\ui\mocap_clipper_widget.ui' applies.
#
# Created: Sat Oct  8 15:31:37 2022
#      by: pyside2-uic  running on PySide2 5.12.5
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MocapClipperWidget(object):
    def setupUi(self, MocapClipperWidget):
        MocapClipperWidget.setObjectName("MocapClipperWidget")
        MocapClipperWidget.resize(1186, 1122)
        self.main_layout = QtWidgets.QVBoxLayout(MocapClipperWidget)
        self.main_layout.setSpacing(2)
        self.main_layout.setContentsMargins(3, 3, 3, 3)
        self.main_layout.setObjectName("main_layout")
        self.main_splitter = QtWidgets.QSplitter(MocapClipperWidget)
        self.main_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.main_splitter.setObjectName("main_splitter")
        self.widget_2 = QtWidgets.QWidget(self.main_splitter)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.import_mocap_BTN = QtWidgets.QPushButton(self.widget_2)
        self.import_mocap_BTN.setMinimumSize(QtCore.QSize(0, 30))
        self.import_mocap_BTN.setStyleSheet("background-color:rgb(160, 100, 60)")
        self.import_mocap_BTN.setObjectName("import_mocap_BTN")
        self.verticalLayout_3.addWidget(self.import_mocap_BTN)
        self.refresh_project_BTN = QtWidgets.QPushButton(self.widget_2)
        self.refresh_project_BTN.setMinimumSize(QtCore.QSize(0, 30))
        self.refresh_project_BTN.setObjectName("refresh_project_BTN")
        self.verticalLayout_3.addWidget(self.refresh_project_BTN)
        self.refresh_BTN = QtWidgets.QPushButton(self.widget_2)
        self.refresh_BTN.setMinimumSize(QtCore.QSize(0, 30))
        self.refresh_BTN.setObjectName("refresh_BTN")
        self.verticalLayout_3.addWidget(self.refresh_BTN)
        self.clips_LW = QtWidgets.QListWidget(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clips_LW.sizePolicy().hasHeightForWidth())
        self.clips_LW.setSizePolicy(sizePolicy)
        self.clips_LW.setStyleSheet("QListView::item {height: 30px;}")
        self.clips_LW.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.clips_LW.setObjectName("clips_LW")
        self.verticalLayout_3.addWidget(self.clips_LW)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.widget = QtWidgets.QWidget(self.main_splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(2, 0, 2, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 807, 1114))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.clip_info_layout = QtWidgets.QVBoxLayout()
        self.clip_info_layout.setSpacing(3)
        self.clip_info_layout.setContentsMargins(0, 0, 0, 0)
        self.clip_info_layout.setObjectName("clip_info_layout")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.clip_name_LE = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clip_name_LE.sizePolicy().hasHeightForWidth())
        self.clip_name_LE.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.clip_name_LE.setFont(font)
        self.clip_name_LE.setCursor(QtCore.Qt.BlankCursor)
        self.clip_name_LE.setAlignment(QtCore.Qt.AlignCenter)
        self.clip_name_LE.setReadOnly(True)
        self.clip_name_LE.setObjectName("clip_name_LE")
        self.horizontalLayout_8.addWidget(self.clip_name_LE)
        self.rename_clip_BTN = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rename_clip_BTN.sizePolicy().hasHeightForWidth())
        self.rename_clip_BTN.setSizePolicy(sizePolicy)
        self.rename_clip_BTN.setMaximumSize(QtCore.QSize(70, 16777215))
        self.rename_clip_BTN.setObjectName("rename_clip_BTN")
        self.horizontalLayout_8.addWidget(self.rename_clip_BTN)
        self.clip_info_layout.addLayout(self.horizontalLayout_8)
        self.source_path_LE = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.source_path_LE.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.source_path_LE.setReadOnly(True)
        self.source_path_LE.setObjectName("source_path_LE")
        self.clip_info_layout.addWidget(self.source_path_LE)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.frame_start = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_start.sizePolicy().hasHeightForWidth())
        self.frame_start.setSizePolicy(sizePolicy)
        self.frame_start.setReadOnly(True)
        self.frame_start.setObjectName("frame_start")
        self.horizontalLayout_7.addWidget(self.frame_start)
        self.frame_end = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_end.sizePolicy().hasHeightForWidth())
        self.frame_end.setSizePolicy(sizePolicy)
        self.frame_end.setReadOnly(True)
        self.frame_end.setObjectName("frame_end")
        self.horizontalLayout_7.addWidget(self.frame_end)
        self.frame_duration = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_duration.sizePolicy().hasHeightForWidth())
        self.frame_duration.setSizePolicy(sizePolicy)
        self.frame_duration.setMaximumSize(QtCore.QSize(70, 16777215))
        self.frame_duration.setText("")
        self.frame_duration.setReadOnly(True)
        self.frame_duration.setObjectName("frame_duration")
        self.horizontalLayout_7.addWidget(self.frame_duration)
        self.clip_info_layout.addLayout(self.horizontalLayout_7)
        self.verticalLayout.addLayout(self.clip_info_layout)
        self.pose_configuration_root_layout = QtWidgets.QVBoxLayout()
        self.pose_configuration_root_layout.setSpacing(2)
        self.pose_configuration_root_layout.setObjectName("pose_configuration_root_layout")
        self.pose_configuration_BTN = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setItalic(True)
        self.pose_configuration_BTN.setFont(font)
        self.pose_configuration_BTN.setStyleSheet("background-color:rgb(75, 75, 75); text-align:left;")
        self.pose_configuration_BTN.setCheckable(True)
        self.pose_configuration_BTN.setChecked(True)
        self.pose_configuration_BTN.setObjectName("pose_configuration_BTN")
        self.pose_configuration_root_layout.addWidget(self.pose_configuration_BTN)
        self.pose_configuration_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.pose_configuration_widget.setObjectName("pose_configuration_widget")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.pose_configuration_widget)
        self.verticalLayout_10.setSpacing(2)
        self.verticalLayout_10.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.start_pose_CHK = QtWidgets.QCheckBox(self.pose_configuration_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_pose_CHK.sizePolicy().hasHeightForWidth())
        self.start_pose_CHK.setSizePolicy(sizePolicy)
        self.start_pose_CHK.setObjectName("start_pose_CHK")
        self.horizontalLayout_9.addWidget(self.start_pose_CHK)
        self.start_pose_CB = QtWidgets.QComboBox(self.pose_configuration_widget)
        self.start_pose_CB.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_pose_CB.sizePolicy().hasHeightForWidth())
        self.start_pose_CB.setSizePolicy(sizePolicy)
        self.start_pose_CB.setObjectName("start_pose_CB")
        self.horizontalLayout_9.addWidget(self.start_pose_CB)
        self.verticalLayout_10.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.end_pose_CHK = QtWidgets.QCheckBox(self.pose_configuration_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.end_pose_CHK.sizePolicy().hasHeightForWidth())
        self.end_pose_CHK.setSizePolicy(sizePolicy)
        self.end_pose_CHK.setObjectName("end_pose_CHK")
        self.horizontalLayout_10.addWidget(self.end_pose_CHK)
        self.end_pose_CB = QtWidgets.QComboBox(self.pose_configuration_widget)
        self.end_pose_CB.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.end_pose_CB.sizePolicy().hasHeightForWidth())
        self.end_pose_CB.setSizePolicy(sizePolicy)
        self.end_pose_CB.setObjectName("end_pose_CB")
        self.horizontalLayout_10.addWidget(self.end_pose_CB)
        self.verticalLayout_10.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pose_match_CHK = QtWidgets.QCheckBox(self.pose_configuration_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pose_match_CHK.sizePolicy().hasHeightForWidth())
        self.pose_match_CHK.setSizePolicy(sizePolicy)
        self.pose_match_CHK.setObjectName("pose_match_CHK")
        self.horizontalLayout_2.addWidget(self.pose_match_CHK)
        self.pose_match_type_CB = QtWidgets.QComboBox(self.pose_configuration_widget)
        self.pose_match_type_CB.setEnabled(False)
        self.pose_match_type_CB.setObjectName("pose_match_type_CB")
        self.horizontalLayout_2.addWidget(self.pose_match_type_CB)
        self.pose_match_method_CB = QtWidgets.QComboBox(self.pose_configuration_widget)
        self.pose_match_method_CB.setEnabled(False)
        self.pose_match_method_CB.setObjectName("pose_match_method_CB")
        self.horizontalLayout_2.addWidget(self.pose_match_method_CB)
        self.verticalLayout_10.addLayout(self.horizontalLayout_2)
        self.pose_configuration_root_layout.addWidget(self.pose_configuration_widget)
        self.verticalLayout.addLayout(self.pose_configuration_root_layout)
        self.preprocess_mocap_actions_root_layout = QtWidgets.QVBoxLayout()
        self.preprocess_mocap_actions_root_layout.setSpacing(4)
        self.preprocess_mocap_actions_root_layout.setObjectName("preprocess_mocap_actions_root_layout")
        self.preprocess_mocap_actions_BTN = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setItalic(True)
        self.preprocess_mocap_actions_BTN.setFont(font)
        self.preprocess_mocap_actions_BTN.setStyleSheet("background-color:rgb(75, 75, 75); text-align:left;")
        self.preprocess_mocap_actions_BTN.setCheckable(True)
        self.preprocess_mocap_actions_BTN.setChecked(True)
        self.preprocess_mocap_actions_BTN.setObjectName("preprocess_mocap_actions_BTN")
        self.preprocess_mocap_actions_root_layout.addWidget(self.preprocess_mocap_actions_BTN)
        self.preprocess_mocap_actions_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.preprocess_mocap_actions_widget.setObjectName("preprocess_mocap_actions_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.preprocess_mocap_actions_widget)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.reproject_mocap_ctrl_BTN = QtWidgets.QPushButton(self.preprocess_mocap_actions_widget)
        self.reproject_mocap_ctrl_BTN.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reproject_mocap_ctrl_BTN.sizePolicy().hasHeightForWidth())
        self.reproject_mocap_ctrl_BTN.setSizePolicy(sizePolicy)
        self.reproject_mocap_ctrl_BTN.setObjectName("reproject_mocap_ctrl_BTN")
        self.verticalLayout_2.addWidget(self.reproject_mocap_ctrl_BTN)
        self.reproject_root_anim_BTN = QtWidgets.QPushButton(self.preprocess_mocap_actions_widget)
        self.reproject_root_anim_BTN.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reproject_root_anim_BTN.sizePolicy().hasHeightForWidth())
        self.reproject_root_anim_BTN.setSizePolicy(sizePolicy)
        self.reproject_root_anim_BTN.setObjectName("reproject_root_anim_BTN")
        self.verticalLayout_2.addWidget(self.reproject_root_anim_BTN)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.align_root_to_origin_BTN = QtWidgets.QPushButton(self.preprocess_mocap_actions_widget)
        self.align_root_to_origin_BTN.setEnabled(False)
        self.align_root_to_origin_BTN.setObjectName("align_root_to_origin_BTN")
        self.horizontalLayout_4.addWidget(self.align_root_to_origin_BTN)
        self.align_root_to_rig_BTN = QtWidgets.QPushButton(self.preprocess_mocap_actions_widget)
        self.align_root_to_rig_BTN.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.align_root_to_rig_BTN.sizePolicy().hasHeightForWidth())
        self.align_root_to_rig_BTN.setSizePolicy(sizePolicy)
        self.align_root_to_rig_BTN.setObjectName("align_root_to_rig_BTN")
        self.horizontalLayout_4.addWidget(self.align_root_to_rig_BTN)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.toggle_root_aim_BTN = QtWidgets.QPushButton(self.preprocess_mocap_actions_widget)
        self.toggle_root_aim_BTN.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggle_root_aim_BTN.sizePolicy().hasHeightForWidth())
        self.toggle_root_aim_BTN.setSizePolicy(sizePolicy)
        self.toggle_root_aim_BTN.setCheckable(True)
        self.toggle_root_aim_BTN.setObjectName("toggle_root_aim_BTN")
        self.verticalLayout_2.addWidget(self.toggle_root_aim_BTN)
        self.preprocess_mocap_actions_root_layout.addWidget(self.preprocess_mocap_actions_widget)
        self.verticalLayout.addLayout(self.preprocess_mocap_actions_root_layout)
        self.bake_configuration_root_layout = QtWidgets.QVBoxLayout()
        self.bake_configuration_root_layout.setSpacing(2)
        self.bake_configuration_root_layout.setObjectName("bake_configuration_root_layout")
        self.bake_configuration_BTN = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setItalic(True)
        self.bake_configuration_BTN.setFont(font)
        self.bake_configuration_BTN.setStyleSheet("background-color:rgb(75, 75, 75); text-align:left;")
        self.bake_configuration_BTN.setCheckable(True)
        self.bake_configuration_BTN.setChecked(True)
        self.bake_configuration_BTN.setObjectName("bake_configuration_BTN")
        self.bake_configuration_root_layout.addWidget(self.bake_configuration_BTN)
        self.bake_configuration_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.bake_configuration_widget.setObjectName("bake_configuration_widget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.bake_configuration_widget)
        self.verticalLayout_6.setSpacing(2)
        self.verticalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.project_settings_layout = QtWidgets.QVBoxLayout()
        self.project_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.project_settings_layout.setObjectName("project_settings_layout")
        self.verticalLayout_6.addLayout(self.project_settings_layout)
        self.bake_configs = QtWidgets.QVBoxLayout()
        self.bake_configs.setObjectName("bake_configs")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.align_mocap_CHK = QtWidgets.QCheckBox(self.bake_configuration_widget)
        self.align_mocap_CHK.setObjectName("align_mocap_CHK")
        self.horizontalLayout.addWidget(self.align_mocap_CHK)
        self.align_to_start_pose_RB = QtWidgets.QRadioButton(self.bake_configuration_widget)
        self.align_to_start_pose_RB.setChecked(True)
        self.align_to_start_pose_RB.setObjectName("align_to_start_pose_RB")
        self.horizontalLayout.addWidget(self.align_to_start_pose_RB)
        self.align_to_end_pose_RB = QtWidgets.QRadioButton(self.bake_configuration_widget)
        self.align_to_end_pose_RB.setObjectName("align_to_end_pose_RB")
        self.horizontalLayout.addWidget(self.align_to_end_pose_RB)
        self.align_mocap_CB = QtWidgets.QComboBox(self.bake_configuration_widget)
        self.align_mocap_CB.setObjectName("align_mocap_CB")
        self.horizontalLayout.addWidget(self.align_mocap_CB)
        spacerItem = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.bake_configs.addLayout(self.horizontalLayout)
        self.euler_filter_CHK = QtWidgets.QCheckBox(self.bake_configuration_widget)
        self.euler_filter_CHK.setChecked(True)
        self.euler_filter_CHK.setObjectName("euler_filter_CHK")
        self.bake_configs.addWidget(self.euler_filter_CHK)
        self.set_time_range_CHK = QtWidgets.QCheckBox(self.bake_configuration_widget)
        self.set_time_range_CHK.setChecked(True)
        self.set_time_range_CHK.setObjectName("set_time_range_CHK")
        self.bake_configs.addWidget(self.set_time_range_CHK)
        self.adjustment_blend_CHK = QtWidgets.QCheckBox(self.bake_configuration_widget)
        self.adjustment_blend_CHK.setObjectName("adjustment_blend_CHK")
        self.bake_configs.addWidget(self.adjustment_blend_CHK)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.save_clip_CHK = QtWidgets.QCheckBox(self.bake_configuration_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_clip_CHK.sizePolicy().hasHeightForWidth())
        self.save_clip_CHK.setSizePolicy(sizePolicy)
        self.save_clip_CHK.setObjectName("save_clip_CHK")
        self.horizontalLayout_6.addWidget(self.save_clip_CHK)
        self.output_path_W = QtPathWidget(self.bake_configuration_widget)
        self.output_path_W.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_path_W.sizePolicy().hasHeightForWidth())
        self.output_path_W.setSizePolicy(sizePolicy)
        self.output_path_W.setMinimumSize(QtCore.QSize(0, 20))
        self.output_path_W.setObjectName("output_path_W")
        self.horizontalLayout_6.addWidget(self.output_path_W)
        self.bake_configs.addLayout(self.horizontalLayout_6)
        self.verticalLayout_6.addLayout(self.bake_configs)
        self.bake_actions_layout = QtWidgets.QHBoxLayout()
        self.bake_actions_layout.setSpacing(3)
        self.bake_actions_layout.setObjectName("bake_actions_layout")
        self.scene_actor_CB = QtWidgets.QComboBox(self.bake_configuration_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scene_actor_CB.sizePolicy().hasHeightForWidth())
        self.scene_actor_CB.setSizePolicy(sizePolicy)
        self.scene_actor_CB.setMinimumSize(QtCore.QSize(0, 30))
        self.scene_actor_CB.setObjectName("scene_actor_CB")
        self.scene_actor_CB.addItem("")
        self.bake_actions_layout.addWidget(self.scene_actor_CB)
        self.connect_mocap_to_rig_BTN = QtWidgets.QPushButton(self.bake_configuration_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connect_mocap_to_rig_BTN.sizePolicy().hasHeightForWidth())
        self.connect_mocap_to_rig_BTN.setSizePolicy(sizePolicy)
        self.connect_mocap_to_rig_BTN.setObjectName("connect_mocap_to_rig_BTN")
        self.bake_actions_layout.addWidget(self.connect_mocap_to_rig_BTN)
        self.bake_BTN = QtWidgets.QPushButton(self.bake_configuration_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bake_BTN.sizePolicy().hasHeightForWidth())
        self.bake_BTN.setSizePolicy(sizePolicy)
        self.bake_BTN.setMinimumSize(QtCore.QSize(0, 30))
        self.bake_BTN.setStyleSheet("background-color:rgb(80, 80, 80)")
        self.bake_BTN.setObjectName("bake_BTN")
        self.bake_actions_layout.addWidget(self.bake_BTN)
        self.verticalLayout_6.addLayout(self.bake_actions_layout)
        self.bake_configuration_root_layout.addWidget(self.bake_configuration_widget)
        self.verticalLayout.addLayout(self.bake_configuration_root_layout)
        self.project_widgets_root_layout = QtWidgets.QVBoxLayout()
        self.project_widgets_root_layout.setObjectName("project_widgets_root_layout")
        self.project_widgets_BTN = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setItalic(True)
        self.project_widgets_BTN.setFont(font)
        self.project_widgets_BTN.setStyleSheet("background-color:rgb(75, 75, 75); text-align:left;")
        self.project_widgets_BTN.setCheckable(True)
        self.project_widgets_BTN.setChecked(True)
        self.project_widgets_BTN.setObjectName("project_widgets_BTN")
        self.project_widgets_root_layout.addWidget(self.project_widgets_BTN)
        self.project_widgets_widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.project_widgets_widget.setObjectName("project_widgets_widget")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.project_widgets_widget)
        self.verticalLayout_14.setSpacing(2)
        self.verticalLayout_14.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.project_widgets_layout = QtWidgets.QVBoxLayout()
        self.project_widgets_layout.setContentsMargins(0, 0, 0, 0)
        self.project_widgets_layout.setObjectName("project_widgets_layout")
        self.verticalLayout_14.addLayout(self.project_widgets_layout)
        self.project_widgets_root_layout.addWidget(self.project_widgets_widget)
        self.verticalLayout.addLayout(self.project_widgets_root_layout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_4.addWidget(self.scrollArea)
        self.main_layout.addWidget(self.main_splitter)

        self.retranslateUi(MocapClipperWidget)
        QtCore.QMetaObject.connectSlotsByName(MocapClipperWidget)

    def retranslateUi(self, MocapClipperWidget):
        MocapClipperWidget.setWindowTitle(QtWidgets.QApplication.translate("MocapClipperWidget", "Form", None, -1))
        self.import_mocap_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Import Mocap", None, -1))
        self.refresh_project_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Refresh Project Poses", None, -1))
        self.refresh_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Refresh Time Editor Clips", None, -1))
        self.clip_name_LE.setPlaceholderText(QtWidgets.QApplication.translate("MocapClipperWidget", "Clip Name", None, -1))
        self.rename_clip_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Rename", None, -1))
        self.source_path_LE.setPlaceholderText(QtWidgets.QApplication.translate("MocapClipperWidget", "Source Path", None, -1))
        self.frame_start.setPlaceholderText(QtWidgets.QApplication.translate("MocapClipperWidget", "Start Frame", None, -1))
        self.frame_end.setPlaceholderText(QtWidgets.QApplication.translate("MocapClipperWidget", "End Frame", None, -1))
        self.frame_duration.setPlaceholderText(QtWidgets.QApplication.translate("MocapClipperWidget", "Duration", None, -1))
        self.pose_configuration_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "> Pose Configuration", None, -1))
        self.start_pose_CHK.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Start Pose", None, -1))
        self.end_pose_CHK.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "End Pose", None, -1))
        self.pose_match_CHK.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Match", None, -1))
        self.preprocess_mocap_actions_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "> Pre-Process Mocap", None, -1))
        self.reproject_mocap_ctrl_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Re-Project Mocap Control under Hips", None, -1))
        self.reproject_root_anim_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Re-Project Root Anim under Hips", None, -1))
        self.align_root_to_origin_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Align Root to World Origin", None, -1))
        self.align_root_to_rig_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Align Root to Rig", None, -1))
        self.toggle_root_aim_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Toggle Root Aim", None, -1))
        self.bake_configuration_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "> Bake", None, -1))
        self.align_mocap_CHK.setToolTip(QtWidgets.QApplication.translate("MocapClipperWidget", "Move the Mocap skeleton to match the rig at a certain pose", None, -1))
        self.align_mocap_CHK.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Align Mocap to:", None, -1))
        self.align_to_start_pose_RB.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Start Frame", None, -1))
        self.align_to_end_pose_RB.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "End Frame", None, -1))
        self.euler_filter_CHK.setToolTip(QtWidgets.QApplication.translate("MocapClipperWidget", "Run an euler filter on the keys after baking", None, -1))
        self.euler_filter_CHK.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Euler Filter", None, -1))
        self.set_time_range_CHK.setToolTip(QtWidgets.QApplication.translate("MocapClipperWidget", "Set the scene time range to match the clip after bake", None, -1))
        self.set_time_range_CHK.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Set Time Range", None, -1))
        self.adjustment_blend_CHK.setToolTip(QtWidgets.QApplication.translate("MocapClipperWidget", "Blend the Start and End pose layer using the intensity of the base animation", None, -1))
        self.adjustment_blend_CHK.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Run Adjustment Blend", None, -1))
        self.save_clip_CHK.setToolTip(QtWidgets.QApplication.translate("MocapClipperWidget", "Enable this to automatically save the clip into the selected folder", None, -1))
        self.save_clip_CHK.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Save As Clip", None, -1))
        self.output_path_W.setToolTip(QtWidgets.QApplication.translate("MocapClipperWidget", "Output folder for the clips", None, -1))
        self.scene_actor_CB.setToolTip(QtWidgets.QApplication.translate("MocapClipperWidget", "Name of the target rig", None, -1))
        self.scene_actor_CB.setItemText(0, QtWidgets.QApplication.translate("MocapClipperWidget", "actor0:Rig", None, -1))
        self.connect_mocap_to_rig_BTN.setToolTip(QtWidgets.QApplication.translate("MocapClipperWidget", "Constrain the rig to the mocap skeleton", None, -1))
        self.connect_mocap_to_rig_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Preview Mocap On Rig", None, -1))
        self.bake_BTN.setToolTip(QtWidgets.QApplication.translate("MocapClipperWidget", "Bake the selected clip to the rig using the above configuration", None, -1))
        self.bake_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "Bake to Rig", None, -1))
        self.project_widgets_BTN.setText(QtWidgets.QApplication.translate("MocapClipperWidget", "> Project Actions", None, -1))

from mocap_clipper.ui_utils import QtPathWidget
