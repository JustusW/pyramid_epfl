# * encoding: utf-8

from solute.epfl.components.text_input.text_input import TextInput


class PasswordInput(TextInput):
    #: Set to true if input field should be used as a password field
    password = True

    def __init__(self, page, cid,
                 label=None,
                 name=None,
                 value=None,
                 default=None,
                 placeholder=None,
                 readonly=False,
                 validation_error='',
                 mandatory=False,
                 submit_form_on_enter=False,
                 input_focus=False,
                 fire_change_immediately=False,
                 compo_col=12,
                 label_col=2,
                 layout_vertical=False,
                 label_style=None,
                 input_style=None,
                 typeahead=False,
                 max_length=None,
                 show_count=False,
                 password=False,
                 layover_icon=None,
                 date=False,
                 **extra_params):
        """
        A Password input this is a convenience component for textinput which overrides the password flag to true.

        :param label: Optional label describing the input field
        :param name: An element without a name cannot have a value
        :param value: The actual value of the input element that is posted upon form submission
        :param default: Default value that may be pre-set or pre-selected
        :param placeholder: Placeholder text that can be displayed if supported by the input
        :param readonly: Set to true if input cannot be changed and is displayed in readonly mode
        :param validation_error: Set during call of :func:`validate` with an error message if validation fails
        :param mandatory: Set to true if value has to be provided for this element in order to yield a valid form
        :param submit_form_on_enter: If true, underlying form is submitted upon enter key in this input
        :param input_focus: Set focus on this input when component is displayed
        :param fire_change_immediately: Set to true if input change events should be fired immediately to the server. Otherwise, change events are fired upon the next immediate epfl event
        :param compo_col: Set the width of the complete input component (default: max: 12)
        :param label_col: Set the width of the complete input component (default: 2)
        :param layout_vertical: Set to true if label should be displayed on top of the input and not on the left before it
        :param label_style: Can be used to add additional css styles for the label
        :param input_style: Can be used to add additional css styles for the input
        :param typeahead: Set to true if typeahead should be provided by the input (if supported)
        :param max_length: Maximum length for the input
        :param show_count: Set to true to show a input counter right to the field. Requires a max_length to be set
        :param password: Set to true if input field should be used as a password field
        :param layover_icon: Optional font-awesome icon to be rendered as a layover icon above the input field (aligned to the right)
        :param date: Set to true if input field should be a datetime picker (using jquery-datetimepicker plugin)
        """
        super(PasswordInput, self).__init__(page, cid,
                                            label=label,
                                            name=name,
                                            value=value,
                                            default=default,
                                            placeholder=placeholder,
                                            readonly=readonly,
                                            validation_error=validation_error,
                                            mandatory=mandatory,
                                            submit_form_on_enter=submit_form_on_enter,
                                            input_focus=input_focus,
                                            fire_change_immediately=fire_change_immediately,
                                            compo_col=compo_col,
                                            label_col=label_col,
                                            layout_vertical=layout_vertical,
                                            label_style=label_style,
                                            input_style=input_style,
                                            typeahead=typeahead,
                                            max_length=max_length,
                                            show_count=show_count,
                                            password=password,
                                            layover_icon=layover_icon,
                                            **extra_params)
