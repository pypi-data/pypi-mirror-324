"""Paf"""

from .lineable import LineableMixin

class Paf(LineableMixin):
    """Main Paf class"""

    def __init__(self, args):
        """Initialise Paf address elements"""
        for key in self.__class__.attrs:
            setattr(self, key, '')
        for key, val in args.items():
            if hasattr(self, key):
                setattr(self, key, val)
        self.extend_premises()

    def __repr__(self):
        """Return full representation of Paf"""
        args = {k: getattr(self, k) for k in self.__class__.attrs if getattr(self, k, None)}
        return self.__class__.__name__ + '(' + str(args) + ')'

    def __str__(self):
        """Return Paf as string"""
        line = ', '.join(self.lines)
        if self.is_empty('postcode'):
            return line
        return '. '.join([line] + [getattr(self, 'postcode')])

    def list(self):
        """Return Paf as list of strings"""
        if self.is_empty('postcode'):
            return self.lines
        return self.lines + [getattr(self, 'postcode')]
