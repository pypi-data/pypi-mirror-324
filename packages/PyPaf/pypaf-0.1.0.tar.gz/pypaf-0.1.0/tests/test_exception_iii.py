"""Test Paf Exception III formatting"""

import unittest
from paf import Paf

class TestExceptionIII(unittest.TestCase):
    """Test Paf Exception III"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'building_name': "K",
            'thoroughfare_name': "PORTLAND",
            'thoroughfare_descriptor': "ROAD",
            'post_town': "DORKING",
            'postcode': "RH4 1EW"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["K PORTLAND ROAD", "DORKING", "RH4 1EW"]
        self.assertEqual(self.paf.list(), address, "Incorrect Exception III list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "K PORTLAND ROAD, DORKING. RH4 1EW"
        self.assertEqual(str(self.paf), address, "Incorrect Exception III string format")

if __name__ == '__main__':
    unittest.main()
