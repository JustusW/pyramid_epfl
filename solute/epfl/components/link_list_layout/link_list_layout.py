# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase
from solute.epfl.components import PaginatedListLayout
from solute.epfl.components import Link
from solute.epfl.core.epflutil import has_permission_for_route


class LinkListLayout(PaginatedListLayout):
    data_interface = {'id': None,
                      'text': None,
                      'url': None}

    theme_path = {'default': PaginatedListLayout.theme_path,
                  'row': ['link_list_layout/theme']}

    js_name = PaginatedListLayout.js_name + [('solute.epfl.components:link_list_layout/static', 'link_list_layout.js')]

    compo_state = PaginatedListLayout.compo_state + ['links']

    #: Add the specific list type for the link list layout. see :attr:`ListLayout.list_type`
    list_type = PaginatedListLayout.list_type + ['link']

    links = None  #: List of dicts to be used as entries.
    event_name = None  #: Default event to be triggered on clicks.

    auto_update_children = False

    new_style_compo = True
    compo_js_name = 'LinkListLayout'

    def __init__(self, page, cid, links=None, event_name=None, show_search=None, height=None, **kwargs):
        """Paginated list using the PrettyListLayout based on bootstrap. Offers search bar above and pagination below
        using the EPFL theming mechanism. Links given as parameters are checked against the existing routes
        automatically showing or hiding them based on the users permissions.

        :param links: List of dicts with text and url. May contain an icon entry.
        :param event_name: The name of an event to be triggered instead of rendering normal links.
        :param height: Set the list to the given height in pixels.
        :param show_search: Toggle weather the search field is shown or not.
        :param show_pagination: Toggle weather the pagination is shown or not.
        :param search_focus: Toggle weather the search field receives focus on load or not.
        """
        super(PaginatedListLayout, self).__init__(page, cid, links=None, event_name=None, show_search=None, height=None,
                                                  **kwargs)

    def get_data(self, row_offset=None, row_limit=None, row_data=None):
        links = []
        if self.links is None:
            self.links = []
        for i, link in enumerate(self.links):
            if not has_permission_for_route(self.request, link['url']):
                continue

            links.append({'id': i,
                          'text': link['text'],
                          'url': link['url']})
            if link.get('menu_group'):
                links[-1]['menu_group'] = link['menu_group']
            if link.get('icon'):
                links[-1]['icon'] = link['icon']
            if self.event_name:
                links[-1]['event_name'] = self.event_name

        return links

    @staticmethod
    def default_child_cls(*args, **kwargs):
        kwargs['list_element'] = True
        return Link(*args, **kwargs)

    def is_current_url(self, url):
        return self.page.request.matched_route.path == url
