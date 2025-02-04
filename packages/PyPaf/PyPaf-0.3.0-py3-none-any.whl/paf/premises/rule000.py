"""Rule 1"""

from .common import Common

class Rule000(Common):
    """Rule 1 processing"""

    @property
    def premises_rule_attrs(self):
        """Returns premises list"""
        return []

    @property
    def does_premises_include_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return False
