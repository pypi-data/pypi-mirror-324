"""Thoroughfare and Locality Mixin"""

from .premises_extender import PremisesExtenderMixin

class ThoroughfareLocalityMixin(PremisesExtenderMixin):
    """Thoroughfare and locality processing"""

    @classmethod
    @property
    def thoroughfare_and_locality_attrs(cls):
        """Returns Paf address line attributes"""
        return ['dependent_thoroughfare', 'thoroughfare'] + cls.locality_attrs

    @property
    def thoroughfares_and_localities(self):
        """Returns thoroughfares and localities list"""
        attrs = self.__class__.thoroughfare_and_locality_attrs
        return [getattr(self, k) for k in attrs if not self.is_used_or_empty(k)]

    @property
    def dependent_thoroughfare(self):
        """Returns dependent thoroughfare"""
        return self._concatenate(self.__class__.dependent_thoroughfare_attrs)

    @property
    def thoroughfare(self):
        """Returns thoroughfare"""
        return self._concatenate(self.__class__.thoroughfare_attrs)

    @property
    def first_thoroughfare_or_locality_attr(self):
        """Returns name of first populated thoroughfare or locality attribute"""
        for k in self.__class__.thoroughfare_and_locality_attrs:
            if not self.is_empty(k):
                return k
        return None

    @property
    def first_thoroughfare_or_locality(self):
        """Returns first populated thoroughfare or locality value"""
        attr = self.first_thoroughfare_or_locality_attr
        return getattr(self, attr) if attr is not None else ''

    def is_used_or_empty(self, attr):
        """Returns if attribute value is empty or has already been used"""
        if self.is_empty(attr):
            return True
        return(
            attr == self.first_thoroughfare_or_locality_attr and
                self.does_premises_include_first_thoroughfare_or_locality
            )
