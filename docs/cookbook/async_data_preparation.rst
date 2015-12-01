Asynchronous Data Preparation
#############################
Complex data sometimes results in long running queries. In order to properly parallelize those requests one needs to
find the correct places to call preparation functions. The example provided here uses threading.Thread to show how it
can be done by properly using EPFL lifecycles.

.. code-block:: python

    # * encoding: utf-8

    from solute import epfl
    from solute.epfl import epflassets
    from solute.epfl import components
    import time
    import threading
    import Queue


    class HomeRoot(components.CardinalLayout):
        def init_struct(self):
            self.node_list.extend([
                epflassets.EPFLView.get_nav_list()(slot='west'),
                components.ColLayout(
                    node_list=[
                        components.Button(
                            event_name='foo',
                            value='Foo with preparation!',
                            cols=6
                        ),
                        components.Button(
                            event_name='foo_no_prep',
                            value='Foo without preparation!',
                            cols=6
                        ),
                        components.LinkListLayout(
                            cid='foo_one',
                            auto_initialize_children=False,
                            get_data='foo_one',
                            cols=3,
                            show_search=False
                        ),
                        components.LinkListLayout(
                            cid='foo_two',
                            auto_initialize_children=False,
                            get_data='foo_two',
                            cols=3,
                            show_search=False
                        ),
                        components.LinkListLayout(
                            cid='foo_three',
                            auto_initialize_children=False,
                            get_data='foo_three',
                            cols=3,
                            show_search=False
                        ),
                        components.LinkListLayout(
                            cid='foo_four',
                            auto_initialize_children=False,
                            get_data='foo_four',
                            cols=3,
                            show_search=False
                        )
                    ]
                )
            ])

        def handle_foo_no_prep(self):
            """Set all four lists to update but do not trigger the prepare functions.
            """
            calling_compo = self.page.foo_one
            calling_compo.auto_update_children = True

            calling_compo = self.page.foo_two
            calling_compo.auto_update_children = True

            calling_compo = self.page.foo_three
            calling_compo.auto_update_children = True

            calling_compo = self.page.foo_four
            calling_compo.auto_update_children = True

            self.redraw()

        def handle_foo(self):
            """Set all four lists to update and trigger the prepare functions.
            """
            calling_compo = self.page.foo_one
            calling_compo.auto_update_children = True
            self.page.model.prepare_foo_one(calling_compo, calling_compo.row_offset, calling_compo.row_limit,
                                            calling_compo.row_data)

            calling_compo = self.page.foo_two
            calling_compo.auto_update_children = True
            self.page.model.prepare_foo_two(calling_compo, calling_compo.row_offset, calling_compo.row_limit,
                                            calling_compo.row_data)

            calling_compo = self.page.foo_three
            calling_compo.auto_update_children = True
            self.page.model.prepare_foo_three(calling_compo, calling_compo.row_offset, calling_compo.row_limit,
                                              calling_compo.row_data)

            calling_compo = self.page.foo_four
            calling_compo.auto_update_children = True
            self.page.model.prepare_foo_four(calling_compo, calling_compo.row_offset, calling_compo.row_limit,
                                             calling_compo.row_data)

            self.redraw()


    class Worker(threading.Thread):
        def __init__(self, tid, q):
            super(Worker, self).__init__()
            self.tid = tid
            self.q = q

        def run(self):
            time.sleep(2)
            self.q.put([{'id': i,
                         'text': 'foo %s %s' % (i, self.tid),
                         'url': '/foo/%s/%s' % (i, self.tid)} for i in range(0, 10)])


    class Model(epflassets.ModelBase):
        foo_one = None
        foo_two = None
        foo_three = None
        foo_four = None

        def prepare_foo_one(self, calling_compo, row_offset, row_limit, row_data, *args, **kwargs):
            if self.foo_one is None:
                self.foo_one = Worker('prepare_foo_one', Queue.Queue())
                self.foo_one.start()

        def load_foo_one(self, calling_compo, row_offset, row_limit, row_data, *args, **kwargs):
            self.prepare_foo_one(calling_compo, row_offset, row_limit, row_data)
            data = self.foo_one.q.get()
            self.foo_one.join()
            return data

        def prepare_foo_two(self, calling_compo, row_offset, row_limit, row_data, *args, **kwargs):
            if self.foo_two is None:
                self.foo_two = Worker('prepare_foo_two', Queue.Queue())
                self.foo_two.start()

        def load_foo_two(self, calling_compo, row_offset, row_limit, row_data, *args, **kwargs):
            self.prepare_foo_two(calling_compo, row_offset, row_limit, row_data)
            data = self.foo_two.q.get()
            self.foo_two.join()
            return data

        def prepare_foo_three(self, calling_compo, row_offset, row_limit, row_data, *args, **kwargs):
            if self.foo_three is None:
                self.foo_three = Worker('prepare_foo_three', Queue.Queue())
                self.foo_three.start()

        def load_foo_three(self, calling_compo, row_offset, row_limit, row_data, *args, **kwargs):
            self.prepare_foo_three(calling_compo, row_offset, row_limit, row_data)
            data = self.foo_three.q.get()
            self.foo_three.join()
            return data

        def prepare_foo_four(self, calling_compo, row_offset, row_limit, row_data, *args, **kwargs):
            if self.foo_four is None:
                self.foo_four = Worker('prepare_foo_four', Queue.Queue())
                self.foo_four.start()

        def load_foo_four(self, calling_compo, row_offset, row_limit, row_data, *args, **kwargs):
            self.prepare_foo_four(calling_compo, row_offset, row_limit, row_data)
            data = self.foo_four.q.get()
            self.foo_four.join()
            return data


    @epflassets.EPFLView(route_name='home', route_pattern='/', route_text='Home')
    class HomePage(epfl.Page):
        model = Model

        root_node = HomeRoot

