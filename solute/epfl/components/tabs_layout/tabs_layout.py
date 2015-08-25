from solute.epfl.core import epflcomponentbase


class TabsLayout(epflcomponentbase.ComponentContainerBase):
    asset_spec = "solute.epfl.components:tabs_layout/static"
    template_name = "tabs_layout/tabs_layout.html"

    compo_state = ["active_tab_cid"]

    js_parts = epflcomponentbase.ComponentContainerBase.js_parts + ["tabs_layout/tabs_layout.js"]
    js_name = ["tabs_layout.js"]

    active_tab_cid = ""  #: CID of the currently active tab.

    def __init__(self, page, cid, **extra_params):
        """A Layouting component displaying its children inside separate tabs.
        """
        super(TabsLayout, self).__init__(page, cid, **extra_params)

    def render(self, target='main'):
        """Just before the normal rendering the visibility of all child components needs to be updated.
        """
        for i, compo in enumerate(self.components):
            if self.is_active_tab(i, compo):
                compo.set_visible()
            else:
                compo.set_hidden()

        return super(TabsLayout, self).render(target=target)

    def handle_toggle_tab(self, selected_compo_cid):
        if self.active_tab_cid != selected_compo_cid:
            self.redraw()
        self.active_tab_cid = selected_compo_cid
        self.add_js_response("$('#%s_tabmenuentry').tab('show');" % self.active_tab_cid)

    def del_component(self, cid, slot=None):
        position = None
        if cid.cid == self.active_tab_cid:
            position = self.components.index(cid)
        super(TabsLayout, self).del_component(cid, slot)
        if position > 0:
            self.handle_toggle_tab(self.components[position-1].cid)
            self.redraw()

    def is_active_tab(self, loop, compo_obj):
        """Check whether the component is the currently active tab or the first tab if no cid has been set as active.
        """
        if type(loop) is not int:
            loop = loop.index
        return (self.active_tab_cid == "" and loop == 1) or (self.active_tab_cid == compo_obj.cid)
