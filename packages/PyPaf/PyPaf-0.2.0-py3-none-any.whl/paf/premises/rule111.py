"""Rule 7"""

from .common import Common

class Rule111(Common):
    """Rule 7 processing"""

    @property
    def premises_rule_attrs(self):
        """Returns premises list"""
        if self.is_exception('sub_building_name'):
            return['sub_name_and_name', 'number_and_thoroughfare_or_locality']
        return ['sub_building_name', 'building_name', 'number_and_thoroughfare_or_locality']

    @property
    def does_premises_include_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return True
