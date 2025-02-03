import importlib
import sys
from pathlib import Path

class ModManager:
    """
    A utility to simplify Python imports by allowing dynamic module loading
    without deep import paths.
    """
    
    def __init__(self, base_path=None):
        self.base_path = base_path or Path.cwd()
        sys.path.insert(0, str(self.base_path))
    
    def load(self, module_name):
        """Dynamically load a module by name."""
        try:
            return importlib.import_module(module_name)
        except ModuleNotFoundError as e:
            print(f"Error: Module '{module_name}' not found.")
            raise e
    
    def auto_import(self, package_name):
        """Automatically import all modules in a given package."""
        package_path = self.base_path / package_name.replace('.', '/')
        if not package_path.exists() or not package_path.is_dir():
            raise ModuleNotFoundError(f"Package '{package_name}' not found.")
        
        modules = []
        for file in package_path.glob("*.py"):
            if file.name != "__init__.py":
                module_name = f"{package_name}.{file.stem}"
                try:
                    module = importlib.import_module(module_name)
                    modules.append(module)
                except Exception as e:
                    print(f"Error importing module '{module_name}': {e}")
        return modules
    
    def list_available_modules(self, package_name):
        """List all available modules in a package."""
        package_path = self.base_path / package_name.replace('.', '/')
        if not package_path.exists() or not package_path.is_dir():
            return []
        
        return [file.stem for file in package_path.glob("*.py") if file.name != "__init__.py"]

# Usage Example:
# mod_manager = ModManager()
# my_module = mod_manager.load("my_package.my_module")