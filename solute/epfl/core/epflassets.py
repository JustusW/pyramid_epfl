from pyramid.view import view_config
from pyramid import security
from functools import wraps


def get_item_or_attr(obj, key):
    """
    Helper function returning the item key from obj or, failing that the attribute key. If both do not exist an
    Exception is raised by getattr.
    """
    try:
        return obj[key]
    except (KeyError, TypeError):
        return getattr(obj, key)


class ModelBase(object):
    """
    Use this class as a base for your own bound models. For any given method identificator a method of its nam prefiload_
    """

    def __init__(self, request):
        self.request = request

    def get(self, compo, key, row, data_interface):
        args, kwargs = row
        output = []
        for row in getattr(self, 'load_' + key)(compo, *args, **kwargs):
            tmp_data = data_interface.copy()
            for k, v in tmp_data.items():
                if type(v) is str:
                    try:
                        v.format()
                        tmp_data[k] = get_item_or_attr(row, tmp_data[k])
                    except KeyError:
                        if type(row) is dict:
                            tmp_data[k] = v.format(**row)
                        else:
                            tmp_data[k] = v.format(**row.__dict__)
                else:
                    tmp_data[k] = get_item_or_attr(row, k)

            output.append(tmp_data)

        return output


class ACL(object):
    def __init__(self, acl):
        self.__acl__ = acl


class DefaultACLRootFactory(object):
    __acl__ = []

    def __init__(self, request):
        self.request = request

    def __call__(self, request):
        return self


def epfl_acl(permissions, default_allow=True, default_principal='system.Everyone', extend=False, use_as_global=False):
    default_action = security.Deny
    if default_allow:
        default_action = security.Allow

    if permissions is None:
        permissions = []
    elif type(permissions) is not list:
        permissions = [permissions]

    actions = {}
    for permission in permissions:
        action, principal = default_action, default_principal
        if type(permission) is tuple and len(permission) == 2:
            principal, permission = permission
        elif type(permission) is tuple and len(permission) == 3:
            action, principal, permission = permission
            if action:
                action = security.Allow
            else:
                action = security.Deny

        if type(permission) is not list:
            permission = [permission]

        actions.setdefault(action, {}).setdefault(principal, permission)

    acl = []
    for action, _principals in actions.items():
        for principal, _permission in _principals.items():
            acl.append((action, principal, _permission))

    if use_as_global:
        if not DefaultACLRootFactory.__acl__:
            DefaultACLRootFactory.__acl__ = acl
        else:
            raise Exception('An acl has already been set to the DefaultACLRootFactory.')

    def wrapper(cls):
        _acl = acl
        if extend:
            # Retrieve any previous acl to extend if requested.
            old_acl = getattr(cls, '__acl__', [])
            old_acl.extend(_acl)
            _acl = old_acl

        setattr(cls, '__acl__', _acl)

        return cls

    return wrapper


def epfl_has_permission(permission, fail_callback=None):
    def wrapper(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            self = args[0]
            request = self.request
            if not request.has_permission(permission, self):
                if fail_callback:
                    return fail_callback(*args, **kwargs)
                return
            return func(*args, **kwargs)

        return wrap

    return wrapper


def epfl_has_role(role, fail_callback=None):
    def wrapper(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            self = args[0]
            request = self.request
            if not request.has_permission('has_role', ACL([(security.Allow, role, 'has_role')])):
                if fail_callback:
                    return fail_callback(*args, **kwargs)
                return
            return func(*args, **kwargs)

        return wrap

    return wrapper


def epfl_check_role(role, request):
    if request.has_permission('has_role', ACL([(security.Allow, role, 'has_role')])):
        return True
    else:
        return False


class EpflView(object):
    config = None

    def __init__(self, route_name=None, route_pattern=None, permission=None, route_text=None):
        self.route_name = route_name
        self.route_text = route_text or self.route_name
        self.route_pattern = route_pattern
        self.permission = permission

        self._config.add_route(self.route_name, self.route_pattern)

    def __call__(self, cb):
        self._config.add_view(cb,
                              route_name=self.route_name,
                              permission=self.permission, )
        return cb

    @property
    def _config(self):
        if self.config:
            return self.config
        raise Exception('No config found, have you added this module to epfl.active_modules?')

    @staticmethod
    def configure(config):
        EpflView.config = config

        active_modules = [m.strip() for m in config.registry.settings.get('epfl.active_modules', '').split(',')]
        for m in active_modules:
            config.maybe_dotted(m)

        EpflView.config = None
