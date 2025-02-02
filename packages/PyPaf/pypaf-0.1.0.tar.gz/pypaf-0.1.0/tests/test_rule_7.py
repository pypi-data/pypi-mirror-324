"""Test Paf Rule 7 formatting"""

import unittest
from paf import Paf

class TestRule7WithSubBuildingName(unittest.TestCase):
    """Test Paf Rule 7 with Sub-Building Name Exception"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'sub_building_name': "2B",
            'building_name': "THE TOWER",
            'building_number': "27",
            'thoroughfare_name': "JOHN",
            'thoroughfare_descriptor': "STREET",
            'post_town': "WINCHESTER",
            'postcode': "SO23 9AP"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["2B THE TOWER", "27 JOHN STREET", "WINCHESTER", "SO23 9AP"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 7 with sub-building list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "2B THE TOWER, 27 JOHN STREET, WINCHESTER. SO23 9AP"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 7 with sub-building string format")

class TestRule7(unittest.TestCase):
    """Test Paf Rule 7 without Exception"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'sub_building_name': "BASEMENT FLAT",
            'building_name': "VICTORIA HOUSE",
            'building_number': "15",
            'thoroughfare_name': "THE",
            'thoroughfare_descriptor': "STREET",
            'post_town': "CORYTON",
            'postcode': "BP23 6AA"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["BASEMENT FLAT", "VICTORIA HOUSE", "15 THE STREET", "CORYTON", "BP23 6AA"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 7 list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "BASEMENT FLAT, VICTORIA HOUSE, 15 THE STREET, CORYTON. BP23 6AA"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 7 string format")

if __name__ == '__main__':
    unittest.main()
