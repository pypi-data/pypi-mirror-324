"""Rule 6"""

from .common import Common

class Rule110(Common):
    """Rule 6 processing"""

    @property
    def premises_rule_attrs(self):
        """Returns premises list"""
        if self.is_exception('sub_building_name'):
            return['sub_name_and_name']
        if self.is_exception('building_name'):
            return['sub_building_name', 'name_and_thoroughfare_or_locality']
        return ['sub_building_name', 'building_name']

    @property
    def does_premises_include_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return (not self.is_exception('sub_building_name')) and self.is_exception('building_name')
