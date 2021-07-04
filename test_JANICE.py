import JANICE
import unittest

class test_JANICE(unittest.TestCase):
    def test_get_connection_object(self):
        pass

    def test_setup(self):
        pass

    def test_check_safe_environment(self):
        tv = JANICE.check_safe_environment()
        self.assertTrue(tv)

    def test_activate_relay(self):
        tv = JANICE.activate_relay(1,1)
        self.assertTrue(tv)

    def test_get_data_from_conn(self):
        pass
    
    def test_log_data(self):
        pass
    


if __name__ == '__main__':
    unittest.main()