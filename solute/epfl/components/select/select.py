from solute.epfl.components.form.inputbase import FormInputBase


class Select(FormInputBase):
    """
    A form drop-down select input.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[Select(label="Select color:",
                                      name="color",
                                      default="black",
                                      options=[{"value":"white","visual":"White"},{"value":"red","visual":"Red"},{"value":"black","visual":"Black"}])])

    """

    template_name = "select/select.html"
    js_name = FormInputBase.js_name + [("solute.epfl.components:select/static", "select.js")]
    js_parts = []
    css_name = FormInputBase.css_name + [("solute.epfl.components:select/static", "select.css")]
    compo_state = FormInputBase.compo_state + ['options']

    options = None  #: A list if options for the select input.

    validation_type = 'text'  #: Validate input as text.
    layout_vertical = False  #: Use the vertical layout instead of the default horizontal.

    new_style_compo = True
    compo_js_name = 'Select'
    compo_js_params = ['fire_change_immediately', 'submit_form_on_enter']

    def __init__(self, page, cid, options=None, layout_vertical=None, **extra_params):
        """Select form element that gives the selected option as its value.

        :param options: A list if options for the select input.
        :param layout_vertical: Use the vertical layout instead of the default horizontal.
        """
        super(Select, self).__init__(page, cid, options=options, layout_vertical=layout_vertical, **extra_params)
