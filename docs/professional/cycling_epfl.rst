.. cycling_epfl:

Cycling EPFL: Life of a request
===============================
Previously this topic was kind of a hassle. There were actually a hand full of ways any request might walk through a
given :class:`~solute.epfl.core.epflpage.Page` call. Thankfully we've had time to rearrange this a bit so take a look:

A model for everyone
--------------------
.. code-block:: python

    def __call__(self):
        """
        The page is called by pyramid as view, it returns a rendered page for every request. Uses :meth:`call_ajax`,
        :meth:`call_default`, :meth:`call_cleanup`.
        [request-processing-flow]
        """

        self.setup_model()

Previously EPFL was utilizing the reflection mechanisms of pyramid (and thus zope) to allow a user the creation of
custom data sources. But since actually meddling with the config is frowned upon nowadays (there's really only a blessed
few processes that absolutely require this still) a new solution had to be found. The new
:class:`~solute.epfl.core.epflassets.ModelBase` is a simple base class for all the needs anyone might ever have. It's
tightly tied into the get_data pattern you should know well from working with
:class:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase` and its offspring before. You can find more
information on this mechanism in its own topic: :ref:`get_data`

Only you can prevent transaction loss!
--------------------------------------
.. code-block:: python

        # Check if we lost our transaction to a timeout.
        transaction_loss = self.prevent_transaction_loss()
        if transaction_loss:
            return transaction_loss

Since EPFL does no longer carry its own specific session handler some instances have arisen where transactions were
partially or completely lost. This little helper function checks if the transaction is still well formed and if not
creates a page reload in order to avoid exceptions and crashes from a malformed
:class:`~solute.epfl.core.epfltransaction.Transaction`.

Recursive statements are recursive because they are Recursions
--------------------------------------------------------------
.. code-block:: python

        self.handle_transaction()

This call is the first actual stepping stone in the official lifecycle. It invokes the following methods:
 1. :meth:`solute.epfl.core.epflpage.Page.setup_components` is called to assign the root_node.
 2. If the root_node has not already been initialized in this :class:`~solute.epfl.core.epfltransaction.Transaction`
    its :meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.init_transaction` method is called.
 3. Any currently active component, that is components that have been instantiated during this phase, are then also
    initialized as necessary by calling their respective
    :meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.init_transaction` methods as well.

These three steps build the lifecycle stage usually referred to as "init transaction" or similar names. The title of
this topic refers to a very important fact about this stage: It's about as recursive as the rendering process, which
is basically saying "it's really heavily relying on recursion". The reason is that during the individual call to
:meth:`~solute.epfl.core.epflcomponentbase.ComponentBase.init_transaction` any
:class:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase` component will instantiate all its children as
directed by its :attr:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.node_list`. This would in turn cause
that component to instantiate any potential children it might have. So that initial call in #3 kicks of all the fixed
component instantiations for this page which can be a lot.

Event handling
--------------
Now there's a short topic name for the place most EPFL requests spends more than half its total time. This is where
almost all the fun happens.

.. code-block:: python

        content_type = "text/html"

        if self.request.is_xhr:
            self.handle_ajax_events()
            content_type = "text/javascript"
        else:
            # Reset the rendered_extra_content list since none actually has been rendered yet!
            self.transaction['rendered_extra_content'] = set()

        for compo in self.get_active_components():
            compo.after_event_handling()

The default content type of any request is set to text/html and then subsequently overwritten if it's actually an AJAX
request. Based on the pyramid request flag the actual handling is dispatched to either the ajax or no special handlers.
Previously it was possible to hook into submit requests directly, since this option had been disabled by a bug for over
a month without it being noticed it was deprecated. The only important action in case of a full page reques is to reset
the rendered_extra_content, if omitted this leads to devilishly hard to find bugs with missing static extra content.
Finally the after_event_handling cycle is kicked off on all active components. You can find more information on this
mechanism in its own topic: :ref:`event_handling`

After Event Handling
--------------------

.. code-block:: python

        out = self.render()

        out += self.call_cleanup(self.request.is_xhr)

        response = Response(body=out.encode("utf-8"),
                            status=200,
                            content_type=content_type)
        response.headerlist.extend(self.remember_cookies)
        return response


The easy one up front: :meth:`~solute.epfl.core.epflpage.Page.call_cleanup` just appends a javascript snippet if the
transaction ID has changed in order to update the client side state. In the end a pyramid Response is created using the
rendered output string and the appropriate content_type. The remember_cookies are required for using the pyramid
remember() and forget() API. You can find more information on the rendering mechanism in its own topic:
:ref:`rendering`