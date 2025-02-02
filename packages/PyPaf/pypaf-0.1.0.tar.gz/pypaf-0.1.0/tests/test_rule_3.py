"""Test Paf Rule 3 formatting"""

import unittest
from paf import Paf

class TestRule3WithBuildingName(unittest.TestCase):
    """Test Paf Rule 3 with Building Name Exception"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'building_name': "1A",
            'dependent_thoroughfare_name': "SEASTONE",
            'dependent_thoroughfare_descriptor': "COURT",
            'thoroughfare_name': "STATION",
            'thoroughfare_descriptor': "ROAD",
            'post_town': "HOLT",
            'postcode': "NR25 7HG"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["1A SEASTONE COURT", "STATION ROAD", "HOLT", "NR25 7HG"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 3 with building list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "1A SEASTONE COURT, STATION ROAD, HOLT. NR25 7HG"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 3 with building string format")

class TestRule3WithoutBuildingName(unittest.TestCase):
    """Test Paf Rule 3 without Building Name Exception"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'building_name': "THE MANOR",
            'thoroughfare_name': "UPPER",
            'thoroughfare_descriptor': "ROAD",
            'post_town': "HORLEY",
            'postcode': "RH6 0HP"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["THE MANOR", "UPPER ROAD", "HORLEY", "RH6 0HP"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 3 without building list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "THE MANOR, UPPER ROAD, HORLEY. RH6 0HP"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 3 without building string format")

class TestRule3WithSplit(unittest.TestCase):
    """Test Paf Rule 3 with Split Exception"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'organisation_name': "S D ALCOTT FLORISTS",
            'building_name': "FLOWER HOUSE 189A",
            'thoroughfare_name': "PYE GREEN",
            'thoroughfare_descriptor': "ROAD",
            'post_town': "CANNOCK",
            'postcode': "WS11 5SB"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = [
            "S D ALCOTT FLORISTS",
            "FLOWER HOUSE",
            "189A PYE GREEN ROAD",
            "CANNOCK",
            "WS11 5SB"
            ]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 3 with split list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "S D ALCOTT FLORISTS, FLOWER HOUSE, 189A PYE GREEN ROAD, CANNOCK. WS11 5SB"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 3 with split string format")

class TestRule3WithoutSplit(unittest.TestCase):
    """Test Paf Rule 3 without Split Exception"""

    def setUp(self):
        """Set up Paf instance"""
        self.paf = Paf({
            'organisation_name': "JAMES VILLA HOLIDAYS",
            'building_name': "CENTRE 30",
            'thoroughfare_name': "ST LAURENCE",
            'thoroughfare_descriptor': "AVENUE",
            'post_town': "GRAFTON",
            'postcode': "ME16 0LP"
            })

    def test_list(self):
        """Test conversion to an list"""
        address = ["JAMES VILLA HOLIDAYS", "CENTRE 30", "ST LAURENCE AVENUE", "GRAFTON", "ME16 0LP"]
        self.assertEqual(self.paf.list(), address, "Incorrect Rule 3 without split list format")

    def test_string(self):
        """Test conversion to a string"""
        address = "JAMES VILLA HOLIDAYS, CENTRE 30, ST LAURENCE AVENUE, GRAFTON. ME16 0LP"
        self.assertEqual(str(self.paf), address, "Incorrect Rule 3 without split string format")

if __name__ == '__main__':
    unittest.main()
