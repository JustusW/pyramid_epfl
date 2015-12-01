# coding: utf-8

"""

"""

import types
import copy

from pyramid import security

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil
import json


class Diagram(epflcomponentbase.ComponentBase):
    asset_spec = "solute.epfl.components:diagram/static"

    template_name = "diagram/diagram.html"
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["diagram/diagram.js"]

    js_name = ["highcharts.js", "exporting.js", "export-csv-1.2.1.js", "diagram.js"]

    compo_state = ["diagram_params"]

    diagram_params = None  #: Dict of diagram parameters. Please consult the highcharts.js documentation.

    def __init__(self, page, cid, diagram_params=None, **extra_params):
        """A component for showing complex diagrams using highcharts.js.

        :param diagram_params: Dict of diagram parameters. Please consult the highcharts.js documentation.
        """
        super(Diagram, self).__init__(page, cid, diagram_params=diagram_params, **extra_params)

    def get_params(self):
        if self.diagram_params is None:
            self.diagram_params = {}
        return self.diagram_params

    def set_params(self, params):
        self.diagram_params = params

    def handle_visibilityChange(self, series_visibility):
        if self.diagram_params is None:
            self.diagram_params = {}
        if not "series" in self.diagram_params:
            return
        for series_visibility_entry in series_visibility:
            if "name" in series_visibility_entry:
                for backed_series_entry in self.diagram_params["series"]:
                    if backed_series_entry["name"] == series_visibility_entry["name"]:
                        if ("visible" in series_visibility_entry) and (series_visibility_entry["visible"] == False):
                            backed_series_entry["visible"] = False
                        elif "visible" in backed_series_entry:
                            backed_series_entry.pop("visible")
