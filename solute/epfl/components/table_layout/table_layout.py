from solute.epfl.components import PaginatedListLayout
from collections2.dicts import OrderedDict


class TableLayout(PaginatedListLayout):
    js_parts = PaginatedListLayout.js_parts + ['table_layout/table_layout.js']
    js_name = PaginatedListLayout.js_name + [('solute.epfl.components:table_layout/static',
                                              'table_layout.js'),
                                             ('solute.epfl.components:table_layout/static',
                                              'jquery.fixedheadertable.min.js')]
    css_name = PaginatedListLayout.css_name + [("solute.epfl.components:table_layout/static", "css/table_layout.css")]

    template_name = 'table_layout/table_layout.html'

    map_child_cls = {}

    def __init__(self, page, cid, show_search=None, height=None, **kwargs):
        """Table based on a paginated list. Offers searchbar above and pagination below using the EPFL theming
        mechanism.

        components.TableLayout(
            get_data='objects',
            show_search=False,
            headings=[
                {'title': 'Name'},
                {'title': 'Wert'},
                {'title': 'Einheit'},
            ],
            map_child_cls=[
                ('name', components.Text, {'value': 'name'}),
                ('value', components.Text, {'value': 'value'}),
                ('unit', components.Text, {'value': 'unit'}),
            ],
            data_interface={
                'id': None,
                'name': None,
                'value': None,
                'unit': None,
            }
        )

        :param height: Set the table to the given height in pixels.
        :param show_search: Toggle weather the search field is shown or not.
        :param show_pagination: Toggle weather the pagination is shown or not.
        :param search_focus: Toggle weather the search field receives focus on load or not.
        """
        super(PaginatedListLayout, self).__init__(page, cid, show_search=None, height=height, **kwargs)

    def default_child_cls(self, **compo_info):
        return self.map_child_cls[compo_info['compo_type']][1](**compo_info)

    def _get_data(self, *args, **kwargs):
        result = super(TableLayout, self)._get_data(*args, **kwargs)
        out = []
        child_maps = list(enumerate(self.map_child_cls))
        for row in result:
            for i, child_map in child_maps:
                if len(child_map) == 3:
                    key, cls, interface = child_map
                else:
                    key, cls = child_map
                    interface = {}

                data = {'row': row,
                        'key': key,
                        'compo_type': i,
                        'id': "%s_%s" % (row['id'], i)}

                for key, value in interface.items():
                    data[key] = row[value]

                out.append(data)

        return out

    @property
    def slotted_components(self):
        slotted_components = OrderedDict()
        for compo in self.components:
            slotted_components.setdefault(compo.row['id'], []).append(compo)
        return slotted_components