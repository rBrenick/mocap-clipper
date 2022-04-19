def main(*args, **kwargs):
    from . import mocap_clipper_ui
    return mocap_clipper_ui.main(*args, **kwargs)


def reload_modules():
    import sys
    if sys.version_info.major >= 3:
        from importlib import reload
    else:
        from imp import reload

    from . import adjustment_blend_maya
    from . import mocap_clipper_constants
    from . import mocap_clipper_logger
    from . import mocap_clipper_dcc_core
    from . import mocap_clipper_dcc_maya
    from . import mocap_clipper_system
    from .ui import mocap_clipper_widget
    from . import mocap_clipper_ui
    reload(adjustment_blend_maya)
    reload(mocap_clipper_constants)
    reload(mocap_clipper_logger)
    reload(mocap_clipper_dcc_core)
    reload(mocap_clipper_dcc_maya)
    reload(mocap_clipper_system)
    reload(mocap_clipper_widget)
    reload(mocap_clipper_ui)
    mocap_clipper_system.import_extensions(refresh=True)
    reload(mocap_clipper_system)


def compile_ui():
    from . import ui_utils
    import os
    ui_path = os.path.join(os.path.dirname(__file__), "ui", "mocap_clipper_widget.ui")
    ui_utils.compile_ui(ui_path)


def startup():
    # from maya import cmds
    # cmds.optionVar(query="") # example of finding a maya optionvar
    pass
