#* coding: utf-8
from solute.epfl.core.epflvalidators import ValidatorBase


class TextValidator(ValidatorBase):
    def __init__(self, value='value', error_message='Value is required!', *args, **kwargs):
        """Validate a related Input field as a text.

        :param value: Where to get the value to be evaluated.
        :param error_message: Error message to be displayed upon failed validation.
        """
        super(TextValidator, self).__init__(value=value, error_message=error_message, *args, **kwargs)

    def validate(self, value=None, error_message=None, **kwargs):
        # Check if mandatory and present.
        if self.caller.mandatory and (value is None or value in ["", u'']):
            self.error_message = error_message
            return False

        return True
