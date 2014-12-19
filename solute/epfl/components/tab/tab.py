
from solute.epfl.core import epflcomponentbase

class Tab(epflcomponentbase.ComponentContainerBase):
    
    template_name = "tab/tab.html"
    asset_spec = "solute.epfl.components:tab/static"

    css_name = ["bootstrap.min.css"]
    js_name = ["bootstrap.tab.js", "tab.js"]


    compo_state = [ "active_tab_cid"]
    
    active_tab_cid = ""
    
    def handle_toggleTab(self, selected_compo_cid):
        self.active_tab_cid = selected_compo_cid
        