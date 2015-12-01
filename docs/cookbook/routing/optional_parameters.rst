Optional Parameters
===================
Sometimes you may have some kind of detail view opening after you selected an entry from a list, and you may want to
provide that parameter to this route. For this very purpose :class:`~solute.epfl.core.epflassets.EPFLView` can be
chained:

.. code-block:: python

    @epflassets.EPFLView(route_name='home', route_pattern='/', route_text='Home')
    @epflassets.EPFLView(route_name='home_id', route_pattern='/{id}')
    class HomePage(epfl.Page):

In order to access the parameter just do this in the root node:

.. code-block:: python

    class HomeRoot(components.CardinalLayout):
        def init_struct(self):
            self.node_list.append(epflassets.EPFLView.get_nav_list()(slot='west'))

            if self.page.request.matchdict.get('id', None):
                print self.page.request.matchdict.get('id', None)

You can add a new component using that ID:

.. code-block:: python

    my_id = self.page.request.matchdict.get('id', None)
    self.node_list.append(
        components.Text(
            value='Selected ID is {my_id}'.format(my_id=my_id)
        )
    )

All the while the extra route will not be shown in the menu since no route_text is provided.
