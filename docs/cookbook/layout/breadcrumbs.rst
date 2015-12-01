Breadcrumbs
===========

Breadcrumbs are useful in complex projects where pages have many subpages. Details however matter, and here is a
best-practice solution for EPFL Style Breadcrumbs:

.. code-block:: python

    # * encoding: utf-8

    from solute import epfl
    from solute.epfl import epflassets
    from solute.epfl import components


    class LayoutRoot(components.CardinalLayout):
        plain = ['north']

        def init_struct(self):
            self.node_list.append(epflassets.EPFLView.get_nav_list()(slot='west'))

            self.node_list.append(components.NavLayout(
                cid='breadcrumbs',
                title='My EPFL Page',
                img='epfl/static/img/epfl.jpg',
                slot='north',
                node_list=[
                    components.Text(
                        value='Hello there!',
                        slot='right',
                        verbose=True,
                        tag='a'
                    ),
                    components.Link(
                        name='Logout',
                        url='logout',
                        slot='right'
                    )
                ]
            ))

        def init_breadcrumbs(self):
            pass

        def init_transaction(self):
            super(LayoutRoot, self).init_transaction()
            self.init_breadcrumbs()


    class HomeRoot(LayoutRoot):
        def init_breadcrumbs(self):
            super(HomeRoot, self).init_breadcrumbs()

            self.page.breadcrumbs.add_component(
                components.Link(
                    name='Home',
                    url='/',
                    slot='left',
                    breadcrumb=True
                )
            )


    class SecondRoot(HomeRoot):
        def init_breadcrumbs(self):
            super(SecondRoot, self).init_breadcrumbs()

            self.page.breadcrumbs.add_component(
                components.Link(
                    name='Some sub page',
                    url='/',
                    slot='left',
                    breadcrumb=True
                )
            )


    class ThirdRoot(HomeRoot):
        def init_breadcrumbs(self):
            super(ThirdRoot, self).init_breadcrumbs()

            self.page.breadcrumbs.add_component(
                components.Link(
                    name='Another sub page',
                    url='/',
                    slot='left',
                    breadcrumb=True
                )
            )


    @epflassets.EPFLView(route_name='home', route_pattern='/', route_text='Home')
    class HomePage(epfl.Page):
        root_node = HomeRoot


    @epflassets.EPFLView(route_name='second', route_pattern='/second', route_text='Second Page')
    class SecondPage(epfl.Page):
        root_node = SecondRoot


    @epflassets.EPFLView(route_name='third', route_pattern='/third', route_text='Third Page')
    class ThirdPage(epfl.Page):
        root_node = ThirdRoot

