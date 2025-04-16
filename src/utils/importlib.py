"""
Module: Utilities
This module provides utility functions for dynamic module and object imports.
"""
import importlib


def import_module_from_path(module_path: str, object_name: str) -> object:
    """
    Dynamically imports a module and retrieves an object from it.

    Parameters:
        module_path (str): The dot-separated path of the module to import.
        object_name (str): The name of the object to retrieve from the module.

    Returns:
        object: The retrieved object from the specified module.
    """
    module = importlib.import_module(module_path)
    return getattr(module, object_name)
