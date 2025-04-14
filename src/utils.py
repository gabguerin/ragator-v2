import importlib


def import_module_from_path(module_path, object_name):
    module = importlib.import_module(module_path)
    return getattr(module, object_name)
