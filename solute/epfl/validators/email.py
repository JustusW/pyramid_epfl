#* coding: utf-8
from solute.epfl.validators.text import TextValidator


class EmailValidator(TextValidator):
    def __init__(self, value='value', error_message='E-Mail is required!', domain=None,
                 error_message_domain='Invalid domain!', *args, **kwargs):
        """Validate a related Input field as a text.

        :param value: Where to get the value to be evaluated.
        :param error_message: Error message to be displayed upon failed validation.
        :param domain: List of domains accepted by this validator instance.
        :param error_message_domain: Error message to be displayed upon encountering a wrong domain.
        """
        super(EmailValidator, self).__init__(value=value, error_message=error_message, domain=domain,
                                             error_message_domain=error_message_domain, *args, **kwargs)

    def validate(self, value=None, error_message=None, domain=None, error_message_domain=None, **kwargs):
        result = super(EmailValidator, self).validate(value=value, error_message=error_message,
                                                      error_message_domain=error_message_domain, **kwargs)
        if result is False:
            return False

        if value is not None and value not in ["", u'']:
            if '@' not in value:
                self.error_message = error_message
                return False
            split_value = value.split('@')
            if len(split_value) != 2:
                self.error_message = error_message
                return False

            if domain is not None and split_value[1] not in domain:
                self.error_message = error_message_domain
                return False

        return True
