.. _get_data:

How do I get data?
==================
The get_data convenience methods are the way of choice to provide data from any API, Database or other Datasource to
EPFL and its components.


The basics
----------
You probably have followed these instructions more than once:

.. automethod:: solute.epfl.core.epflcomponentbase.ComponentContainerBase.get_data
    :noindex:

The actual mechanism enabling this method is in
:meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase._get_data`:

.. code-block:: python

    def _get_data(self, *args, **kwargs):
        """
        Internal wrapper for :meth:`get_data` to decide wether it is to be called as a function or only contains a
        reference to a model on :attr:`.epflpage.Page.model`.
        """
        # get_data is a string pointing to a model load function.
        if type(self.get_data) is str and self.page.model is not None:
            return self.page.model.get(self, self.get_data, (args, kwargs), self.data_interface)
        # get_data is a tuple with a string or integer pointing to a model and a string pointing to a model load
        # function.
        elif type(self.get_data) is tuple and self.page.model is not None:
            return self.page.model[self.get_data[0]].get(self, self.get_data[1], (args, kwargs), self.data_interface)
        # default: get_data is a callable.
        return self.get_data(*args, **kwargs)

The three cases are separated here and put into the correct pipelines.

Default handling
````````````````
:meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.get_data` is called and its return value is used as
data inside :meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.update_children`:

.. code-block:: python

    data = self._get_data(self.row_offset, self.row_limit, self.row_data)

The data is then used to either update existing components:

.. code-block:: python

    # IDs of data represented by a component. Matching components are updated.
    for data_id in set(new_order).intersection(current_order):
        compo = getattr(self.page, data_cid_dict[data_id])
        for k, v in data_dict[data_id].items():
            if getattr(compo, k) != v:
                setattr(compo, k, v)
                self.redraw()

or used as attributes to create completely new components:

.. code-block:: python

    # IDs of data not yet represented by a component. Matching components are created.
    for data_id in set(new_order).difference(current_order):
        ubc = self.default_child_cls(**data_dict[data_id])
        bc = self.add_component(ubc, init_transaction=init_transaction)
        data_cid_dict[data_id] = bc.cid

        self.redraw()

In every case data needs to be a Sequence of Mappings.

Loading from a model
````````````````````
This part is pretty straight forward and implemented in :meth:`~solute.epfl.core.epflassets.ModelBase.get` in
:class:`~solute.epfl.core.epflassets.ModelBase`. This method is one you have very probably never seen before, since it
is most definitely a deep part of the core. While providing your own :class:`~solute.epfl.core.epflassets.ModelBase`
implementation to provide data is required, :meth:`~solute.epfl.core.epflassets.ModelBase.get` is accessed only by
:meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase._get_data`.

.. automethod:: solute.epfl.core.epflassets.ModelBase.get
    :noindex:

This method simply selects the load\_{key} function of the :class:`~solute.epfl.core.epflassets.ModelBase` instance, and
calls it. The result has to be a Sequence of Objects.

Creating a Mapping
..................
:meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.get_data` is expected to return a Sequence of
Mappings. So :meth:`~solute.epfl.core.epflassets.ModelBase.get` needs to translate an object into a Sequence, for this
very purpose the :attr:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.data_interface` dict is provided. The
minimum contents of this dict has to be an entry for the id, since this is required for the get_data system to work at
all.

There are three possible scenarios for any item of
:attr:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.data_interface`: None, a string or a formatted string.
Every row of the result is made off of a copy of
:attr:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.data_interface`:

.. code-block:: python

    tmp_data = data_interface.copy()

For a complete reference of the possible actions refer to the `Format Specification Mini-Language`_ Section of the
official python docs. To recognize a formatted string format() is called once without parameters. If this raises a
KeyError the string contains formatting instructions requiring named parameters.

.. code-block:: python

    'foobar'.format()  # This passes fine.
    '{foobar}'.format()  # This does not.

If a formatted string is recognized the current row of the result is used like a mapping to provide keywords for the
format call:

.. code-block:: python

    tmp_data[k] = v.format(**row)

If the row is not a dict its __dict__ attribute is used instead:

.. code-block:: python

    tmp_data[k] = v.format(**row.__dict__)

Unformatted strings will simply be used as attribute or item name respectively:

.. code-block:: python

    tmp_data[k] = get_item_or_attr(row, tmp_data[k])

If no string is provided the key will be used instead:

.. code-block:: python

    tmp_data[k] = get_item_or_attr(row, k)

At the end :meth:`~solute.epfl.core.epflassets.ModelBase.get` returns a list of
:attr:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.data_interface` copies filled with the appropriate
values.

Model Selection
```````````````
If a model selector is provided the appropriate model is selected as an item from the current
:class:`~solute.epfl.core.epflpage.Page` :attr:`~solute.epfl.core.epflpage.Page.model`. This can be either a list or a
dict. The rest is just like the previous section.


Update children
---------------
So, what's it all for? Well, this. Once data has been loaded and mapped it is provided to
:meth:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.update_children` and transformed into actual
:class:`~solute.epfl.core.epflcomponentbase.ComponentBase` instances.

This is done in five separate steps:
 1. Determine the tipping point.
 2. Delete no longer included results.
 3. Create components for new results.
 4. Update existing components for existing results.
 5. Enforce the order of the result on the child components.

The tipping point
`````````````````
Simply put, the tipping point is the number of non get_data created child components. This point is of particular
importance since it ensures that a component may contain static preset components as well as components generated
dynamically from results. As an example think of an "add new entry" button in a list of entries.

.. code-block:: python

    tipping_point = len([c for c in self.components if not hasattr(c, 'id')])

This is one of the reasons it is considered best practice to never set an attribute called id on any
:class:`~solute.epfl.core.epflcomponentbase.ComponentBase` derivative since it is the sole distinction available to the
core to tell its own generated and "normal" components apart.

Component begone!
`````````````````
Quite straight forward really:

.. code-block:: python

    # IDs of components no longer present in data. Their matching components are deleted.
    for data_id in set(current_order).difference(new_order):
        self.del_component(data_cid_dict.pop(data_id))
        self.redraw()

For easier reading the appropriate methods of `set`_ have been used. And you thought set theory was a useless math
topic, huh?

Updating components
```````````````````
Although the result rows are used as attributes of the new components it is possible to include them in the
:attr:`~solute.epfl.core.epflcomponentbase.ComponentBase.compo_state`. In that scenario it may be necessary to update.

.. code-block:: python

    # IDs of data represented by a component. Matching components are updated.
    for data_id in set(new_order).intersection(current_order):
        compo = getattr(self.page, data_cid_dict[data_id])
        # A component may decide that it can not be updated by this mechanism. Relevant for components doing heavy
        # lifting in their :meth:`ComponentBase.init_transaction`.
        if compo.disable_auto_update:
            current_order.remove(data_id)
            self.del_component(data_cid_dict.pop(data_id))
            self.redraw()
            continue
        for k, v in data_dict[data_id].items():
            if getattr(compo, k) != v:
                setattr(compo, k, v)
                self.redraw()

Of course this calls for an intersection. Everything else is just house keeping. Be aware: This previously might have
caused problems with more complex components, e.g. If a component relied on treating data in its
:meth:`~solute.epfl.core.epflcomponents.ComponentBase.init_transaction` method. In cases like this the
:attr:`~solute.epfl.core.epflcomponents.ComponentBase.disable_auto_update` flag can be set to True. The component is
deleted and flagged for (re-)creation in cases such as this.

Hello component
```````````````
If you delete them you have to create them at one time:

.. code-block:: python

    # IDs of data not yet represented by a component. Matching components are created.
    for data_id in set(new_order).difference(current_order):
        ubc = self.default_child_cls(**data_dict[data_id])
        bc = self.add_component(ubc, init_transaction=init_transaction)
        data_cid_dict[data_id] = bc.cid

        self.redraw()

For this purpose we use the difference between the new and existing order. An
:class:`~solute.epfl.core.epflcomponentbase.UnboundComponent` is created from the
:attr:`~solute.epfl.core.epflcomponentbase.ComponentContainerBase.default_child_cls`. Note how it is called: It's a
feature that is actually used in the :class:`~solute.epfl.components.TableLayout`. You can of course simply provide an
:class:`~solute.epfl.core.epflcomponentbase.UnboundComponent` or
:class:`~solute.epfl.core.epflcomponentbase.ComponentBase` derivative, but you may also provide an instance method, thus
giving you the ability to dynamically pick and choose what component to use here! Once created the
:class:`~solute.epfl.core.epflcomponentbase.UnboundComponent` instance is added.

Order is everything
```````````````````
Last but not least the correct order has to be enforced.

.. code-block:: python

    # Rebuild order.
    compo_struct = self.compo_info['compo_struct']
    for i, data_id in enumerate(new_order):
        try:
            key = compo_struct.keys()[i + tipping_point]
            if compo_struct[key].get('config', {}).get('id', None) != data_id:
                self.switch_component(self.cid, data_cid_dict[data_id], position=i + tipping_point)
                self.redraw()
        except AttributeError:
            pass

Not really a case for a full blown sort of any kind since all that needs to be ensured is that the order of the actual
components equals the order from the current result. For this purpose the actual OrderedDict  with the compo_struct is
used as a reference.

.. _`Format Specification Mini-Language`: https://docs.python.org/2/library/string.html#format-specification-mini-language
.. _`set`: https://docs.python.org/2/library/stdtypes.html#set