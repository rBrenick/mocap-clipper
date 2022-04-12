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
        MocapClipperWidget.resize(717, 366)
        self.verticalLayout_2 = QVBoxLayout(MocapClipperWidget)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter = QSplitter(MocapClipperWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.widget_2 = QWidget(self.splitter)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.refresh_BTN = QPushButton(self.widget_2)
        self.refresh_BTN.setObjectName(u"refresh_BTN")
        self.refresh_BTN.setMinimumSize(QSize(0, 30))

        self.verticalLayout_3.addWidget(self.refresh_BTN)

        self.clips_LW = QListWidget(self.widget_2)
        QListWidgetItem(self.clips_LW)
        self.clips_LW.setObjectName(u"clips_LW")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clips_LW.sizePolicy().hasHeightForWidth())
        self.clips_LW.setSizePolicy(sizePolicy)
        self.clips_LW.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_3.addWidget(self.clips_LW)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.splitter.addWidget(self.widget_2)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_4 = QHBoxLayout(self.widget)
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.clip_name_LE = QLineEdit(self.widget)
        self.clip_name_LE.setObjectName(u"clip_name_LE")
        self.clip_name_LE.setCursor(QCursor(Qt.BlankCursor))
        self.clip_name_LE.setAlignment(Qt.AlignCenter)
        self.clip_name_LE.setReadOnly(True)

        self.verticalLayout_4.addWidget(self.clip_name_LE)

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


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

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

        self.start_pose_browse_BTN = QPushButton(self.widget)
        self.start_pose_browse_BTN.setObjectName(u"start_pose_browse_BTN")
        sizePolicy1.setHeightForWidth(self.start_pose_browse_BTN.sizePolicy().hasHeightForWidth())
        self.start_pose_browse_BTN.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.start_pose_browse_BTN)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

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

        self.end_pose_browse_BTN = QPushButton(self.widget)
        self.end_pose_browse_BTN.setObjectName(u"end_pose_browse_BTN")
        sizePolicy1.setHeightForWidth(self.end_pose_browse_BTN.sizePolicy().hasHeightForWidth())
        self.end_pose_browse_BTN.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.end_pose_browse_BTN)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.euler_filter_CHK = QCheckBox(self.widget)
        self.euler_filter_CHK.setObjectName(u"euler_filter_CHK")
        self.euler_filter_CHK.setChecked(True)

        self.verticalLayout_4.addWidget(self.euler_filter_CHK)

        self.selected_controls_CHK = QCheckBox(self.widget)
        self.selected_controls_CHK.setObjectName(u"selected_controls_CHK")

        self.verticalLayout_4.addWidget(self.selected_controls_CHK)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.splitter.addWidget(self.widget)

        self.verticalLayout_2.addWidget(self.splitter)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.scene_actor_CB = QComboBox(MocapClipperWidget)
        self.scene_actor_CB.addItem("")
        self.scene_actor_CB.setObjectName(u"scene_actor_CB")
        self.scene_actor_CB.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.scene_actor_CB)

        self.attach_to_rig_BTN = QPushButton(MocapClipperWidget)
        self.attach_to_rig_BTN.setObjectName(u"attach_to_rig_BTN")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.attach_to_rig_BTN.sizePolicy().hasHeightForWidth())
        self.attach_to_rig_BTN.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.attach_to_rig_BTN)

        self.bake_BTN = QPushButton(MocapClipperWidget)
        self.bake_BTN.setObjectName(u"bake_BTN")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.bake_BTN.sizePolicy().hasHeightForWidth())
        self.bake_BTN.setSizePolicy(sizePolicy3)
        self.bake_BTN.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.bake_BTN)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(MocapClipperWidget)

        QMetaObject.connectSlotsByName(MocapClipperWidget)
    # setupUi

    def retranslateUi(self, MocapClipperWidget):
        MocapClipperWidget.setWindowTitle(QCoreApplication.translate("MocapClipperWidget", u"Form", None))
        self.refresh_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Refresh", None))

        __sortingEnabled = self.clips_LW.isSortingEnabled()
        self.clips_LW.setSortingEnabled(False)
        ___qlistwidgetitem = self.clips_LW.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MocapClipperWidget", u"Clip_01", None));
        self.clips_LW.setSortingEnabled(__sortingEnabled)

        self.clip_name_LE.setPlaceholderText(QCoreApplication.translate("MocapClipperWidget", u"Clip Name", None))
        self.frame_start.setPlaceholderText(QCoreApplication.translate("MocapClipperWidget", u"Start Frame", None))
        self.frame_end.setPlaceholderText(QCoreApplication.translate("MocapClipperWidget", u"End Frame", None))
        self.frame_duration.setText("")
        self.frame_duration.setPlaceholderText(QCoreApplication.translate("MocapClipperWidget", u"Duration", None))
        self.start_pose_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Start Pose", None))
        self.start_pose_browse_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Browse", None))
        self.end_pose_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"End Pose", None))
        self.end_pose_same_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Same As Start", None))
        self.end_pose_browse_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Browse", None))
        self.euler_filter_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"Euler Filter", None))
        self.selected_controls_CHK.setText(QCoreApplication.translate("MocapClipperWidget", u"On Selected Controls", None))
        self.scene_actor_CB.setItemText(0, QCoreApplication.translate("MocapClipperWidget", u"actor0", None))

        self.attach_to_rig_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Attach to Rig", None))
        self.bake_BTN.setText(QCoreApplication.translate("MocapClipperWidget", u"Bake to Rig", None))
    # retranslateUi

