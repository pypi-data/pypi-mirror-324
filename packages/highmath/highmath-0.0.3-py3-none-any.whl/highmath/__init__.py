import os
import importlib.util
import sys

def loads(directory_path):
    """
    Loads all functions from all Python scripts in a given directory into the global namespace.

    Args:
        directory_path (str): The path to the directory containing the Python scripts.

    Note:
        This method should be used with caution due to potential name conflicts and code readability issues.
        Explicit imports are generally recommended in Python.
    """
    for filename in os.listdir(directory_path):
        if filename.endswith(".py"):
            file_path = os.path.join(directory_path, filename)
            module_name = os.path.splitext(filename)[0] # Remove .py extension

            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module # Add to sys.modules to prevent duplicate imports
                spec.loader.exec_module(module)
            except Exception as e:
                #print(f"Error importing {filename}: {e}")
                continue

            for name in dir(module):
                if callable(getattr(module, name)) and not name.startswith("_"):
                    globals()[name] = getattr(module, name) # Assign to the global scope
                    #print(f"Loaded function '{name}' from '{filename}' into the global namespace.")

directory = __file__.replace('__init__.py','')+"mathdir\\" # Replace with the path to your directory
loads(directory)
del os
del importlib.util
del sys
del directory
del loads
