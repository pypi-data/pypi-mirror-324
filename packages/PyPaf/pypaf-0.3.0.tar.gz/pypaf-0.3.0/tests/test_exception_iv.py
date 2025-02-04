"""Test Paf Exception IV formatting"""

import unittest
from paf import Paf

class TestExceptionIVUnit(unittest.TestCase):
    """Test Paf Exception IV Unit"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'organisation_name': "THE TAMBOURINE WAREHOUSE",
            'building_name': "UNIT 1-3",
            'dependent_thoroughfare_name': "INDUSTRIAL",
            'dependent_thoroughfare_descriptor': "ESTATE",
            'thoroughfare_name': "TAME",
            'thoroughfare_descriptor': "ROAD",
            'post_town': "LONDON",
            'postcode': "E6 7HS"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = [
            "THE TAMBOURINE WAREHOUSE",
            "UNIT 1-3",
            "INDUSTRIAL ESTATE",
            "TAME ROAD",
            "LONDON",
            "E6 7HS"
            ]
        self.assertEqual(self.paf.list(), address, "Incorrect Exception IV Unit list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "THE TAMBOURINE WAREHOUSE, UNIT 1-3, INDUSTRIAL ESTATE, TAME ROAD, LONDON. E6 7HS"
        self.assertEqual(self.paf.str(), address, "Incorrect Exception IV Unit string format")

class TestExceptionIVStall(unittest.TestCase):
    """Test Paf Exception IV Stall"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'organisation_name': "QUIRKY CANDLES LTD",
            'building_name': "STALL 4",
            'thoroughfare_name': "MARKET",
            'thoroughfare_descriptor': "SQUARE",
            'post_town': "LIVERPOOL",
            'postcode': "L8 1LH"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = [
            "QUIRKY CANDLES LTD",
            "STALL 4",
            "MARKET SQUARE",
            "LIVERPOOL",
            "L8 1LH"
            ]
        self.assertEqual(self.paf.list(), address, "Incorrect Exception IV Stall list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "QUIRKY CANDLES LTD, STALL 4, MARKET SQUARE, LIVERPOOL. L8 1LH"
        self.assertEqual(self.paf.str(), address, "Incorrect Exception IV Stall string format")

class TestExceptionIVRearOf(unittest.TestCase):
    """Test Paf Exception IV Rear Of"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'organisation_name': "FIONA'S FLOWERS",
            'building_name': "REAR OF 5A",
            'thoroughfare_name': "HIGH",
            'thoroughfare_descriptor': "STREET",
            'post_town': "GATESHEAD",
            'postcode': "NE8 1BH"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = [
            "FIONA'S FLOWERS",
            "REAR OF 5A",
            "HIGH STREET",
            "GATESHEAD",
            "NE8 1BH"
            ]
        self.assertEqual(self.paf.list(), address, "Incorrect Exception IV Rear Of list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "FIONA'S FLOWERS, REAR OF 5A, HIGH STREET, GATESHEAD. NE8 1BH"
        self.assertEqual(self.paf.str(), address, "Incorrect Exception IV Rear Of string format")

if __name__ == '__main__':
    unittest.main()
