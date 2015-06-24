# coding: utf-8
from solute.epfl.components import LinkListLayout
from collections2 import OrderedDict


class GroupedLinkListLayout(LinkListLayout):
    css_name = LinkListLayout.css_name + [('solute.epfl.components:grouped_link_list_layout/static',
                                           'grouped_link_list_layout.css')]

    template_name = "grouped_link_list_layout/grouped_link_list_layout.html"
    data_interface = {'id': None,
                      'text': None,
                      'url': None,
                      'menu_group': None}

    use_headings = False  #: Use menu_group strings as headings instead of submenus.

    #: Add the specific list type for the grouped list layout. see :attr:`ListLayout.list_type`
    list_type = LinkListLayout.list_type + ['grouped']

    def __init__(self, page, cid, links=None, use_headings=None, event_name=None, show_search=None, height=None,
                 **kwargs):
        """Paginated list using the PrettyListLayout based on bootstrap. Offers search bar above and pagination below
        using the EPFL theming mechanism. Links given as parameters are checked against the existing routes
        automatically showing or hiding them based on the users permissions. Entries can be grouped in submenus or below
        a common heading given in the menu_group entry.

        The format of menu_group entries can either be string or tuple. The later being used to allow selection of text
        to be marked with the html MARK-Tag. The tuple should look like this: ("group name", (sel_start, sel_end)) with
        sel_start and sel_end being integers used to slice the string "group name".

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

    @property
    def groups(self):
        groups = OrderedDict()

        for compo in self.components:
            if getattr(compo, 'menu_group', None):
                groups.setdefault(compo.menu_group, {}).setdefault('components', []).append(compo)
                groups[compo.menu_group]['icon'] = getattr(compo, 'icon', None)
                groups[compo.menu_group]['type'] = 'group'
                group_name = compo.menu_group
                if type(compo.menu_group) is tuple:
                    group_name, groups[compo.menu_group]['selection'] = group_name

                groups[compo.menu_group]['name'] = group_name
            else:
                groups.setdefault(compo.cid, {}).setdefault('components', []).append(compo)
                groups[compo.cid]['type'] = 'entry'

        return groups.values()
