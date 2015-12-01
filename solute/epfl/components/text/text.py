from solute.epfl.core import epflcomponentbase


class Text(epflcomponentbase.ComponentBase):
    template_name = "text/text.html"
    value = None  #: The textual value of this component.
    verbose = False  #: A verbose text component can determine its own html tag.
    tag = None  #: HTML tag to use on verbose text components.
    tag_class = None  #: css class to use on verbose text components with a custom tag.
    #: If set, display a label before the text. In this case, the :attr:`verbose` attribute is not needed and
    #: will be neglected, since verbose tags will be rendered anyway.
    label = None
    #: If set to True, the label will be rendered above the text instead of left before the text.
    #: This attribute is only regarded if the :attr:`label` attribute is set.
    layout_vertical = False
    compo_state = epflcomponentbase.ComponentBase.compo_state + ["value", "tag", "tag_class", "verbose", "label"]

    def __init__(self, page, cid, value=None, verbose=False, tag=None, tag_class=False, label=None,
                 layout_vertical=False, **extra_params):
        """A very basic component to display text values.

        :param value: The textual value of this component.
        :param verbose: A verbose text component can determine its own html tag.
        :param tag: HTML tag to use on verbose text components.
        :param tag_class: css class to use on verbose text components with a custom tag.
        :param label: Label to be used for this text component.
        :param layout_vertical:
        """
        super(Text, self).__init__()
