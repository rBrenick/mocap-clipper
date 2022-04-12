import inspect
import os
import site
import sys
import traceback


def _mocap_clipper_site_dir_setup():
    dirname = os.path.dirname

    # Add site-packages to sys.path
    package_dir = dirname(dirname(dirname(dirname(inspect.getfile(inspect.currentframe())))))

    if package_dir not in sys.path:
        site.addsitedir(package_dir)


_mocap_clipper_site_dir_setup()

try:
    import mocap_clipper

    mocap_clipper.startup()
except Exception as e:
    traceback.print_exc()




