from solute.epfl.components.form.form import FormInputBase


class Checkbox(FormInputBase):

    """
    A form checkbox input.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[Checkbox(label="I agree to the terms and conditions.", name="toc_agreed")])

    """

    template_name = "checkbox/checkbox.html"

    validation_type = 'bool'
    validation_helper = FormInputBase.validation_helper[:]
    validation_helper.append(
        (lambda x: ((not x.mandatory) or x.value), 'Mandatory field not checked.'))

    #: If set to True, label and checkbox are not splitted to different bootstrap rows,
    # but placed directly next to each other.
    compact = False

    #: If set to True, this checkbox belongs to a group of checkboxes where always just one can be checked.
    # Note that to enable proper functionality of grouped option you have to set fire_change_immediately to True.
    grouped = False

    #: A list of checkbox-cids. If grouped is set to true, all cids in the group list will form a checkbox group
    # where only one checkbox can be checked at a time.
    group = []

    js_parts = FormInputBase.js_parts[:]
    js_parts.extend(['checkbox/checkbox.js'])
    js_name = FormInputBase.js_name + [("solute.epfl.components:checkbox/static", "checkbox.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:checkbox/static", "checkbox.css")]

    def handle_change(self, value):
        self.value = value
        if not self.grouped and len(self.group) > 0:
            # for grouped checkboxes the group has to contain at least 1 other checkbox
            return
        group = self.group
        if value is True:
            for chbox in group:
                check_box = getattr(self.page, chbox)
                check_box.handle_change(False)
        self.redraw()
