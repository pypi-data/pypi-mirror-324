"""Test Paf Rule 6 formatting"""

import unittest
from paf import Paf

class TestRule6WithSubBuildingName(unittest.TestCase):
    """Test Paf Rule 6 with Sub-Building Name Exception"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'sub_building_name': "10B",
            'building_name': "BARRY JACKSON TOWER",
            'thoroughfare_name': "ESTONE",
            'thoroughfare_descriptor': "WALK",
            'post_town': "BIRMINGHAM",
            'postcode': "B6 5BA"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["10B BARRY JACKSON TOWER", "ESTONE WALK", "BIRMINGHAM", "B6 5BA"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 6 with sub-building list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "10B BARRY JACKSON TOWER, ESTONE WALK, BIRMINGHAM. B6 5BA"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 6 with sub-building string format")

class TestRule6WithBuildingName(unittest.TestCase):
    """Test Paf Rule 6 with Building Name Exception"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'sub_building_name': "CARETAKERS FLAT",
            'building_name': "110-114",
            'thoroughfare_name': "HIGH",
            'thoroughfare_descriptor': "STREET WEST",
            'post_town': "BRISTOL",
            'postcode': "BS1 2AW"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["CARETAKERS FLAT", "110-114 HIGH STREET WEST", "BRISTOL", "BS1 2AW"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 6 with building list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "CARETAKERS FLAT, 110-114 HIGH STREET WEST, BRISTOL. BS1 2AW"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 6 with building string format")

class TestRule6(unittest.TestCase):
    """Test Paf Rule 6 without Exception"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'sub_building_name': "STABLES FLAT",
            'building_name': "THE MANOR",
            'thoroughfare_name': "UPPER",
            'thoroughfare_descriptor': "HILL",
            'post_town': "HORLEY",
            'postcode': "RH6 0HP"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["STABLES FLAT", "THE MANOR", "UPPER HILL", "HORLEY", "RH6 0HP"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 6 list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "STABLES FLAT, THE MANOR, UPPER HILL, HORLEY. RH6 0HP"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 6 string format")

if __name__ == '__main__':
    unittest.main()
