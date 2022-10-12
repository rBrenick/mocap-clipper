import os
import sys
import traceback
from functools import partial
import logging

from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance

if sys.version_info.major >= 3:
    long = int

active_dcc_is_maya = "maya" in os.path.basename(sys.executable).lower()
active_dcc_is_houdini = "houdini" in os.path.basename(sys.executable).lower()

standalone_app_window = None

resources_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")


def get_app_window():
    top_window = standalone_app_window

    if active_dcc_is_maya:
        from maya import OpenMayaUI as omui
        maya_main_window_ptr = omui.MQtUtil.mainWindow()
        top_window = wrapInstance(long(maya_main_window_ptr), QtWidgets.QMainWindow)

    elif active_dcc_is_houdini:
        import hou
        top_window = hou.qt.mainWindow()

    return top_window


class CoreToolWindow(QtWidgets.QMainWindow):

    win_instances = []

    def __init__(self, parent=None):
        if parent is None:
            parent = get_app_window()
        super(CoreToolWindow, self).__init__(parent)

        self.ui = None
        self.setWindowTitle(self.__class__.__name__)

    def main(self, *args, **kwargs):
        self.show()

    def on_close(self):
        """for easy overloading with maya dockable windows"""
        pass

    #########################################################
    # convenience functions to make a simple button layout

    def ensure_main_layout(self):
        if self.ui is None:
            main_widget = QtWidgets.QWidget()
            main_layout = QtWidgets.QVBoxLayout()
            main_widget.setLayout(main_layout)
            self.ui = main_widget
            self.setCentralWidget(main_widget)

    def add_button(self, text, command, clicked_args=None):
        self.ensure_main_layout()

        main_layout = self.ui.layout()

        btn = QtWidgets.QPushButton(text)
        btn.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        main_layout.addWidget(btn)

        if clicked_args:
            btn.clicked.connect(partial(command, *clicked_args))
        else:
            btn.clicked.connect(command)


if active_dcc_is_maya:

    from maya.app.general import mayaMixin
    from maya import OpenMayaUI as omui
    from maya import cmds

    class ToolWindow(mayaMixin.MayaQWidgetDockableMixin, CoreToolWindow):

        WORKSPACE_NAMES = []

        def __init__(self, parent=None):
            if parent is None:
                parent = get_app_window()
            super(ToolWindow, self).__init__(parent=parent)
            self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        def main(self, restore=False, refresh=False):
            if restore:
                restored_control = omui.MQtUtil.getCurrentParent()
                mixin_ptr = omui.MQtUtil.findControl(self.objectName())
                omui.MQtUtil.addWidgetToMayaLayout(long(mixin_ptr), long(restored_control))

                self.WORKSPACE_NAMES.append(self.parent().objectName())
                return self

            if refresh:
                opened_workspaces = list(self.WORKSPACE_NAMES)
                for workspace_name in opened_workspaces:
                    try:
                        remove_workspace(workspace_name)
                        self.WORKSPACE_NAMES.remove(workspace_name)
                    except Exception as e:
                        print(e)

            launch_ui_script = "import {module}; {module}.{class_name}().main(restore=True)".format(
                module=self.__class__.__module__,
                class_name=self.__class__.__name__,
            )

            self.show(dockable=True, height=500, width=700, uiScript=launch_ui_script)

            self.WORKSPACE_NAMES.append(self.parent().objectName())
            return self

        def hideEvent(self, *args):
            if not self.isVisible():
                self.on_close()
            super(ToolWindow, self).hideEvent(*args)


    def remove_workspace(workspace_control_name):
        if cmds.workspaceControl(workspace_control_name, q=True, exists=True):
            cmds.workspaceControl(workspace_control_name, e=True, close=True)
            cmds.deleteUI(workspace_control_name, control=True)

else:
    ToolWindow = CoreToolWindow


def build_menu_from_action_list(actions, menu=None, is_sub_menu=False):
    if not menu:
        menu = QtWidgets.QMenu()

    for action in actions:
        if action == "-":
            menu.addSeparator()
            continue

        for action_title, action_command in action.items():
            if action_title == "RADIO_SETTING":
                # Create RadioButtons for QSettings object
                settings_obj = action_command.get("settings")  # type: QtCore.QSettings
                settings_key = action_command.get("settings_key")  # type: str
                choices = action_command.get("choices")  # type: list
                default_choice = action_command.get("default")  # type: str
                on_trigger_command = action_command.get("on_trigger_command")  # function to trigger after setting value

                # Has choice been defined in settings?
                item_to_check = settings_obj.value(settings_key)

                # If not, read from default option argument
                if not item_to_check:
                    item_to_check = default_choice

                grp = QtWidgets.QActionGroup(menu)
                for choice_key in choices:
                    action = QtWidgets.QAction(choice_key, menu)
                    action.setCheckable(True)

                    if choice_key == item_to_check:
                        action.setChecked(True)

                    action.triggered.connect(partial(
                        set_settings_value,
                        settings_obj,
                        settings_key,
                        choice_key,
                        on_trigger_command
                    ))
                    menu.addAction(action)
                    grp.addAction(action)

                grp.setExclusive(True)
                continue

            if isinstance(action_command, list):
                sub_menu = menu.addMenu(action_title)
                build_menu_from_action_list(action_command, menu=sub_menu, is_sub_menu=True)
                continue

            atn = menu.addAction(action_title)
            atn.triggered.connect(action_command)

    if not is_sub_menu:
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    return menu


def set_settings_value(settings_obj, key, value, post_set_command=None):
    settings_obj.setValue(key, value)
    if post_set_command:
        post_set_command()


def compile_ui(src_ui_path):
    out_py_path = src_ui_path.replace(".ui", ".py")

    if sys.version_info.major > 2:
        import subprocess
        uic_exe = os.path.join(os.path.dirname(os.path.dirname(sys.executable)), "bin3", "pyside2-uic.exe")
        command = '"%s" %s > %s' % (uic_exe, src_ui_path, out_py_path)
        subprocess.Popen(command, shell=True)
    else:
        import pyside2uic
        with open(out_py_path, 'w') as filehandle:
            pyside2uic.compileUi(src_ui_path, filehandle, indent=4)


def set_combo_box_by_data(cb, data):
    """
    Args:
        cb (QtWidgets.QComboBox):
        data (str):
    """
    index = cb.findData(data, QtCore.Qt.UserRole)
    if index != -1:
        cb.setCurrentIndex(index)


def set_combo_box_by_text(cb, text):
    """
    Args:
        cb (QtWidgets.QComboBox):
        text (str):
    """
    index = cb.findData(text, QtCore.Qt.DisplayRole)
    if index != -1:
        cb.setCurrentIndex(index)


def get_list_widget_items(list_widget):
    """

    Args:
        list_widget (QtWidgets.QListWidget):

    Returns:

    """
    list_widget_items = []

    for i in range(list_widget.count()):
        lwi = list_widget.item(i)
        list_widget_items.append(lwi)

    return list_widget_items


def set_combo_box_searchable(combo_box):
    combo_box.setFocusPolicy(QtCore.Qt.StrongFocus)
    combo_box.setEditable(True)
    combo_box.setInsertPolicy(QtWidgets.QComboBox.NoInsert)

    filter_model = QtCore.QSortFilterProxyModel(combo_box)
    filter_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
    filter_model.setSourceModel(combo_box.model())

    completer = QtWidgets.QCompleter(filter_model, combo_box)
    completer.setCompletionMode(QtWidgets.QCompleter.UnfilteredPopupCompletion)
    combo_box.setCompleter(completer)
    combo_box.lineEdit().textEdited.connect(filter_model.setFilterFixedString)


def build_log_level_menu(menu_bar, log_cls):
    log_levels = {
        logging.getLevelName(logging.DEBUG): logging.DEBUG,
        logging.getLevelName(logging.INFO): logging.INFO,
        logging.getLevelName(logging.WARNING): logging.WARNING,
    }

    log_menu = menu_bar.addMenu("Log Level")  # type: QtWidgets.QMenu
    ag = QtWidgets.QActionGroup(log_menu, exclusive=True)

    for level_name, log_level in log_levels.items():
        action = QtWidgets.QAction(level_name, log_menu, checkable=True)

        if log_level == log_cls.level:
            action.setChecked(True)

        # connect signal
        set_level = partial(log_cls.setLevel, log_level)
        action.triggered.connect(set_level)

        ag.addAction(action)
        log_menu.addAction(action)


class QtPathWidget(QtWidgets.QWidget):
    def __init__(
            self,
            parent=None,
            settings_name="_DefaultQtPathSettings",
            start_dir="",
            file_filter="",
            use_directory_dialog=False,
            relative_to_path="",
            recent_paths_amount=30,
    ):
        """
        QWidget for file paths.

        Includes "browse" button and list of recent file paths.

        :param parent: Qt Parent
        :param settings_name: name for settings .ini
        :param start_dir: start folder for file dialog
        :param file_filter: filter for the QFileDialog
        :param use_directory_dialog: browse for folder instead of file path
        :param relative_to_path: show paths relative to this path
        :param recent_paths_amount: clamp recent paths to this amount
        """

        super(QtPathWidget, self).__init__(parent)

        # safety convert, just in case we get passed negative float values for some reason
        recent_paths_amount = int(abs(recent_paths_amount))

        self.start_dir = start_dir
        self.relative_to_path = relative_to_path
        self.relative_to_path_drive = os.path.splitdrive(self.relative_to_path)[0]
        self.use_directory_dialog = use_directory_dialog
        self.recent_paths_amount = recent_paths_amount

        # settings object to store data between sessions
        self._settings = QtPathWidgetSettings(
            identifier=settings_name,
            recent_paths_amount=recent_paths_amount,
            relative_to_path=relative_to_path,
        )

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)

        # surprise, it's a QComboBox for the path display
        self.path_CB = QtWidgets.QComboBox()
        self.path_CB.addItems(self._settings.get_recent_paths())
        self.path_CB.setEditable(True)
        self.path_CB.setCurrentText("")
        self.path_CB.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)

        main_layout.addWidget(self.path_CB)

        # Browse path button
        self.browse_file_BTN = QtWidgets.QPushButton("...")
        self.browse_file_BTN.setMaximumWidth(40)
        self.browse_file_BTN.setMaximumHeight(20)
        self.browse_file_BTN.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.browse_file_BTN.clicked.connect(self._open_dialog_and_set_path)
        main_layout.addWidget(self.browse_file_BTN)

        self.setLayout(main_layout)

        # create path dialog instance for later use
        self.path_dialog = QtWidgets.QFileDialog()

        if self.use_directory_dialog:
            self.path_dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)

        self.path_dialog.setNameFilter(file_filter)

    def _open_dialog_and_set_path(self):
        file_path = self.get_dialog_path()
        if file_path:
            self.set_path(file_path)

    def get_dialog_path(self):
        # set starting directory for dialog
        start_dir = self.start_dir

        # no start_dir specified, use folder of most recent path
        if not start_dir:
            start_dir = str(self._settings.value(QtPathWidgetSettings.key_most_recent_dir, defaultValue=""))

        self.path_dialog.setDirectory(start_dir)

        # display dialog
        if self.path_dialog.exec_():
            selected_paths = self.path_dialog.selectedFiles()
            self._settings.setValue(QtPathWidgetSettings.key_most_recent_dir, os.path.dirname(selected_paths[0]))
            return selected_paths[0]

    def set_path(self, path):
        """
        Set path display in ComboBox and store in settings

        :param path:
        :return:
        """
        self._settings.add_recent_path(path)  # store full path in settings, then convert to relative if desired

        # convert to relative path
        path_drive = os.path.splitdrive(path)[0]
        if self.relative_to_path and path_drive == self.relative_to_path_drive:
            path = os.path.relpath(path, self.relative_to_path)

        # if path has already been added to ComboBox, remove the old one
        path_index_map = {self.path_CB.itemText(i): i for i in range(self.path_CB.count())}
        if path in path_index_map.keys():
            self.path_CB.removeItem(path_index_map[path])

        # add to ComboBox and set as active path
        self.path_CB.insertItem(0, path)
        self.path_CB.setCurrentIndex(0)

        # clamp amount of recent paths
        while self.path_CB.count() > self.recent_paths_amount:
            self.path_CB.removeItem(self.recent_paths_amount)

    def path(self):
        """get path from widget"""
        current_path = self.path_CB.currentText()

        # join with relative_to_path if it's a relative path
        if self.relative_to_path and os.path.splitdrive(current_path)[0] != "":
            return os.path.abspath(os.path.join(self.relative_to_path, current_path))

        return current_path

    ###################################################
    # Convenience functions for replacing LineEdit with this widget

    def text(self):
        return self.path()

    def setText(self, value):
        self.set_path(value)


class QtPathWidgetSettings(QtCore.QSettings):
    key_recent_paths = "recent_paths"
    key_most_recent_dir = "most_recent_dir"

    def __init__(self, identifier="_DefaultQtPathWidgetSettings", recent_paths_amount=30, relative_to_path=""):

        # C:\Users\USERNAME\AppData\Roaming\QtPathWidget\_DefaultQtFilePathSettings.ini

        super(QtPathWidgetSettings, self).__init__(
            QtCore.QSettings.IniFormat,
            QtCore.QSettings.UserScope,
            'QtPathWidget',
            identifier
        )
        self.recent_paths_amount = recent_paths_amount
        self.relative_to_path = relative_to_path
        self.relative_to_path_drive = os.path.splitdrive(self.relative_to_path)[0]

    def get_recent_paths(self, full_paths=False):
        """
        Get recent paths from settings

        :param full_paths: skip converting to relative paths
        :return:
        """
        paths = self.value(self.key_recent_paths)
        if not isinstance(paths, list):
            if paths:
                # QSettings ini sometimes has trouble reading data types
                paths = str(paths).split(", ")
            else:
                paths = []

        # convert to relative paths before returning
        if not full_paths and self.relative_to_path:
            relative_paths = []

            for full_path in paths:
                if os.path.splitdrive(full_path)[0] != self.relative_to_path_drive:
                    # if the path is on a separate drive then we can't get a relative path
                    relative_paths.append(full_path)
                else:
                    relative_paths.append(os.path.relpath(full_path, self.relative_to_path))

            paths = relative_paths

        return paths

    def add_recent_path(self, path):
        """
        Add path to recent paths in settings

        :param path: <str>
        :return:
        """
        recent_paths = self.get_recent_paths(full_paths=True)

        # remove path from recent_paths if it's been added previously
        if path in recent_paths:
            recent_paths.remove(path)

        recent_paths.insert(0, path)

        if len(recent_paths) > self.recent_paths_amount:  # clamp amount of paths
            recent_paths = recent_paths[:self.recent_paths_amount]

        self.setValue(self.key_recent_paths, recent_paths)
