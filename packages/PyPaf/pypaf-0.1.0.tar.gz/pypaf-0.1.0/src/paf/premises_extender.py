"""Premises Extender Mixin"""

import sys
from .attribute import AttributeMixin
from .premises.rule000 import Rule000 # pylint: disable=unused-import
from .premises.rule001 import Rule001 # pylint: disable=unused-import
from .premises.rule010 import Rule010 # pylint: disable=unused-import
from .premises.rule011 import Rule011 # pylint: disable=unused-import
from .premises.rule101 import Rule101 # pylint: disable=unused-import
from .premises.rule110 import Rule110 # pylint: disable=unused-import
from .premises.rule111 import Rule111 # pylint: disable=unused-import

class PremisesExtenderMixin(AttributeMixin):
    """Dynamic Premises processing"""

    @property
    def premises_rule(self):
        """Returns premises rule class"""
        rule = ''.join(['0' if self.is_empty(k) else '1' for k in self.__class__.premises_attrs])
        return getattr(sys.modules[__name__], 'Rule' + rule)

    def extend_premises(self):
        """Dynamically extends instance with appropriate premises rule"""
        base_cls = self.__class__
        self.__class__ = type(base_cls.__name__, (base_cls, self.premises_rule), {})
