"""Rule 2"""

from .common import Common

class Rule001(Common):
    """Rule 2 processing"""

    @property
    def premises_rule_attrs(self):
        """Returns premises list"""
        return ['number_and_thoroughfare_or_locality']

    @property
    def does_premises_include_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return True
