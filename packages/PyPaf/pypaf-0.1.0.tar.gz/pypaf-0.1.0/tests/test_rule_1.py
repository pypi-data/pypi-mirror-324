"""Test Paf Rule 1 formatting"""

import unittest
from paf import Paf

class TestRule1(unittest.TestCase):
    """Test Paf Rule 1"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'organisation_name': "LEDA ENGINEERING LTD",
            'dependent_locality': "APPLEFORD",
            'post_town': "ABINGDON",
            'postcode': "OX14 4PG"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["LEDA ENGINEERING LTD", "APPLEFORD", "ABINGDON", "OX14 4PG"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 1 list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "LEDA ENGINEERING LTD, APPLEFORD, ABINGDON. OX14 4PG"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 1 string format")

if __name__ == '__main__':
    unittest.main()
