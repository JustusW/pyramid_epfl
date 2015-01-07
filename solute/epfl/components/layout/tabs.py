
from solute.epfl.core import epflcomponentbase



class TabsLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "layout/tabs.html"
    js_parts = "layout/tabs.js"
    asset_spec = "solute.epfl.components:layout/static"

    css_name = ["bootstrap.min.css"]
    js_name = ["js/jquery-1.8.2.min.js", "bootstrap.tab.js", "tabs.js"]

    compo_state = ["active_tab_cid"]

    active_tab_cid = ""

    def handle_toggleTab(self, selected_compo_cid):
        self.active_tab_cid = selected_compo_cid
