"""Test Paf Exception II formatting"""

import unittest
from paf import Paf

class TestExceptionII(unittest.TestCase):
    """Test Paf Exception II"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'building_name': "12A",
            'thoroughfare_name': "UPPERKIRKGATE",
            'post_town': "ABERDEEN",
            'postcode': "AB10 1BA"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["12A UPPERKIRKGATE", "ABERDEEN", "AB10 1BA"]
        self.assertEqual(self.paf.list(), address, "Incorrect Exception II list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "12A UPPERKIRKGATE, ABERDEEN. AB10 1BA"
        self.assertEqual(str(self.paf), address, "Incorrect Exception II string format")

if __name__ == '__main__':
    unittest.main()
