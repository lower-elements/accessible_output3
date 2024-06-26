from __future__ import absolute_import
import ctypes
import os
import types
from platform_utils import paths


def load_library(libname, cdll=False):
    if paths.is_frozen():
        libfile = os.path.join(
            paths.embedded_data_path(), "accessible_output3", "lib", libname
        )
    else:
        libfile = os.path.join(paths.module_path(), "lib", libname)
    if not os.path.exists(libfile):
        _cxfreeze_libfile = os.path.join(
            paths.embedded_data_path(), "lib", "accessible_output3", "lib", libname
        )
        if os.path.exists(_cxfreeze_libfile):
            libfile = _cxfreeze_libfile
    if cdll:
        return ctypes.cdll[libfile]
    return ctypes.windll[libfile]


def get_output_classes():
    from . import outputs

    module_type = types.ModuleType
    classes = [
        m.output_class
        for m in outputs.__dict__.values()
        if isinstance(m, module_type) and hasattr(m, "output_class")
    ]
    return sorted(classes, key=lambda c: c.priority)


def find_datafiles():
    import platform
    from glob import glob
    import accessible_output3

    if platform.system() != "Windows":
        return []
    path = os.path.join(accessible_output3.__path__[0], "lib", "*.dll")
    results = glob(path)
    dest_dir = os.path.join("accessible_output3", "lib")
    return [(dest_dir, results)]
