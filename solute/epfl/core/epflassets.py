

def get_item_or_attr(obj, key):
    try:
        return obj[key]
    except (KeyError, TypeError):
        return getattr(obj, key)


class ModelBase(object):
    def __getitem__(self, item):
        compo, key, row, data_interface = item
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


from pyramid import security
from functools import wraps


def epfl_acl(permissions, default_allow=True, default_principal='system.Everyone', extend=False):
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

    def wrapper(cls):
        _acl = acl
        if extend:
            #Retrieve any previous acl to extend if requested.
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
    class ACL(object):
        def __init__(self, acl):
            self.__acl__ = acl

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