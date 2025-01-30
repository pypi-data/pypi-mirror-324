import unittest
import tkinter as tk
from src.ui.advanced_dashboard import PumpQDashboard

class TestAdvancedDashboard(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.dashboard = PumpQDashboard(self.root)
    
    def test_dashboard_initialization(self):
        """اختبار تهيئة لوحة المعلومات"""
        self.assertIsNotNone(self.dashboard)
        self.assertTrue(hasattr(self.dashboard, 'sidebar'))
        self.assertTrue(hasattr(self.dashboard, 'main_content'))
    
    def test_sidebar_menu(self):
        """اختبار قائمة التنقل الجانبية"""
        sidebar_buttons = [btn for btn in self.dashboard.sidebar.winfo_children() if isinstance(btn, tk.Button)]
        self.assertTrue(len(sidebar_buttons) > 0)
    
    def test_dashboard_view(self):
        """اختبار عرض لوحة المعلومات"""
        self.assertTrue(hasattr(self.dashboard, 'create_dashboard_view'))
    
    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
