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


class Ui_MocapClipperWidget(object):
    def setupUi(self, MocapClipperWidget):
        if not MocapClipperWidget.objectName():
            MocapClipperWidget.setObjectName(u"MocapClipperWidget")
        MocapClipperWidget.resize(630, 327)
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


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.main_splitter.addWidget(self.widget_2)
        self.widget = QWidget(self.main_splitter)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_4 = QHBoxLayout(self.widget)
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.clip_info_layout = QVBoxLayout()
        self.clip_info_layout.setObjectName(u"clip_info_layout")
        self.clip_name_LE = QLineEdit(self.widget)
        self.clip_name_LE.setObjectName(u"clip_name_LE")
        font = QFont()
        font.setPointSize(12)
        self.clip_name_LE.setFont(font)
        self.clip_name_LE.setCursor(QCursor(Qt.BlankCursor))
        self.clip_name_LE.setAlignment(Qt.AlignCenter)
        self.clip_name_LE.setReadOnly(True)

        self.clip_info_layout.addWidget(self.clip_name_LE)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.frame_start = QLineEdit(self.widget)
        self.frame_start.setObjectName(u"frame_start")

        self.horizontalLayout_7.addWidget(self.frame_start)

        self.frame_end = QLineEdit(self.widget)
        self.frame_end.setObjectName(u"frame_end")

        self.horizontalLayout_7.addWidget(self.frame_end)

        self.frame_duration = QLineEdit(self.widget)
        self.frame_duration.setObjectName(u"frame_duration")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_duration.sizePolicy().hasHeightForWidth())
        self.frame_duration.setSizePolicy(sizePolicy1)
        self.frame_duration.setMaximumSize(QSize(70, 16777215))
        self.frame_duration.setReadOnly(True)

        self.horizontalLayout_7.addWidget(self.frame_duration)


        self.clip_info_layout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.start_pose_CHK = QCheckBox(self.widget)
        self.start_pose_CHK.setObjectName(u"start_pose_CHK")
        sizePolicy1.setHeightForWidth(self.start_pose_CHK.sizePolicy().hasHeightForWidth())
        self.start_pose_CHK.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.start_pose_CHK)

        self.start_pose_CB = QComboBox(self.widget)
        self.start_pose_CB.setObjectName(u"start_pose_CB")
        self.start_pose_CB.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.start_pose_CB)


        self.clip_info_layout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.end_pose_CHK = QCheckBox(self.widget)
        self.end_pose_CHK.setObjectName(u"end_pose_CHK")
        sizePolicy1.setHeightForWidth(self.end_pose_CHK.sizePolicy().hasHeightForWidth())
        self.end_pose_CHK.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.end_pose_CHK)

        self.end_pose_same_CHK = QCheckBox(self.widget)
        self.end_pose_same_CHK.setObjectName(u"end_pose_same_CHK")
        sizePolicy1.setHeightForWidth(self.end_pose_same_CHK.sizePolicy().hasHeightForWidth())
        self.end_pose_same_CHK.setSizePolicy(sizePolicy1)
        self.end_pose_same_CHK.setChecked(True)

        self.horizontalLayout_2.addWidget(self.end_pose_same_CHK)

        self.end_pose_CB = QComboBox(self.widget)
        self.end_pose_CB.setObjectName(u"end_pose_CB")
        self.end_pose_CB.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.end_pose_CB)


        self.clip_info_layout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_4.addLayout(self.clip_info_layout)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.bake_settings_layout = QVBoxLayout()
        self.bake_settings_layout.setObjectName(u"bake_settings_layout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.align_mocap_CHK = QCheckBox(self.widget)
        self.align_mocap_CHK.setObjectName(u"align_mocap_CHK")
        self.align_mocap_CHK.setChecked(True)

        self.horizontalLayout.addWidget(self.align_mocap_CHK)

        self.align_to_start_pose_RB = QRadioButton(self.widget)
        self.align_to_start_pose_RB.setObjectName(u"align_to_start_pose_RB")
        self.align_to_start_pose_RB.setChecked(True)

        self.horizontalLayout.addWidget(self.align_to_start_pose_RB)

        self.align_to_end_pose_RB = QRadioButton(self.widget)
        self.align_to_end_pose_RB.setObjectName(u"align_to_end_pose_RB")

        self.horizontalLayout.addWidget(self.align_to_end_pose_RB)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.bake_settings_layout.addLayout(self.horizontalLayout)

        self.euler_filter_CHK = QCheckBox(self.widget)
        self.euler_filter_CHK.setObjectName(u"euler_filter_CHK")
        self.euler_filter_CHK.setChecked(True)

        self.bake_settings_layout.addWidget(self.euler_filter_CHK)

        self.set_time_range_CHK = QCheckBox(self.widget)
        self.set_time_range_CHK.setObjectName(u"set_time_range_CHK")
        self.set_time_range_CHK.setChecked(True)

        self.bake_settings_layout.addWidget(self.set_time_range_CHK)

        self.adjustment_blend_CHK = QCheckBox(self.widget)
        self.adjustment_blend_CHK.setObjectName(u"adjustment_blend_CHK")

        self.bake_settings_layout.addWidget(self.adjustment_blend_CHK)


        self.verticalLayout_4.addLayout(self.bake_settings_layout)

        self.project_settings_layout = QVBoxLayout()
        self.project_settings_layout.setObjectName(u"project_settings_layout")

        self.verticalLayout_4.addLayout(self.project_settings_layout)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.bake_actions_layout = QHBoxLayout()
        self.bake_actions_layout.setSpacing(3)
        self.bake_actions_layout.setObjectName(u"bake_actions_layout")
        self.scene_actor_CB = QComboBox(self.widget)
        self.scene_actor_CB.addItem("")
        self.scene_actor_CB.setObjectName(u"scene_actor_CB")
        sizePolicy1.setHeightForWidth(self.scene_actor_CB.sizePolicy().hasHeightForWidth())
        self.scene_actor_CB.setSizePolicy(sizePolicy1)
        self.scene_actor_CB.setMinimumSize(QSize(0, 30))

        self.bake_actions_layout.addWidget(self.scene_actor_CB)

        self.connect_mocap_to_rig_BTN = QPushButton(self.widget)
        self.connect_mocap_to_rig_BTN.setObjectName(u"connect_mocap_to_rig_BTN")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.connect_mocap_to_rig_BTN.sizePolicy().hasHeightForWidth())
        self.connect_mocap_to_rig_BTN.setSizePolicy(sizePolicy2)

        self.bake_actions_layout.addWidget(self.connect_mocap_to_rig_BTN)

        self.bake_BTN = QPushButton(self.widget)
        self.bake_BTN.setObjectName(u"bake_BTN")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.bake_BTN.sizePolicy().hasHeightForWidth())
        self.bake_BTN.setSizePolicy(sizePolicy3)
        self.bake_BTN.setMinimumSize(QSize(0, 30))
        self.bake_BTN.setStyleSheet(u"background-color:rgb(80, 80, 80)")

        self.bake_actions_layout.addWidget(self.bake_BTN)


        self.verticalLayout_4.addLayout(self.bake_actions_layout)

        self.project_widgets_layout = QVBoxLayout()
        self.project_widgets_layout.setObjectName(u"project_widgets_layout")

        self.verticalLayout_4.addLayout(self.project_widgets_layout)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.main_splitter.addWidget(self.widget)

        self.main_layout.addWidget(self.main_splitter)


        self.retranslateUi(MocapClipperWidget)

        QMetaObject.connectSlotsByName(MocapClipperWidget)
    # setupUi

    def retranslateUi(self, MocapClipperWidget):
        MocapClipperWidget.setWindowTitle(QCoreApplication.translate("MocapClipperWidget", u"Form", None))
        self.import_mocap_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Import Mocap", None))
        self.refresh_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Refresh Time Editor Clips", None))
        self.clip_name_LE.setPlaceholderText(QCoreApplication.translate("MocapClipperWidget", u"Clip Name", None))
        self.frame_start.setPlaceholderText(QCoreApplication.translate("MocapClipperWidget", u"Start Frame", None))
        self.frame_end.setPlaceholderText(QCoreApplication.translate("MocapClipperWidget", u"End Frame", None))
        self.frame_duration.setText("")
        self.frame_duration.setPlaceholderText(QCoreApplication.translate("MocapClipperWidget", u"Duration", None))
        self.start_pose_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Start Pose", None))
        self.end_pose_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"End Pose", None))
        self.end_pose_same_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Same As Start", None))
        self.align_mocap_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Align Mocap to:", None))
        self.align_to_start_pose_RB.setText(QCoreApplication.translate("MocapClipperWidget", u"Start Pose", None))
        self.align_to_end_pose_RB.setText(QCoreApplication.translate("MocapClipperWidget", u"End Pose", None))
        self.euler_filter_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Euler Filter", None))
        self.set_time_range_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Set Time Range", None))
        self.adjustment_blend_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Adjustment Blend", None))
        self.scene_actor_CB.setItemText(0, QCoreApplication.translate("MocapClipperWidget", u"actor0:Rig", None))

        self.connect_mocap_to_rig_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Preview Mocap On Rig", None))
        self.bake_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Bake to Rig", None))
    # retranslateUi

