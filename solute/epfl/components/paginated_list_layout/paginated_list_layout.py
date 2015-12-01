# coding: utf-8

"""

"""

from solute.epfl.components import PrettyListLayout


class PaginatedListLayout(PrettyListLayout):
    """
    A searchable list layout. Its content is configured using get_data()
    example

    .. code-block:: python

        data = []
        for i in range(0, 100):
            data.append({'id': i, "data": "test" + str(i)})

    """

    show_pagination = True  #: Set to true to show the pagination bar.
    infinite_scrolling = False  #: Set to true to use infinite scrolling pagination.
    show_search = True  #: Set to true to enable the search field.
    search_timeout = 500  #: The timeout in ms until the search event fires
    search_placeholder = "Search..."  #: Placeholder text for the search input.
    #: Specify the number of pages that should be visible in the pagination bar.
    visible_pages_limit = 5
    #: Set this to true in order to reset the row_offset to 0 once the user changes the
    #: search string. This may be useful to avoid scenarios where the components renders page 5,
    #: but the search only returned 2 pages.
    reset_row_offset_on_search_change = False
    infinite_scroll_debounce_delay = 100  #: The delay for scroll debounce in infinite scrolling lists

    search_focus = False  #: Set to true if the search field should receive focus on load.
    search_focus_after_search = True  #: Focus the search input after a search

    theme_path = ['pretty_list_layout/theme', '<paginated_list_layout/theme']

    js_parts = PrettyListLayout.js_parts + ["paginated_list_layout/paginated_list_layout.js"]
    js_name = PrettyListLayout.js_name + [(
        'solute.epfl.components:paginated_list_layout/static',
        'paginated_list_layout.js'
    ), (
        'solute.epfl.components:paginated_list_layout/static',
        'jquery.ba-throttle-debounce.min.js'
    )]

    #: Add the specific list type for the paginated list layout. see :attr:`ListLayout.list_type`
    list_type = PrettyListLayout.list_type + ['paginated']

    def __init__(self, page, cid, show_search=None, show_pagination=None, search_placeholder=None,
                 search_focus=None, visible_pages_limit=None,
                 reset_row_offset_on_search_change=None, height=None,search_focus_after_search=search_focus_after_search,
                 search_timeout=None, infinite_scroll_debounce_delay=None, **kwargs):
        """Paginated list using the PrettyListLayout based on bootstrap. Offers searchbar above and pagination below
        using the EPFL theming mechanism.

        :param show_search: Toggle weather the search field is shown or not.
        :param show_pagination: Toggle weather the pagination is shown or not.
        :param search_placeholder: The placeholder text for the search input.
        :param search_focus: Toggle weather the search field receives focus on load or not.
        :param visible_pages_limit: Specify the number of pages that should be visible in the pagination bar.
        :param reset_row_offset_on_search_change: Reset row_offset once the user changes the search string.
        :param height: Set the list to the given height in pixels.
        :param search_focus_after_search: Focus the search input after a search
        :param search_timeout: The timeout in ms until the search event fires
        :param infinite_scroll_debounce_delay: The delay for scroll debounce in infinite scrolling lists
        """
        super(PaginatedListLayout, self).__init__(page, cid, show_search=show_search,
                                                  show_pagination=show_pagination,
                                                  search_placeholder=search_placeholder,
                                                  search_focus=search_focus,
                                                  visible_pages_limit=visible_pages_limit,
                                                  reset_row_offset_on_search_change=reset_row_offset_on_search_change,
                                                  search_focus_after_search=search_focus_after_search,
                                                  height=height,search_timeout=search_timeout,
                                                  infinite_scroll_debounce_delay=infinite_scroll_debounce_delay,**kwargs)

    def handle_set_row(self, row_offset, row_limit, row_data=None):
        if self.row_data is not None and row_data is not None:
            if self.row_data.get("search", None) != row_data.get("search", None):
                if self.search_focus_after_search:
                    self.search_focus = True
                if self.reset_row_offset_on_search_change:
                    row_offset = 0

        super(PaginatedListLayout, self).handle_set_row(row_offset, row_limit, row_data)
