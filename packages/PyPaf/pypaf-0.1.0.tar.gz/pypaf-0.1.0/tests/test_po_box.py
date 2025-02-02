"""Test Paf PO Box formatting"""

import unittest
from paf import Paf

class TestPoBox(unittest.TestCase):
    """Test Paf PO Box"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'po_box_number': "61",
            'post_town': "FAREHAM",
            'postcode': "PO14 1UX"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["PO BOX 61", "FAREHAM", "PO14 1UX"]
        self.assertEqual(self.paf.list(), address, "Incorrect PO Box list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "PO BOX 61, FAREHAM. PO14 1UX"
        self.assertEqual(str(self.paf), address, "Incorrect PO Box string format")

if __name__ == '__main__':
    unittest.main()
