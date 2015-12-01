# coding: utf-8


from solute.epfl.core.epflcomponentbase import ComponentBase
from solute.epfl.core import epflutil


class Badge(ComponentBase):
    """
    Simple Badge Compo uses bootstrap badge

    example: http://getbootstrap.com/components/#badges
    """

    asset_spec = "solute.epfl.components:badge/static"

    template_name = "badge/badge.html"
    js_name = ["badge.js"]
    css_name = ["badge.css"]

    compo_state = ["value"]
    
    value = None  #: The value will be converted to string and shown inside the Badge.

    def __init__(self, page, cid, value=None, **extra_params):
        """Simple bootstrap badge.
        Usage: components.Badge(value=10)

        :param value: The value will be converted to string and shown inside the Badge.
        """
        super(Badge, self).__init__(page, cid, value=value, **extra_params)
