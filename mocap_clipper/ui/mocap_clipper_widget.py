# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mocap_clipper_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from mocap_clipper.ui_utils import QtPathWidget


class Ui_MocapClipperWidget(object):
    def setupUi(self, MocapClipperWidget):
        if not MocapClipperWidget.objectName():
            MocapClipperWidget.setObjectName(u"MocapClipperWidget")
        MocapClipperWidget.resize(709, 588)
        self.main_layout = QVBoxLayout(MocapClipperWidget)
        self.main_layout.setSpacing(2)
        self.main_layout.setObjectName(u"main_layout")
        self.main_layout.setContentsMargins(3, 3, 3, 3)
        self.main_splitter = QSplitter(MocapClipperWidget)
        self.main_splitter.setObjectName(u"main_splitter")
        self.main_splitter.setOrientation(Qt.Horizontal)
        self.widget_2 = QWidget(self.main_splitter)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.import_mocap_BTN = QPushButton(self.widget_2)
        self.import_mocap_BTN.setObjectName(u"import_mocap_BTN")
        self.import_mocap_BTN.setMinimumSize(QSize(0, 30))
        self.import_mocap_BTN.setStyleSheet(u"background-color:rgb(160, 100, 60)")

        self.verticalLayout_3.addWidget(self.import_mocap_BTN)

        self.refresh_project_BTN = QPushButton(self.widget_2)
        self.refresh_project_BTN.setObjectName(u"refresh_project_BTN")
        self.refresh_project_BTN.setMinimumSize(QSize(0, 30))

        self.verticalLayout_3.addWidget(self.refresh_project_BTN)

        self.refresh_BTN = QPushButton(self.widget_2)
        self.refresh_BTN.setObjectName(u"refresh_BTN")
        self.refresh_BTN.setMinimumSize(QSize(0, 30))

        self.verticalLayout_3.addWidget(self.refresh_BTN)

        self.clips_LW = QListWidget(self.widget_2)
        self.clips_LW.setObjectName(u"clips_LW")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clips_LW.sizePolicy().hasHeightForWidth())
        self.clips_LW.setSizePolicy(sizePolicy)
        self.clips_LW.setStyleSheet(u"QListView::item {height: 30px;}")
        self.clips_LW.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_3.addWidget(self.clips_LW)

        self.scene_actor_CB = QComboBox(self.widget_2)
        self.scene_actor_CB.addItem("")
        self.scene_actor_CB.setObjectName(u"scene_actor_CB")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scene_actor_CB.sizePolicy().hasHeightForWidth())
        self.scene_actor_CB.setSizePolicy(sizePolicy1)
        self.scene_actor_CB.setMinimumSize(QSize(0, 30))

        self.verticalLayout_3.addWidget(self.scene_actor_CB)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.main_splitter.addWidget(self.widget_2)
        self.widget = QWidget(self.main_splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(2, 0, 2, 0)
        self.scrollArea = QScrollArea(self.widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 381, 605))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.clip_info_layout = QVBoxLayout()
        self.clip_info_layout.setObjectName(u"clip_info_layout")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.clip_name_LE = QLineEdit(self.scrollAreaWidgetContents)
        self.clip_name_LE.setObjectName(u"clip_name_LE")
        sizePolicy.setHeightForWidth(self.clip_name_LE.sizePolicy().hasHeightForWidth())
        self.clip_name_LE.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        self.clip_name_LE.setFont(font)
        self.clip_name_LE.setCursor(QCursor(Qt.BlankCursor))
        self.clip_name_LE.setAlignment(Qt.AlignCenter)
        self.clip_name_LE.setReadOnly(True)

        self.horizontalLayout_8.addWidget(self.clip_name_LE)

        self.rename_clip_BTN = QPushButton(self.scrollAreaWidgetContents)
        self.rename_clip_BTN.setObjectName(u"rename_clip_BTN")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.rename_clip_BTN.sizePolicy().hasHeightForWidth())
        self.rename_clip_BTN.setSizePolicy(sizePolicy2)
        self.rename_clip_BTN.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_8.addWidget(self.rename_clip_BTN)


        self.clip_info_layout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.frame_start = QLineEdit(self.scrollAreaWidgetContents)
        self.frame_start.setObjectName(u"frame_start")
        sizePolicy.setHeightForWidth(self.frame_start.sizePolicy().hasHeightForWidth())
        self.frame_start.setSizePolicy(sizePolicy)
        self.frame_start.setReadOnly(True)

        self.horizontalLayout_7.addWidget(self.frame_start)

        self.frame_end = QLineEdit(self.scrollAreaWidgetContents)
        self.frame_end.setObjectName(u"frame_end")
        sizePolicy.setHeightForWidth(self.frame_end.sizePolicy().hasHeightForWidth())
        self.frame_end.setSizePolicy(sizePolicy)
        self.frame_end.setReadOnly(True)

        self.horizontalLayout_7.addWidget(self.frame_end)

        self.frame_duration = QLineEdit(self.scrollAreaWidgetContents)
        self.frame_duration.setObjectName(u"frame_duration")
        sizePolicy2.setHeightForWidth(self.frame_duration.sizePolicy().hasHeightForWidth())
        self.frame_duration.setSizePolicy(sizePolicy2)
        self.frame_duration.setMaximumSize(QSize(70, 16777215))
        self.frame_duration.setReadOnly(True)

        self.horizontalLayout_7.addWidget(self.frame_duration)


        self.clip_info_layout.addLayout(self.horizontalLayout_7)


        self.verticalLayout.addLayout(self.clip_info_layout)

        self.pose_configuration_root_layout = QVBoxLayout()
        self.pose_configuration_root_layout.setSpacing(2)
        self.pose_configuration_root_layout.setObjectName(u"pose_configuration_root_layout")
        self.pose_configuration_BTN = QPushButton(self.scrollAreaWidgetContents)
        self.pose_configuration_BTN.setObjectName(u"pose_configuration_BTN")
        font1 = QFont()
        font1.setItalic(True)
        self.pose_configuration_BTN.setFont(font1)
        self.pose_configuration_BTN.setStyleSheet(u"background-color:rgb(75, 75, 75); text-align:left;")
        self.pose_configuration_BTN.setCheckable(True)
        self.pose_configuration_BTN.setChecked(True)

        self.pose_configuration_root_layout.addWidget(self.pose_configuration_BTN)

        self.pose_configuration_widget = QWidget(self.scrollAreaWidgetContents)
        self.pose_configuration_widget.setObjectName(u"pose_configuration_widget")
        self.verticalLayout_10 = QVBoxLayout(self.pose_configuration_widget)
        self.verticalLayout_10.setSpacing(2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.start_pose_CHK = QCheckBox(self.pose_configuration_widget)
        self.start_pose_CHK.setObjectName(u"start_pose_CHK")
        sizePolicy2.setHeightForWidth(self.start_pose_CHK.sizePolicy().hasHeightForWidth())
        self.start_pose_CHK.setSizePolicy(sizePolicy2)

        self.horizontalLayout_9.addWidget(self.start_pose_CHK)

        self.start_pose_CB = QComboBox(self.pose_configuration_widget)
        self.start_pose_CB.setObjectName(u"start_pose_CB")
        self.start_pose_CB.setEnabled(False)
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.start_pose_CB.sizePolicy().hasHeightForWidth())
        self.start_pose_CB.setSizePolicy(sizePolicy3)

        self.horizontalLayout_9.addWidget(self.start_pose_CB)


        self.verticalLayout_10.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.end_pose_CHK = QCheckBox(self.pose_configuration_widget)
        self.end_pose_CHK.setObjectName(u"end_pose_CHK")
        sizePolicy2.setHeightForWidth(self.end_pose_CHK.sizePolicy().hasHeightForWidth())
        self.end_pose_CHK.setSizePolicy(sizePolicy2)

        self.horizontalLayout_10.addWidget(self.end_pose_CHK)

        self.end_pose_CB = QComboBox(self.pose_configuration_widget)
        self.end_pose_CB.setObjectName(u"end_pose_CB")
        self.end_pose_CB.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.end_pose_CB.sizePolicy().hasHeightForWidth())
        self.end_pose_CB.setSizePolicy(sizePolicy3)

        self.horizontalLayout_10.addWidget(self.end_pose_CB)


        self.verticalLayout_10.addLayout(self.horizontalLayout_10)

        self.end_pose_same_CHK = QCheckBox(self.pose_configuration_widget)
        self.end_pose_same_CHK.setObjectName(u"end_pose_same_CHK")
        sizePolicy2.setHeightForWidth(self.end_pose_same_CHK.sizePolicy().hasHeightForWidth())
        self.end_pose_same_CHK.setSizePolicy(sizePolicy2)

        self.verticalLayout_10.addWidget(self.end_pose_same_CHK)


        self.pose_configuration_root_layout.addWidget(self.pose_configuration_widget)


        self.verticalLayout.addLayout(self.pose_configuration_root_layout)

        self.preprocess_mocap_actions_root_layout = QVBoxLayout()
        self.preprocess_mocap_actions_root_layout.setSpacing(4)
        self.preprocess_mocap_actions_root_layout.setObjectName(u"preprocess_mocap_actions_root_layout")
        self.preprocess_mocap_actions_BTN = QPushButton(self.scrollAreaWidgetContents)
        self.preprocess_mocap_actions_BTN.setObjectName(u"preprocess_mocap_actions_BTN")
        self.preprocess_mocap_actions_BTN.setFont(font1)
        self.preprocess_mocap_actions_BTN.setStyleSheet(u"background-color:rgb(75, 75, 75); text-align:left;")
        self.preprocess_mocap_actions_BTN.setCheckable(True)
        self.preprocess_mocap_actions_BTN.setChecked(True)

        self.preprocess_mocap_actions_root_layout.addWidget(self.preprocess_mocap_actions_BTN)

        self.preprocess_mocap_actions_widget = QWidget(self.scrollAreaWidgetContents)
        self.preprocess_mocap_actions_widget.setObjectName(u"preprocess_mocap_actions_widget")
        self.verticalLayout_2 = QVBoxLayout(self.preprocess_mocap_actions_widget)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.reproject_mocap_ctrl_BTN = QPushButton(self.preprocess_mocap_actions_widget)
        self.reproject_mocap_ctrl_BTN.setObjectName(u"reproject_mocap_ctrl_BTN")
        self.reproject_mocap_ctrl_BTN.setEnabled(False)
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.reproject_mocap_ctrl_BTN.sizePolicy().hasHeightForWidth())
        self.reproject_mocap_ctrl_BTN.setSizePolicy(sizePolicy4)

        self.verticalLayout_2.addWidget(self.reproject_mocap_ctrl_BTN)

        self.reproject_root_anim_BTN = QPushButton(self.preprocess_mocap_actions_widget)
        self.reproject_root_anim_BTN.setObjectName(u"reproject_root_anim_BTN")
        self.reproject_root_anim_BTN.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.reproject_root_anim_BTN.sizePolicy().hasHeightForWidth())
        self.reproject_root_anim_BTN.setSizePolicy(sizePolicy4)

        self.verticalLayout_2.addWidget(self.reproject_root_anim_BTN)

        self.align_root_to_rig_BTN = QPushButton(self.preprocess_mocap_actions_widget)
        self.align_root_to_rig_BTN.setObjectName(u"align_root_to_rig_BTN")
        self.align_root_to_rig_BTN.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.align_root_to_rig_BTN.sizePolicy().hasHeightForWidth())
        self.align_root_to_rig_BTN.setSizePolicy(sizePolicy4)

        self.verticalLayout_2.addWidget(self.align_root_to_rig_BTN)

        self.toggle_root_aim_BTN = QPushButton(self.preprocess_mocap_actions_widget)
        self.toggle_root_aim_BTN.setObjectName(u"toggle_root_aim_BTN")
        self.toggle_root_aim_BTN.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.toggle_root_aim_BTN.sizePolicy().hasHeightForWidth())
        self.toggle_root_aim_BTN.setSizePolicy(sizePolicy4)
        self.toggle_root_aim_BTN.setCheckable(True)

        self.verticalLayout_2.addWidget(self.toggle_root_aim_BTN)


        self.preprocess_mocap_actions_root_layout.addWidget(self.preprocess_mocap_actions_widget)


        self.verticalLayout.addLayout(self.preprocess_mocap_actions_root_layout)

        self.bake_configuration_root_layout = QVBoxLayout()
        self.bake_configuration_root_layout.setSpacing(2)
        self.bake_configuration_root_layout.setObjectName(u"bake_configuration_root_layout")
        self.bake_configuration_BTN = QPushButton(self.scrollAreaWidgetContents)
        self.bake_configuration_BTN.setObjectName(u"bake_configuration_BTN")
        self.bake_configuration_BTN.setFont(font1)
        self.bake_configuration_BTN.setStyleSheet(u"background-color:rgb(75, 75, 75); text-align:left;")
        self.bake_configuration_BTN.setCheckable(True)
        self.bake_configuration_BTN.setChecked(True)

        self.bake_configuration_root_layout.addWidget(self.bake_configuration_BTN)

        self.bake_configuration_widget = QWidget(self.scrollAreaWidgetContents)
        self.bake_configuration_widget.setObjectName(u"bake_configuration_widget")
        self.verticalLayout_6 = QVBoxLayout(self.bake_configuration_widget)
        self.verticalLayout_6.setSpacing(2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.project_settings_layout = QVBoxLayout()
        self.project_settings_layout.setObjectName(u"project_settings_layout")

        self.verticalLayout_6.addLayout(self.project_settings_layout)

        self.bake_configs = QVBoxLayout()
        self.bake_configs.setObjectName(u"bake_configs")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.align_mocap_CHK = QCheckBox(self.bake_configuration_widget)
        self.align_mocap_CHK.setObjectName(u"align_mocap_CHK")

        self.horizontalLayout.addWidget(self.align_mocap_CHK)

        self.align_to_start_pose_RB = QRadioButton(self.bake_configuration_widget)
        self.align_to_start_pose_RB.setObjectName(u"align_to_start_pose_RB")
        self.align_to_start_pose_RB.setChecked(True)

        self.horizontalLayout.addWidget(self.align_to_start_pose_RB)

        self.align_to_end_pose_RB = QRadioButton(self.bake_configuration_widget)
        self.align_to_end_pose_RB.setObjectName(u"align_to_end_pose_RB")

        self.horizontalLayout.addWidget(self.align_to_end_pose_RB)

        self.align_mocap_CB = QComboBox(self.bake_configuration_widget)
        self.align_mocap_CB.setObjectName(u"align_mocap_CB")

        self.horizontalLayout.addWidget(self.align_mocap_CB)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.bake_configs.addLayout(self.horizontalLayout)

        self.euler_filter_CHK = QCheckBox(self.bake_configuration_widget)
        self.euler_filter_CHK.setObjectName(u"euler_filter_CHK")
        self.euler_filter_CHK.setChecked(True)

        self.bake_configs.addWidget(self.euler_filter_CHK)

        self.set_time_range_CHK = QCheckBox(self.bake_configuration_widget)
        self.set_time_range_CHK.setObjectName(u"set_time_range_CHK")
        self.set_time_range_CHK.setChecked(True)

        self.bake_configs.addWidget(self.set_time_range_CHK)

        self.adjustment_blend_CHK = QCheckBox(self.bake_configuration_widget)
        self.adjustment_blend_CHK.setObjectName(u"adjustment_blend_CHK")

        self.bake_configs.addWidget(self.adjustment_blend_CHK)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.save_clip_CHK = QCheckBox(self.bake_configuration_widget)
        self.save_clip_CHK.setObjectName(u"save_clip_CHK")
        sizePolicy2.setHeightForWidth(self.save_clip_CHK.sizePolicy().hasHeightForWidth())
        self.save_clip_CHK.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.save_clip_CHK)

        self.output_path_W = QtPathWidget(self.bake_configuration_widget)
        self.output_path_W.setObjectName(u"output_path_W")
        self.output_path_W.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.output_path_W.sizePolicy().hasHeightForWidth())
        self.output_path_W.setSizePolicy(sizePolicy4)
        self.output_path_W.setMinimumSize(QSize(0, 20))

        self.horizontalLayout_6.addWidget(self.output_path_W)


        self.bake_configs.addLayout(self.horizontalLayout_6)


        self.verticalLayout_6.addLayout(self.bake_configs)


        self.bake_configuration_root_layout.addWidget(self.bake_configuration_widget)


        self.verticalLayout.addLayout(self.bake_configuration_root_layout)

        self.bake_actions_root_layout = QVBoxLayout()
        self.bake_actions_root_layout.setObjectName(u"bake_actions_root_layout")
        self.bake_actions_BTN = QPushButton(self.scrollAreaWidgetContents)
        self.bake_actions_BTN.setObjectName(u"bake_actions_BTN")
        self.bake_actions_BTN.setFont(font1)
        self.bake_actions_BTN.setStyleSheet(u"background-color:rgb(75, 75, 75); text-align:left;")
        self.bake_actions_BTN.setCheckable(True)
        self.bake_actions_BTN.setChecked(True)

        self.bake_actions_root_layout.addWidget(self.bake_actions_BTN)

        self.bake_actions_widget = QWidget(self.scrollAreaWidgetContents)
        self.bake_actions_widget.setObjectName(u"bake_actions_widget")
        self.verticalLayout_12 = QVBoxLayout(self.bake_actions_widget)
        self.verticalLayout_12.setSpacing(2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(-1, 0, -1, -1)
        self.bake_actions_layout = QHBoxLayout()
        self.bake_actions_layout.setSpacing(3)
        self.bake_actions_layout.setObjectName(u"bake_actions_layout")
        self.connect_mocap_to_rig_BTN = QPushButton(self.bake_actions_widget)
        self.connect_mocap_to_rig_BTN.setObjectName(u"connect_mocap_to_rig_BTN")
        sizePolicy4.setHeightForWidth(self.connect_mocap_to_rig_BTN.sizePolicy().hasHeightForWidth())
        self.connect_mocap_to_rig_BTN.setSizePolicy(sizePolicy4)

        self.bake_actions_layout.addWidget(self.connect_mocap_to_rig_BTN)

        self.bake_BTN = QPushButton(self.bake_actions_widget)
        self.bake_BTN.setObjectName(u"bake_BTN")
        sizePolicy5 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.bake_BTN.sizePolicy().hasHeightForWidth())
        self.bake_BTN.setSizePolicy(sizePolicy5)
        self.bake_BTN.setMinimumSize(QSize(0, 30))
        self.bake_BTN.setStyleSheet(u"background-color:rgb(80, 80, 80)")

        self.bake_actions_layout.addWidget(self.bake_BTN)


        self.verticalLayout_12.addLayout(self.bake_actions_layout)


        self.bake_actions_root_layout.addWidget(self.bake_actions_widget)


        self.verticalLayout.addLayout(self.bake_actions_root_layout)

        self.project_widgets_root_layout = QVBoxLayout()
        self.project_widgets_root_layout.setObjectName(u"project_widgets_root_layout")
        self.project_widgets_BTN = QPushButton(self.scrollAreaWidgetContents)
        self.project_widgets_BTN.setObjectName(u"project_widgets_BTN")
        self.project_widgets_BTN.setFont(font1)
        self.project_widgets_BTN.setStyleSheet(u"background-color:rgb(75, 75, 75); text-align:left;")
        self.project_widgets_BTN.setCheckable(True)
        self.project_widgets_BTN.setChecked(True)

        self.project_widgets_root_layout.addWidget(self.project_widgets_BTN)

        self.project_widgets_widget = QWidget(self.scrollAreaWidgetContents)
        self.project_widgets_widget.setObjectName(u"project_widgets_widget")
        self.verticalLayout_14 = QVBoxLayout(self.project_widgets_widget)
        self.verticalLayout_14.setSpacing(2)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(-1, 0, -1, -1)
        self.project_widgets_layout = QVBoxLayout()
        self.project_widgets_layout.setObjectName(u"project_widgets_layout")

        self.verticalLayout_14.addLayout(self.project_widgets_layout)


        self.project_widgets_root_layout.addWidget(self.project_widgets_widget)


        self.verticalLayout.addLayout(self.project_widgets_root_layout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scrollArea)

        self.main_splitter.addWidget(self.widget)

        self.main_layout.addWidget(self.main_splitter)


        self.retranslateUi(MocapClipperWidget)

        QMetaObject.connectSlotsByName(MocapClipperWidget)
    # setupUi

    def retranslateUi(self, MocapClipperWidget):
        MocapClipperWidget.setWindowTitle(QCoreApplication.translate("MocapClipperWidget", u"Form", None))
        self.import_mocap_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Import Mocap", None))
        self.refresh_project_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Refresh Project Poses", None))
        self.refresh_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Refresh Time Editor Clips", None))
        self.scene_actor_CB.setItemText(0, QCoreApplication.translate("MocapClipperWidget", u"actor0:Rig", None))

#if QT_CONFIG(tooltip)
        self.scene_actor_CB.setToolTip(QCoreApplication.translate("MocapClipperWidget", u"Name of the target rig", None))
#endif // QT_CONFIG(tooltip)
        self.clip_name_LE.setPlaceholderText(QCoreApplication.translate("MocapClipperWidget", u"Clip Name", None))
        self.rename_clip_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Rename", None))
        self.frame_start.setPlaceholderText(QCoreApplication.translate("MocapClipperWidget", u"Start Frame", None))
        self.frame_end.setPlaceholderText(QCoreApplication.translate("MocapClipperWidget", u"End Frame", None))
        self.frame_duration.setText("")
        self.frame_duration.setPlaceholderText(QCoreApplication.translate("MocapClipperWidget", u"Duration", None))
        self.pose_configuration_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"> Pose Configuration", None))
        self.start_pose_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Start Pose", None))
        self.end_pose_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"End Pose", None))
        self.end_pose_same_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Match End Pose to Start", None))
        self.preprocess_mocap_actions_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"> Pre-Process Mocap Actions", None))
        self.reproject_mocap_ctrl_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Re-Project Mocap Control under Hips", None))
        self.reproject_root_anim_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Re-Project Root Anim under Hips", None))
        self.align_root_to_rig_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Align Root to Rig", None))
        self.toggle_root_aim_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Toggle Root Aim", None))
        self.bake_configuration_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"> Bake Configuration", None))
#if QT_CONFIG(tooltip)
        self.align_mocap_CHK.setToolTip(QCoreApplication.translate("MocapClipperWidget", u"Move the Mocap skeleton to match the rig at a certain pose", None))
#endif // QT_CONFIG(tooltip)
        self.align_mocap_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Align Mocap to:", None))
        self.align_to_start_pose_RB.setText(QCoreApplication.translate("MocapClipperWidget", u"Start Frame", None))
        self.align_to_end_pose_RB.setText(QCoreApplication.translate("MocapClipperWidget", u"End Frame", None))
#if QT_CONFIG(tooltip)
        self.euler_filter_CHK.setToolTip(QCoreApplication.translate("MocapClipperWidget", u"Run an euler filter on the keys after baking", None))
#endif // QT_CONFIG(tooltip)
        self.euler_filter_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Euler Filter", None))
#if QT_CONFIG(tooltip)
        self.set_time_range_CHK.setToolTip(QCoreApplication.translate("MocapClipperWidget", u"Set the scene time range to match the clip after bake", None))
#endif // QT_CONFIG(tooltip)
        self.set_time_range_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Set Time Range", None))
#if QT_CONFIG(tooltip)
        self.adjustment_blend_CHK.setToolTip(QCoreApplication.translate("MocapClipperWidget", u"Blend the Start and End pose layer using the intensity of the base animation", None))
#endif // QT_CONFIG(tooltip)
        self.adjustment_blend_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Run Adjustment Blend", None))
#if QT_CONFIG(tooltip)
        self.save_clip_CHK.setToolTip(QCoreApplication.translate("MocapClipperWidget", u"Enable this to automatically save the clip into the selected folder", None))
#endif // QT_CONFIG(tooltip)
        self.save_clip_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Save As Clip", None))
#if QT_CONFIG(tooltip)
        self.output_path_W.setToolTip(QCoreApplication.translate("MocapClipperWidget", u"Output folder for the clips", None))
#endif // QT_CONFIG(tooltip)
        self.bake_actions_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"> Bake Actions", None))
#if QT_CONFIG(tooltip)
        self.connect_mocap_to_rig_BTN.setToolTip(QCoreApplication.translate("MocapClipperWidget", u"Constrain the rig to the mocap skeleton", None))
#endif // QT_CONFIG(tooltip)
        self.connect_mocap_to_rig_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Preview Mocap On Rig", None))
#if QT_CONFIG(tooltip)
        self.bake_BTN.setToolTip(QCoreApplication.translate("MocapClipperWidget", u"Bake the selected clip to the rig using the above configuration", None))
#endif // QT_CONFIG(tooltip)
        self.bake_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Bake to Rig", None))
        self.project_widgets_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"> Project Actions", None))
    # retranslateUi

