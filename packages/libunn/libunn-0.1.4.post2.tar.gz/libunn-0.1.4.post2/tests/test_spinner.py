import libunn, unittest
class TestSpinner(unittest.TestCase):

    def test_start_function(self):
        self.assertEqual(libunn.spinner.start("Test"), None) 

    def test_stop_function(self):
        self.assertEqual(libunn.spinner.stop(), None) 

if __name__ == "__main__":
    unittest.main()