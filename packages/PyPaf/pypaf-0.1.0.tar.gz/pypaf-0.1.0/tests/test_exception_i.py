"""Test Paf Exception I formatting"""

import unittest
from paf import Paf

class TestExceptionI(unittest.TestCase):
    """Test Paf Exception I"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'building_name': "1-2",
            'thoroughfare_name': "NURSERY",
            'thoroughfare_descriptor': "LANE",
            'dependent_locality': "PENN",
            'post_town': "HIGH WYCOMBE",
            'postcode': "HP10 8LS"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["1-2 NURSERY LANE", "PENN", "HIGH WYCOMBE", "HP10 8LS"]
        self.assertEqual(self.paf.list(), address, "Incorrect Exception I list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "1-2 NURSERY LANE, PENN, HIGH WYCOMBE. HP10 8LS"
        self.assertEqual(str(self.paf), address, "Incorrect Exception I string format")

if __name__ == '__main__':
    unittest.main()
