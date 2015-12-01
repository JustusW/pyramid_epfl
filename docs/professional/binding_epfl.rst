.. binding_epfl:

Binding EPFL to Pyramid
=======================

Handling Views
--------------

Pyramid has two ways to dispatch a given url to a handler: There is Traversal_ and `URL Dispatch`_. EPFL uses the later,
since it is simpler and fits the pattern of EPFL perfectly: One purpose, one page, one view. (Although you can actually
map more than one route to that particular view.)

In order to use EPFL in pyramid a :class:`~solute.epfl.core.epflpage.Page` is implemented to be callable. Pyramid
ViewHandlers are called once (instantiated in this case) with a request and then called a second time and expected to
return a response. :meth:`~solute.epfl.core.epflpage.Page.__call__` returns a pyramid Response Object using Jinja2 to
parse it.

Let's discuss this in detail:

.. code-block:: python

    def __init__(self, request, transaction=None):
        """
        The optional parameter "transaction" is needed when creating page_objects manually. So the transaction is not
        the same as the requests one.
        The lazy_mode is setup here if the request is an ajax request and all events in it are requesting lazy_mode.
        """
        self.request = request
        self.request.page = self
        self.page_request = PageRequest(request, self)
        self.response = epflclient.EPFLResponse(self)
        self.components = PageComponents(self)  # all registered components of this page

        if transaction:
            self.transaction = transaction

        if not hasattr(self, 'transaction'):
            try:
                self.transaction = self.__get_transaction_from_request()
            except epfltransaction.TransactionRouteViolation:
                # This ensures that a transaction is only used for the route it was created on. A new transaction is
                # created in case of a differing route.
                self.transaction = epfltransaction.Transaction(request)
                self.transaction.set_page_obj(self)

The class :class:`~solute.epfl.core.epflpage.PageRequest` is a wrapper to provide request data to components in a safe
manner. :class:`~solute.epfl.core.epflclient.EPFLResponse` is another wrapper providing primarily template parsing,
including dynamic extra content. odict_ has been changed from the original variant out of collections to a new variant
from collections2_ that offers better performance and most importantly inserting keys at specific positions. The
:class:`~solute.epfl.core.epfltransaction.Transaction` is initialized with the transaction id (tid) parameter from the
request. If the transaction belongs to another route a new Transaction is created instead.

Default Root Factory
--------------------

Another part of the :class:`~solute.epfl.core.epflpage.Page` that is bound deeply into pyramid are the methods
:meth:`~solute.epfl.core.epflpage.Page.remember` and :meth:`~solute.epfl.core.epflpage.Page.forget`. While those methods
themselves are only calling single methods from pyramid they are working in tandem with
:meth:`~solute.epfl.core.epflassets.epfl_acl` to provide global permissions in setting
:class:`~solute.epfl.core.epflassets.DefaultACLRootFactory` as the root factory during configuration. Also note the
close working relationship with :class:`~solute.epfl.core.epflassets.EPFLView` which automatically generates a link list
and sets ACLs.

.. code-block:: python

    def includeme(config):
        """
        The main configuration of the EPFL
        """

        [...]

        config.set_root_factory(epflassets.DefaultACLRootFactory)

This is important to know, and there's an important rationale behind it: `URL Dispatch`_ is seldom to never utilizing a
root factory since it's page oriented. The primary use of a root factory in this case becomes providing a context to
permission checks, which should be handled by epfl. It might not be the best method, I'd much rather set this only if no
RootFactory had been provided or if ACLs had actually been set using :meth:`~solute.epfl.core.epflassets.epfl_acl`.
However due to constraints of pyramid it is not currently possible to find out wether one has been set during an active
configuration run while at the same time the setting of ACLs is not necessarily done before includeme() is called. This
is largely due to limitations of the underlying zope structure and it's complex conflict resolving mechanism.

Routing all over the place
--------------------------
Almost every component depends on having stylesheets and scripts available for static calls. Registering those routes is
handled in the same call as setting the default root factory is:

.. code-block:: python

    # solute/epfl/__init__.py
    def includeme(config):
        """
        The main configuration of the EPFL
        """
        [...]
        # static routes
        config.add_static_view(name = "epfl/static", path = "solute.epfl:static")
        components.add_routes(config)
        [...]

    # solute/epfl/components/__init__.py
    def add_routes(config):
        """
        Called once per thread start, in order to call
        :func:`solute.epfl.core.epflcomponentbase.ComponentBase.add_pyramid_routes` for every component provided by epfl
        through this package.
        """

        Canvas.add_pyramid_routes(config)
        [...]

From this call onward you can use links like 'solute.epfl.components:canvas/canvas.js' to link to any statically
accessible file in the components static sub-directory.


.. _Traversal: http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/traversal.html
.. _`URL Dispatch`: http://docs.pylonsproject.org/docs/pyramid/en/latest/narr/urldispatch.html
.. _odict: https://github.com/therealfakemoot/collections2
.. _collections2: https://github.com/therealfakemoot/collections2
