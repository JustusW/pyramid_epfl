# * encoding: utf-8

from solute import epfl
from solute.epfl import epflassets
from solute.epfl import components


class HomeRoot(components.CardinalLayout):
    def init_struct(self):
        self.node_list.append(epflassets.EPFLView.get_nav_list()(slot='west'))


@epflassets.EPFLView(route_name='home', route_pattern='/', route_text='Home')
class HomePage(epfl.Page):
    root_node = HomeRoot(
        constrained=True,
        node_list=[
            components.Box(title="Welcome to EPFL!")
        ]
    )
