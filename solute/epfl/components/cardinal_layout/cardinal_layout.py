# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase


class CardinalLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "cardinal_layout/cardinal_layout.html"
    asset_spec = "solute.epfl.components:cardinal_layout/static"

    compo_state = ['constrained']

    _cardinal_components = None  #: Cache for the slotted components.
    constrained = None  #: Constrain the layout to the center of the screen.
    plain = []  #: List of slots to be rendered as plain divs.
    css_cls = None  #: Add the value of css_cls to the css class of the outermost div

    def __init__(self, page, cid, constrained=None, plain=None, **extra_params):
        """A Layout component that displays it's children in panels for the four cardinal directions or a center panel.

        :param constrained: If true the Cardinal Layout will restrict itself to the center of the screen.
        :param plain: List of slots to be rendered as plain divs.
        """
        super(CardinalLayout, self).__init__(page, cid, constrained=constrained, plain=plain, **extra_params)

    def cardinal_components(self, direction='center'):
        if self._cardinal_components is None:
            self._cardinal_components = {'center': [],
                                         'north': [],
                                         'east': [],
                                         'south': [],
                                         'west': []}
            for compo in self.components:
                self._cardinal_components.setdefault(getattr(compo, 'container_slot', None) or 'center', []).append(
                    compo)

        return self._cardinal_components.get(direction, [])

    def has_cardinal(self, direction):
        return len(self.cardinal_components(direction)) > 0
