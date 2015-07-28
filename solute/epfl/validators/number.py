#* coding: utf-8
from solute.epfl.core.epflvalidators import ValidatorBase


class NumberValidator(ValidatorBase):
    float = False  #: Treat value as a float.

    def __init__(self, value='value', min_value=None, max_value=None, error_message='Value is required!', *args,
                 **kwargs):
        """Validate a related Input field as a number.

        :param value: Where to get the value to be evaluated.
        :param min_value: Lower boundary for value.
        :param max_value: Upper boundary for value.
        :param error_message: Error message to be displayed upon failed validation. If left to default with either
                              min_value or max_value present this will default to 'Value is outside of limit' instead.
        """
        if (min_value or max_value) and error_message == 'Value is required!':
            error_message = 'Value is outside of limit!'
        super(NumberValidator, self).__init__(value=value, error_message=error_message, *args, **kwargs)

    def validate(self, value=None, min_value=None, max_value=None, error_message=None, **kwargs):
        # Check if mandatory and present.
        if self.caller.mandatory and (value is None or value == ""):
            self.error_message = error_message
            return False

        # Not mandatory and not set passes muster.
        if value is None or value == "":
            return True

        # Can value be cast to float or int respectively.
        try:
            if self.float:
                float(value)
            else:
                int(value)
        except ValueError:
            self.error_message = error_message
            return False

        # Ensure value is within boundaries of min_value and max_value respectively.
        if min_value is not None and int(value) < min_value:
            self.error_message = error_message
            return False
        elif max_value is not None and int(value) > max_value:
            self.error_message = error_message
            return False

        return True
