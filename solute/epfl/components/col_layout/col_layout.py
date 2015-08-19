# coding: utf-8

from solute.epfl.core import epflcomponentbase


class ColLayout(epflcomponentbase.ComponentContainerBase):
    """

    A layout component that renders child components as cols (using Bootstrap's col layout).

    Use it like this:

    .. code:: python

        col_layout = ColLayout(
            node_list=[
                Text(value="Text 1", cols=6),
                Text(value="Text 2 centered", cols=6, align="center")
            ]
        )


    Every child component is should have the cols attribute indicating the number of cols it
    should use. The cols attribute must a number between 1 and 12. If it is missing, 12 is used.
    
    To create responsive layouts (see http://getbootstrap.com/css/#grid), col classes can be used for 
    a column. For this, a child components can have a col_class attribute ("xs", "sm", "md", "lg")
    indicating the col class (e.g. "col-sm-12", "col-md-6", etc.) for the cols. If the col_class attribute
    is missing for a child component, "md" is used. 
    
    A child component can also optionally have the align attribute ("left", "right" or "center"),
    indicating that it should be aligned in a certain way.

    """

    asset_spec = "solute.epfl.components:col_layout/static"
    css_name = ["col_layout.css"]
    js_name = ["col_layout.js"]
    js_parts = []

    template_name = "col_layout/col_layout.html"

    vertical_center = False  #: If set to true, child components are centered vertically.

    css_cls = None  #: Add the value of css_cls to the css class of the outermost div

    new_style_compo = True
    compo_js_name = 'ColLayout'

    def __init__(self, page, cid, vertical_center=False, css_cls=None, **extra_params):
        """
        A layout component that renders child components as cols (using Bootstrap's col layout).

        Every child component is required to have the cols attribute indicating the number of cols it
        should use. The cols attribute must a number between 1 and 12.
        A child component can also optionally have the text_center attribute (boolean), indicating
        that it should be centered horizontally.

        :param vertical_center: If set to true, child components are centered vertically
        :param css_cls: Add the value of css_cls to the css class of the outermost div
        """
        super(ColLayout, self).__init__(
            page=page, cid=cid,
            vertical_center=vertical_center,
            css_cls=css_cls,
            **extra_params)
