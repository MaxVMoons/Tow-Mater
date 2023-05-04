import unittest
import controller

class TestRacer(unittest.TestCase):
    
    def test_stick(self):
        self.assertTrue(controller.getStickAngleAlt(-1) == 180)
        self.assertTrue(controller.getStickAngleAlt(0) == 90)
        self.assertTrue(controller.getStickAngleAlt(1) == 0)
    
    def test_update(self):
        self.assertEqual(controller.update_last_value(0.7, 0.9, 0.15, 2), 0.9)
        self.assertEqual(controller.update_last_value(0.35, -0.5, 0.1, 2), 0.35)
        self.assertEqual(controller.update_last_value(0.88, 0.77, 0.2, 2), 0.77)
        self.assertEqual(controller.update_last_value(0.46, -0.99, 0.35, 2), 0.46)
        self.assertEqual(controller.update_last_value(0.45, None, 0.1, 2), 0.45)

if __name__ == '__main__':
    unittest.main()
