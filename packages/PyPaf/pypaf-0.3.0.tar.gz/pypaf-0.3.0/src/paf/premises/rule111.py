"""Rule 7"""

from .common import Common

class Rule111(Common):
    """Rule 7 processing"""

    @property
    def premises_rule_attrs(self):
        """Returns premises list"""
        if self.is_zero_building_number:
            return['sub_name_comma_name']
        if self.is_exception('sub_building_name'):
            return['sub_name_and_name', 'number_and_thoroughfare_or_locality']
        return ['sub_building_name', 'building_name', 'number_and_thoroughfare_or_locality']

    @property
    def does_premises_include_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return not self.is_zero_building_number

    @property
    def is_zero_building_number(self):
        """Returns if building number is a 0"""
        return getattr(self, 'building_number', '') == "0"

    @property
    def sub_name_comma_name(self):
        """Returns sub-building name and building name concatenated with a comma"""
        return self._concatenate(['sub_building_name', 'building_name'], ', ')
