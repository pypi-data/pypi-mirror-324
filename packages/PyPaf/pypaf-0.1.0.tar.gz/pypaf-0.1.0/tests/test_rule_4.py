"""Test Paf Rule 4 formatting"""

import unittest
from paf import Paf

class TestRule4(unittest.TestCase):
    """Test Paf Rule 4"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'building_name': "VICTORIA HOUSE",
            'building_number': "15",
            'thoroughfare_name': "THE",
            'thoroughfare_descriptor': "STREET",
            'post_town': "CHRISTCHURCH",
            'postcode': "BH23 6AA"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["VICTORIA HOUSE", "15 THE STREET", "CHRISTCHURCH", "BH23 6AA"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 4 list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "VICTORIA HOUSE, 15 THE STREET, CHRISTCHURCH. BH23 6AA"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 4 string format")

if __name__ == '__main__':
    unittest.main()
