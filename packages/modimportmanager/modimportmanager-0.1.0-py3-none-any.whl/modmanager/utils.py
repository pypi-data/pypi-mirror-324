# File: modmanager/utils.py
def print_hello():
    print("Hello from ModManager!")

# File: tests/test_modmanager.py
import unittest
from modmanager import ModManager

class TestModManager(unittest.TestCase):
    def setUp(self):
        self.mod_manager = ModManager()
    
    def test_list_modules(self):
        modules = self.mod_manager.list_available_modules("modmanager")
        self.assertIsInstance(modules, list)

if __name__ == "__main__":
    unittest.main()