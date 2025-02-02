"""Test Paf Rule 2 formatting"""

import unittest
from paf import Paf

class TestRule2(unittest.TestCase):
    """Test Paf Rule 2"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'building_number': "1",
            'thoroughfare_name': "ACACIA",
            'thoroughfare_descriptor': "AVENUE",
            'post_town': "ABINGDON",
            'postcode': "OX14 4PG"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["1 ACACIA AVENUE", "ABINGDON", "OX14 4PG"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 2 list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "1 ACACIA AVENUE, ABINGDON. OX14 4PG"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 2 string format")

if __name__ == '__main__':
    unittest.main()
