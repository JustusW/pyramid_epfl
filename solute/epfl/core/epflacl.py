from pyramid import security
from functools import wraps


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
            if action is True or action == security.Allow:
                action = security.Allow
            else:
                action = security.Deny

        if type(permission) is not list:
            permission = [permission]

        actions.setdefault(action, {}).setdefault(principal, []).extend(permission)

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


def epfl_has_permission(permission, fail_callback=None, obj=None, use_global_acl=False):
    def wrapper(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            self = args[0]
            target = self
            if use_global_acl:
                target = DefaultACLRootFactory
            _request = self.request
            if not _request.has_permission(permission, target):
                if fail_callback:
                    return fail_callback(*args, **kwargs)
                return
            return func(*args, **kwargs)

        return wrap

    if obj:
        return obj.request.has_permission(permission, obj)

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
