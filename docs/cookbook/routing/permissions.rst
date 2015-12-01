Permissions via ACL
===================
EPFL exposes the powerful pyramid ACL implementation in :class:`~solute.epfl.core.epflassets.EPFLView`. Consider the
following basic scenario:

 1. a login page,
 2. a home page with some secret information,
 3. a forbidden page with a warning.

Setting up ACL
--------------
Using the pyramid_epfl_starter scaffold you have already setup pyramid to use an ACLAuthorizationPolicy.
:class:`~solute.epfl.core.epflassets.EPFLView` complements that by setting a RootFactory with a global set of ACLs. In
order to populate that set :meth:`~solute.epfl.core.epflassets.EPFLView.register_acl`.

.. code-block:: python

    EPFLView.register_acl([
        'a_general_permission',
        ('a_role', 'a_role_specific_permission'),
        (False, 'a_role', 'a_role_specific_denied_permission'),
        ('system.Authenticated', 'a_role_specific_permission'),
    ])

The first is a somewhat useless thing, without checking any role the permission *a_general_permission* is given to
everyone. The second example is a much more useful thing, only a user with the role *a_role* will get the permission
*a_role_specific_permission*, while in the third example he will be denied the *a_role_specific_denied_permission*. The
fourth example is using the pyramid custom roles provided by the AuthTktAuthenticationPolicy.

Simple Login
------------
Any :class:`~solute.epfl.core.epflassets.EPFLView` can be restricted to certain permissions:

.. code-block:: python

    @epflassets.EPFLView(route_name='home', route_pattern='/', route_text='Home', permission='authenticated')

If you try to access the home page with this setting you will be greeted by the pyramid default 403 Forbidden page. It
is possible to use an EPFLView as a pyramid forbidden view, in order to provide a handy login screen:

.. code-block:: python

    @epflassets.EPFLView(forbidden_view=True)
    class ForbiddenPage(epfl.Page):
        root_node = components.LoginBox

        def login(self, username=None, password=None):
            if (username, password) == ('admin', '12345'):
                self.remember(username)
                return True

Now this just redirects us to the same place as before, but if we do this:

.. code-block:: python

    epflassets.EPFLView.register_acl([
        'access',
        ('system.Authenticated', 'authenticated'),
        (False, 'system.Authenticated', 'unauthenticated'),
    ])

We are now on the Home page and logged in!

Advanced Permission Handling
----------------------------
Unseen to our eyes the third page is handled automatically by the login box: The forbidden page. While it is viable to
always show the login page it would be better for the user to be able to recognize that he reached a forbidden place,
and hasn't just lost his login. The login box handles that like this:

.. code-block:: python

    def init_struct(self):
        [...]
        if epflacl.epfl_check_role('system.Authenticated', self.page.request):
            self.title = 'Forbidden View'
            self.node_list = [
                Text(
                    value='You are not authorized to see this page!'
                ),
                Link(
                    url='/',
                    name='Return to Home'
                )
            ]

We imported :meth:`solute.epfl.core.epflacl.epfl_check_role` and pushed setting the nodelist into
:meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.init_struct`. If our user is authenticated this check
evaluates to True so the node_list is overwritten again and the link is shown. You can see if this is working by either
modifying the permission of Home, removing the authenticated permission from the ACL or by adding another view with
another permission.
