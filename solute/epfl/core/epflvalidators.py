from abc import abstractmethod


VALIDATOR_MAP = {}


class ValidatorBase(dict):
    """Utility class providing error handling, parameter lookup and validation hooks.
    """

    errors = None

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """Overwrite this method to provide the interface for a custom validator.
        """
        super(ValidatorBase, self).__init__(*args, **kwargs)

    def __call__(self, caller, *args, **kwargs):
        """Lookup parameters, run validation, return result.
        """
        self.caller = caller
        self.errors = []
        for key, value in self.iteritems():
            if type(value) is not str:
                kwargs[key] = value
                continue
            kwargs[key] = self.get_param(value)

        return self.validate(**kwargs)

    @abstractmethod
    def validate(self, **kwargs):
        """Abstract validate method to be called by __call__. Has to be overwritten with custom validation logic.
        """
        raise Exception("No validation implemented.")

    @property
    def error_message(self):
        """Error message handling allowing for multiple messages to be present to describe the current error state.
        """
        return '\n'.join(self.errors)

    @error_message.setter
    def error_message(self, value):
        """Appends value to the list of errors.
        """
        self.errors.append(value)

    @error_message.deleter
    def error_message(self):
        """Resets the list of errors.
        """
        self.errors = []

    def get_param(self, param_name):
        """Get a specific param as determined by its name from either the calling component or the appropriate target.
        Returns in this order: attribute param_name of target component, item param_name of target component, param_name
        on miss. Target component is the calling component if param_name is not dotted. Else the target component is
        looked up in the parent form by the name defined by the string preceding the dot.

        password.value: Lookup the field with the name password and return its attribute or item value.
        password.: Return the field with the name password.
        value: Return the attribute or item value of the calling component.

        :param param_name: The (dotted) name to lookup.
        """
        # Split param_name and lookup actual target if required.
        target, original_name = None, param_name
        if '.' in param_name:
            try:
                target, param_name = self.get_dotted(param_name)
            except TypeError:
                # In case of a dot inside a message or similar legitimate strings get_dotted will return None.
                return param_name

        if param_name == '':
            return target

        if target is None:
            target = self.caller
        if hasattr(target, param_name):
            return getattr(target, param_name)

        return original_name

    def get_dotted(self, param_name):
        field_name, param_name = param_name.split('.')
        form = self.caller.get_parent_form()
        if form is None:
            raise Exception('No parent form found. Did you try using a dotted name on a Validator with no Form?')
        for sibling in form.registered_fields:
            if sibling.name == field_name:
                return sibling, param_name

    def __getstate__(self):
        return dict(self)

    def __setstate__(self, data):
        self.update(data)

    @classmethod
    def by_name(cls, name):
        return VALIDATOR_MAP.get(name, ValidatorBase)

    @classmethod
    def register_name(cls, name):
        VALIDATOR_MAP[name] = cls
