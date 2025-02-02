"""Test Paf Rule 5 formatting"""

import unittest
from paf import Paf

class TestRule5(unittest.TestCase):
    """Test Paf Rule 5"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'sub_building_name': "FLAT 1",
            'building_number': "12",
            'thoroughfare_name': "LIME TREE",
            'thoroughfare_descriptor': "AVENUE",
            'post_town': "BRISTOL",
            'postcode': "BS8 4AB"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["FLAT 1", "12 LIME TREE AVENUE", "BRISTOL", "BS8 4AB"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 5 list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "FLAT 1, 12 LIME TREE AVENUE, BRISTOL. BS8 4AB"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 5 string format")

class TestRule5WithConcatenation(unittest.TestCase):
    """Test Paf Rule 5 with Concatenation"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'sub_building_name': "A",
            'building_number': "12",
            'thoroughfare_name': "HIGH",
            'thoroughfare_descriptor': "STREET NORTH",
            'dependent_locality': "COOMBE BISSETT",
            'post_town': "SALISBURY",
            'postcode': "SP5 4NA",
            'concatenation_indicator': "Y"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["12A HIGH STREET NORTH", "COOMBE BISSETT", "SALISBURY", "SP5 4NA"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 5 with concatenate list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "12A HIGH STREET NORTH, COOMBE BISSETT, SALISBURY. SP5 4NA"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 5 with concatenate string format")

if __name__ == '__main__':
    unittest.main()
