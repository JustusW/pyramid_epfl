# * coding: utf-8
from solute.epfl.core.epflvalidators import ValidatorBase


class BoolValidator(ValidatorBase):
    def __init__(self, value='value', error_message='Mandatory field not checked!', *args, **kwargs):
        """Validate a related Input field as a boolean.

        :param value: Where to get the value to be evaluated.
        :param error_message: Error message to be displayed upon failed validation.
        """
        super(BoolValidator, self).__init__(value=value, error_message=error_message, *args, **kwargs)

    def validate(self, value=None, error_message=None, **kwargs):
        # Check if mandatory and True.
        if self.caller.mandatory and value is not True:
            self.error_message = error_message
            return False

        return True
