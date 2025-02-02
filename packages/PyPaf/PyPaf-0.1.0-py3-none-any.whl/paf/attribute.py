"""Attribute Mixin"""

class AttributeMixin():
    """Base Paf address elements and derived properties"""

    @classmethod
    @property
    def organisation_attrs(cls):
        """Returns Paf organisation elements"""
        return ['organisation_name', 'department_name']

    @classmethod
    @property
    def premises_attrs(cls):
        """Returns Paf premises elements"""
        return ['sub_building_name', 'building_name', 'building_number']

    @classmethod
    @property
    def dependent_thoroughfare_attrs(cls):
        """Returns Paf dependent thoroughfare elements"""
        return ['dependent_thoroughfare_name', 'dependent_thoroughfare_descriptor']

    @classmethod
    @property
    def thoroughfare_attrs(cls):
        """Returns Paf thoroughfare elements"""
        return ['thoroughfare_name', 'thoroughfare_descriptor']

    @classmethod
    @property
    def locality_attrs(cls):
        """Returns Paf localoty elements"""
        return ['double_dependent_locality', 'dependent_locality']

    @classmethod
    @property
    def post_attrs(cls):
        """Returns Paf post elements"""
        return ['post_town', 'postcode']

    @classmethod
    @property
    def other_attrs(cls):
        """Returns Paf other elements"""
        return ['po_box_number', 'udprn', 'concatenation_indicator']

    @classmethod
    @property
    def attrs(cls):
        """Returns all Paf address elements"""
        return(
            cls.organisation_attrs +
                cls.premises_attrs +
                cls.dependent_thoroughfare_attrs +
                cls.thoroughfare_attrs +
                cls.locality_attrs +
                cls.post_attrs +
                cls.other_attrs
            )

    def is_empty(self, attr):
        """Returns if attribute value is empty"""
        if getattr(self, attr, '') == '':
            return True
        return False
