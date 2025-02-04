"""Rule 5"""

from .common import Common

class Rule101(Common):
    """Rule 5 processing"""

    @property
    def premises_rule_attrs(self):
        """Returns premises list"""
        if getattr(self, 'concatenation_indicator', '') == 'Y':
            return ['number_sub_name_and_thoroughfare_or_locality']
        return ['sub_building_name', 'number_and_thoroughfare_or_locality']

    @property
    def does_premises_include_first_thoroughfare_or_locality(self):
        """Returns if premises includes first thoroughfare or locality"""
        return True

    @property
    def building_number_and_sub_building_name(self):
        """Returns building number and sub-building name"""
        return self._concatenate(['building_number', 'sub_building_name'], '')

    @property
    def number_sub_name_and_thoroughfare_or_locality(self):
        """Returns building number, sub-building name and first thoroughfare or locality"""
        return(self._concatenate([
            'building_number_and_sub_building_name', 'first_thoroughfare_or_locality'
            ]))
