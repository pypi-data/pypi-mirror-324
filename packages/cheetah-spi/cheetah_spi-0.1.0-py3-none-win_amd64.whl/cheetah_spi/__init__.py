# cheetah/__init__.py
import os
import sys
import platform

ext = '.dll' if platform.system() == 'Windows' else '.so'
lib_name = f"cheetah{ext}"

# Full path to the library in the same folder as this __init__.py
lib_path = os.path.join(os.path.dirname(__file__), lib_name)

# Depending on Python version, use importlib.machinery or imp
if sys.version_info >= (3, 5):
    from importlib.machinery import ExtensionFileLoader
    from importlib.util import spec_from_file_location, module_from_spec

    loader = ExtensionFileLoader("cheetah", lib_path)
    spec = spec_from_file_location("cheetah", lib_path, loader=loader)
    cheetah_module = module_from_spec(spec)
    spec.loader.exec_module(cheetah_module)

else:
    # Fallback for older Python versions
    import imp
    cheetah_module = imp.load_dynamic("cheetah", lib_path)

# Put the loaded module into sys.modules so `import cheetah` works
sys.modules["cheetah_spi"] = cheetah_module

# Optionally import or define short aliases here if you want them:
# e.g. from .cheetah_module import some_function