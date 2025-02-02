"""Test Paf Mainfile formatting"""

import unittest
from paf import Paf

class TestMainfile(unittest.TestCase):
    """Test Paf Mainfile"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'organisation_name': "SOUTH LANARKSHIRE COUNCIL",
            'department_name': "HEAD START",
            'sub_building_name': "UNIT 1",
            'building_name': "BLOCK 3",
            'thoroughfare_name': "THIRD",
            'thoroughfare_descriptor': "ROAD",
            'double_dependent_locality': "BLANTYRE INDUSTRIAL ESTATE",
            'dependent_locality': "BLANTYRE",
            'post_town': "GLASGOW",
            'postcode': "G72 0UP"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = [
            "SOUTH LANARKSHIRE COUNCIL",
            "HEAD START",
            "UNIT 1",
            "BLOCK 3",
            "THIRD ROAD",
            "BLANTYRE INDUSTRIAL ESTATE",
            "BLANTYRE",
            "GLASGOW",
            "G72 0UP"
            ]
        self.assertEqual(self.paf.list(), address, "Incorrect Mainfile list format")

    def test_string(self):
        """Test conversion to a string"""
        address = (
            "SOUTH LANARKSHIRE COUNCIL, "
            "HEAD START, "
            "UNIT 1, "
            "BLOCK 3, "
            "THIRD ROAD, "
            "BLANTYRE INDUSTRIAL ESTATE, "
            "BLANTYRE, "
            "GLASGOW. "
            "G72 0UP"
            )
        self.assertEqual(str(self.paf), address, "Incorrect Mainfile string format")

if __name__ == '__main__':
    unittest.main()
