"""Lineable Mixin"""

from itertools import chain
from .thoroughfare_locality import ThoroughfareLocalityMixin

class LineableMixin(ThoroughfareLocalityMixin):
    """Converts Paf address elements into list of address lines, excluding postcode"""

    @classmethod
    @property
    def lines_attrs(cls):
        """Returns Paf address line attributes"""
        return(
            cls.organisation_attrs +
                ['po_box', 'premises', 'thoroughfares_and_localities', 'post_town']
            )

    @property
    def lines(self):
        """Returns Paf as list of address lines"""
        lines = list(filter(None, [getattr(self, k, None) for k in self.__class__.lines_attrs]))
        return list(chain(*[line if isinstance(line, list) else [line] for line in lines]))

    @property
    def po_box(self):
        """Returns PO Box"""
        return '' if self.is_empty('po_box_number') else f"PO BOX {getattr(self, 'po_box_number')}"
