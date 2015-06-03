# coding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import PaginatedListLayout


class TextList(PaginatedListLayout):
    """
    Text List is simple list which displays text
    """
    default_child_cls = epflcomponentbase.ComponentBase
    data_interface = {'id': None,
                      'text': None}

    theme_path = {'default': PaginatedListLayout.theme_path,
                  'row': ['text_list/theme']}

    compo_state = PaginatedListLayout.compo_state + ["search_text"]

    search_text = None


    def __init__(self,page,cid, data_interface=None, *args, **extra_params):
        """
        Text List is simple list which displays text
        :param data_interface: data interface for child class needs id and text
        """
        super(TextList, self).__init__(page,cid,data_interface=data_interface, *args, **extra_params)

    def handle_set_row(self, row_offset, row_limit, row_data=None):
        if row_data is not None:
            self.search_text = row_data.get("search")
        self.update_children()
        self.redraw()
