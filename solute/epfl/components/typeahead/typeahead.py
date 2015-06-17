from solute.epfl.components.grouped_link_list_layout.grouped_link_list_layout import GroupedLinkListLayout


class TypeAhead(GroupedLinkListLayout):
    search_focus = True  #: Focus on the search input field on load.
    show_search = True  #: Show the search input field.
    use_headings = True  #: Sets GroupedLinkListLayout to show headings instead of submenus.

    js_parts = []
    js_name = GroupedLinkListLayout.js_name + [('solute.epfl.components:typeahead/static', 'typeahead.js')]

    new_style_compo = True
    compo_js_name = 'TypeAhead'
    compo_js_params = GroupedLinkListLayout.compo_js_params + ['row_offset', 'row_limit', 'row_count', 'row_data',
                                                               'show_pagination', 'show_search', 'search_focus']
    compo_js_extras = ['handle_click']

    theme_path = GroupedLinkListLayout.theme_path.copy()
    theme_path['before'] = ['pretty_list_layout/theme', '>paginated_list_layout/theme', '>typeahead/theme']

    data_interface = {
        'id': None,
        'text': None
    }

    @property
    def hide_list(self):
        """The list container is supposed to be hidden if no entries are available.
        """
        return len(self.components) == 0

    def __init__(self, page, cid, links=None, use_headings=None, event_name=None, show_search=None, height=None,
                 **kwargs):
        """TypeAhead component that offers grouping of entries under a common heading. Offers search bar above and
        pagination below using the EPFL theming mechanism. Links given as parameters are checked against the existing
        routes automatically showing or hiding them based on the users permissions. Entries can be grouped below a
        common heading given in the menu_group entry.

        .. code-block:: python

            components.TypeAhead(
                event_name='selected_category',
                links=[
                    {'text': 'foo0', 'url': '#foo', 'menu_group': 'bar'},
                    {'text': 'foo1', 'url': '#foo', 'menu_group': 'bar'},
                    {'text': 'foo2', 'url': '#foo', 'menu_group': 'bar2'},
                    {'text': 'foo3', 'url': '#foo', 'menu_group': 'bar2'},
                    {'text': 'foo3', 'url': '#foo', 'menu_group': 'bar2'},
                    {'text': 'foo3', 'url': '#foo', 'menu_group': 'bar2'},
                    {'text': 'foo3', 'url': '#foo', 'menu_group': 'bar2'},
                ]
            )

        :param links: List of dicts with text and url. May contain an icon and a menu_group entry.
        :param use_headings: Use menu_group strings as headings instead of submenus.
        :param event_name: The name of an event to be triggered instead of rendering normal links.
        :param height: Set the list to the given height in pixels.
        :param show_search: Toggle weather the search field is shown or not.
        :param show_pagination: Toggle weather the pagination is shown or not.
        :param search_focus: Toggle weather the search field receives focus on load or not.
        """
        super(GroupedLinkListLayout, self).__init__(page, cid, links=None, use_headings=None, event_name=None,
                                                    show_search=None, height=None, **kwargs)
