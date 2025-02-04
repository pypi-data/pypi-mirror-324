"""Rule 4"""

from .common import Common

class Rule011(Common):
    """Rule 4 processing"""

    @property
    def premises_rule_attrs(self):
        """Returns premises list"""
        return ['building_name', 'number_and_thoroughfare_or_locality']

    @property
    def does_premises_include_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return True
