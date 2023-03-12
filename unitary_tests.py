import unittest
from tkinter import *

class TestMenu(unittest.TestCase):
    def test_add_command(self):
        root = Tk()
        #menu_section = MenuSection(Menu(root))
        #menu_section.add_command("test", lambda: None)
        #self.assertEqual(len(menu_section.menu.index("end")), 1)

    def test_add_section(self):
        root = Tk()
        menu = Menu(root)
        #menu_section = MenuSection(menu)
        #menu.add_cascade(menu=menu_section.menu, label="Test")
        self.assertEqual(len(menu.index("end")), 1)
