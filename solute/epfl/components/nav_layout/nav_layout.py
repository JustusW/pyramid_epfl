# coding: utf-8

from solute.epfl.core import epflcomponentbase


class NavLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "nav_layout/nav_layout.html"
    asset_spec = 'solute.epfl.components:nav_layout/static'

    css_name = epflcomponentbase.ComponentBase.css_name + ['nav_layout.css']

    compo_state = ['links', 'title', 'img']

    img = None  #: Logo to be used on the top left.
    title = None  #: Title to be displayed on the top left.

    def __init__(self, page, cid, title=None, img=None, **extra_params):
        """Topnav with optional title and image.

         :param img: Logo to be used on the top left.
         :param title: Title to be displayed on the top left.
        """
        super(NavLayout, self).__init__()
