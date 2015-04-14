# coding: utf-8

from solute.epfl.core import epflcomponentbase
from collections2 import OrderedDict as odict


class Simpletree(epflcomponentbase.ComponentBase):
    template_name = "simpletree/simpletree.html"
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["simpletree/simpletree.js"]

    asset_spec = "solute.epfl.components:simpletree/static"

    js_name = ["simpletree.js", ("solute.epfl.components:context_list_layout/static", "contextmenu.js")]

    css_name = ["simpletree.css"]

    compo_config = ['tree_data']
    compo_state = ["tree_data", "search_string", "open_leaf_0_ids", "open_leaf_1_ids", "open_leaf_2_ids",
                   "selected_0_id", "selected_1_id", "selected_2_id", "selected_3_id",
                   "all_filter", "filter_key", "scroll_position",  "is_loading", "load_async", "expanded"]

    tree_data = None

    open_leaf_0_ids = None
    open_leaf_1_ids = None
    open_leaf_2_ids = None
    all_filter = None
    
    expanded = False #: Indicates whether the tree is fully expanded or not.

    height = 400

    search_string = None
    filter_key = None

    scroll_position = 0
    selected_0_id = None
    selected_1_id = None
    selected_2_id = None
    selected_3_id = None

    is_loading = False
    load_async = True

    def handle_scrolled(self, scroll_position):
        """
        Remember the scroll position.
        """
        self.scroll_position = scroll_position

    # TREE DATA
    def reset_tree_data(self):
        self.tree_data = odict()

    def add_level_0(self, data):
        if self.tree_data is None:
            self.tree_data = odict()
        for entry in data:
            self.tree_data[entry['id']] = entry


    def add_level_1(self, data, parent_id):
        self.tree_data[parent_id]["children"] = odict()
        for entry in data:
            self.tree_data[parent_id]["children"][entry['id']] = entry

    def remove_level_1(self, parent_id):
        try:
            del self.tree_data[parent_id]["children"]
        except KeyError:
            pass


    def add_level_2(self, data, level_1_id, level_0_id):
        if not "children" in self.tree_data[level_0_id]:
            return

        if not level_1_id in self.tree_data[level_0_id]["children"]:
            return

        self.tree_data[level_0_id]["children"][level_1_id]["children"] = odict()
        for entry in data:
            self.tree_data[level_0_id]["children"][level_1_id]["children"][entry['id']] = entry
            
    def remove_level_2(self, level_1_id, level_0_id):
        try:
            del self.tree_data[level_0_id]["children"][level_1_id]["children"]
        except KeyError:
            pass
            
    def add_level_3(self, data, level_2_id, level_1_id, level_0_id):
        if not "children" in self.tree_data[level_0_id]:
            return

        if not level_1_id in self.tree_data[level_0_id]["children"]:
            return
        
        if not "children" in self.tree_data[level_0_id]["children"][level_1_id]:
            return

        if not level_2_id in self.tree_data[level_0_id]["children"][level_1_id]["children"]:
            return

        self.tree_data[level_0_id]["children"][level_1_id]["children"][level_2_id]["children"] = odict()
        for entry in data:
            self.tree_data[level_0_id]["children"][level_1_id]["children"][level_2_id]["children"][entry['id']] = entry

    def remove_level_3(self, level_2_id, level_1_id, level_0_id):
        try:
            del self.tree_data[level_0_id]["children"][level_1_id]["children"][level_2_id]["children"]
        except KeyError:
            pass

    def init_transaction(self):
        if self.load_async:
            self.is_loading = True
            self.add_js_response("epfl.Simpletree.LoadData('%s')" % self.cid);
            self.load_async = False
        else:
            self.add_level_0(self.load_level_0())

    def handle_load_data(self):
        self.add_level_0(self.load_level_0())
        self.is_loading = False
        self.redraw()

    def load_level_0(self):
        return []

    def load_level_1(self, upper_leaf_id):
        return []

    def load_level_2(self, upper_leaf_id):
        return []
    
    def load_level_3(self, upper_leaf_id):
        return []

    def rebuild_tree_structure(self):
        self.reset_tree_data()

        self.add_level_0(self.load_level_0())

        if self.open_leaf_0_ids is None:
            self.open_leaf_0_ids = []


        for leafid in self.open_leaf_0_ids:
            if leafid in self.tree_data.keys():
                self.add_level_1(self.load_level_1(leafid), leafid)
            else:
                self.open_leaf_0_ids.remove(leafid)
        deprecated_leaf_1_ids = []
        deprecated_leaf_2_ids = []
        if self.open_leaf_1_ids is None:
            self.open_leaf_1_ids = {}
        if self.open_leaf_2_ids is None:
            self.open_leaf_2_ids = {}
        for level_1_id, leaf_obj in self.open_leaf_1_ids.iteritems():
            if (leaf_obj['level_0_id'] in self.tree_data.keys()) and (
                        'children' in self.tree_data[leaf_obj['level_0_id']]) and (
                        level_1_id in self.tree_data[leaf_obj['level_0_id']]['children'].keys()):
                self.add_level_2(self.load_level_2(level_1_id),
                                 level_1_id, leaf_obj['level_0_id'])
            else:
                deprecated_leaf_1_ids.append(level_1_id)
        for level_2_id, leaf_obj in self.open_leaf_2_ids.iteritems():
            if (leaf_obj['level_0_id'] in self.tree_data.keys()) and \
                ('children' in self.tree_data[leaf_obj['level_0_id']]) and \
                (leaf_obj['level_1_id'] in self.tree_data[leaf_obj['level_0_id']]['children'].keys()) and \
                ('children' in self.tree_data[leaf_obj['level_0_id']]['children'][leaf_obj['level_1_id']]) and \
                (level_2_id in self.tree_data[leaf_obj['level_0_id']]['children'][leaf_obj['level_1_id']]['children'].keys()):
                self.add_level_3(self.load_level_3(level_2_id), level_2_id, leaf_obj['level_1_id'], leaf_obj['level_0_id'])
            else:
                deprecated_leaf_2_ids.append(level_1_id)
        for leaf_id in deprecated_leaf_1_ids:
            del self.open_leaf_1_ids[leaf_id]
        for leaf_id in deprecated_leaf_2_ids:
            del self.open_leaf_2_ids[leaf_id]

        self.redraw()

    def update_level_0(self, recursive=False):
        if recursive:
            self.rebuild_tree_structure()
            return
        level_0_data = self.load_level_0()
        new_tree_data = odict()
        for entry in level_0_data:
            if (entry["id"] in self.tree_data) and ("children" in self.tree_data[entry["id"]]):
                children = self.tree_data[entry["id"]]["children"]
                new_tree_data[entry["id"]] = entry
                new_tree_data[entry["id"]]["children"] = children
            else:
                new_tree_data[entry["id"]] = entry
        self.tree_data = new_tree_data
        self.redraw()

    def update_level_1(self, level_0_id, recursive=False):
        level_1_data = self.load_level_1(level_0_id)
        new_level_1_data = odict()
        recursive_update_ids = []
        for entry in level_1_data:
            if ("children" in self.tree_data[level_0_id]) and (
                        entry["id"] in self.tree_data[level_0_id]["children"]) and (
                        "children" in self.tree_data[level_0_id]["children"][entry["id"]]):
                if recursive:
                    recursive_update_ids.append(entry["id"])
                children = self.tree_data[level_0_id]["children"][entry["id"]]["children"]
                new_level_1_data[entry["id"]] = entry
                new_level_1_data[entry["id"]]["children"] = children
            else:
                new_level_1_data[entry["id"]] = entry
        self.tree_data[level_0_id]["children"] = new_level_1_data
        for recursive_update_id in recursive_update_ids:
            self.update_level_2(level_0_id, recursive_update_id, recursive)

        self.redraw()

    def update_level_1_for_given_level_1_entry(self, level_1_id, recursive=False):
        level_0_id = None
        for entry_id, entry in self.tree_data.iteritems():
            if "children" in entry and (level_1_id in entry["children"].keys()):
                level_0_id = entry_id
                break
        if not level_0_id is None:
            self.update_level_1(level_0_id, recursive)
            
    def update_level_2(self, level_0_id, level_1_id, recursive=False):
        level_2_data = self.load_level_2(level_1_id)
        new_level_2_data = odict()
        recursive_update_ids = []
        for entry in level_2_data:
            if ("children" in self.tree_data[level_0_id]) and \
                (level_1_id in self.tree_data[level_0_id]["children"]) and \
                ("children" in self.tree_data[level_0_id]["children"][level_1_id]) and \
                (entry["id"] in self.tree_data[level_0_id]["children"][level_1_id]["children"]) and \
                ("children" in self.tree_data[level_0_id]["children"][level_1_id]["children"][entry["id"]]):
                if recursive:
                    recursive_update_ids.append(entry["id"])
                children = self.tree_data[level_0_id]["children"][level_1_id]["children"][entry["id"]]["children"]
                new_level_2_data[entry["id"]] = entry
                new_level_2_data[entry["id"]]["children"] = children
            else:
                new_level_2_data[entry["id"]] = entry
        self.tree_data[level_0_id]["children"][level_1_id]["children"] = new_level_2_data

        for recursive_update_id in recursive_update_ids:
            self.update_level_3(level_0_id, level_1_id, recursive_update_id)

        self.redraw()
        
    def update_level_2_for_given_level_2_entry(self, level_2_id, recursive=False):
        level_0_id = None
        level_1_id = None
        for lev_0_id, lev_0_entry in self.tree_data.iteritems():
            if "children" in lev_0_entry:
                for lev_1_id, lev_1_entry in lev_0_entry["children"].iteritems():
                    if "children" in lev_1_entry and (level_2_id in lev_1_entry["children"].keys()):
                        level_1_id = lev_1_id
                        level_0_id = lev_0_id
                        break
                if not level_0_id is None:
                    break
        if not level_0_id is None:
            self.update_level_2(level_0_id, level_1_id, recursive)
            
    def update_level_3(self, level_0_id, level_1_id, level_2_id):
        if self.open_leaf_2_ids is None:
            self.open_leaf_2_ids = {}
        if not level_2_id in self.open_leaf_2_ids.keys():
            return
        level_3_data = self.load_level_3(level_2_id)
        new_level_3_data = odict()
        for entry in level_3_data:
            new_level_3_data[entry["id"]] = entry
        self.tree_data[level_0_id]["children"][level_1_id]["children"][level_2_id]["children"] = new_level_3_data
        self.redraw()

    def handle_leaf_0_clicked(self, leafid, leaf_open):
        pass

    def handle_leaf_0_open(self, leafid, hover):
        self.add_level_1(self.load_level_1(leafid), leafid)

        if self.open_leaf_0_ids is None:
            self.open_leaf_0_ids = []


        if not leafid in self.open_leaf_0_ids:
            self.open_leaf_0_ids.append(leafid)


        self.redraw()


    def handle_leaf_0_close(self, leafid):
        try:
            if self.open_leaf_0_ids is None:
                self.open_leaf_0_ids = []
            self.open_leaf_0_ids.remove(leafid)
        except ValueError:
            pass
        self.remove_level_1(leafid)

        self.redraw()


    def handle_leaf_1_clicked(self, leafid, level_0_id, leaf_open):
        pass


    def handle_leaf_1_open(self, leafid, level_0_id, hover):

        self.add_level_2(self.load_level_2(leafid), leafid, level_0_id)

        if self.open_leaf_1_ids is None:
            self.open_leaf_1_ids = {}

        self.open_leaf_1_ids[leafid] = {"leafid": leafid, "level_0_id": level_0_id}

        self.redraw()

    def handle_leaf_1_close(self, leafid, level_0_id):
        try:

            if self.open_leaf_1_ids is None:
                self.open_leaf_1_ids = {}

            del self.open_leaf_1_ids[leafid]
        except KeyError:
            pass
        self.remove_level_2(leafid, level_0_id)

        self.redraw()
        
    def handle_leaf_2_open(self, leafid, level_1_id, level_0_id, hover):

        self.add_level_3(self.load_level_3(leafid), leafid, level_1_id, level_0_id)

        if self.open_leaf_2_ids is None:
            self.open_leaf_2_ids = {}

        self.open_leaf_2_ids[leafid] = {"leafid": leafid, "level_1_id": level_1_id, "level_0_id": level_0_id}

        self.redraw()

    def handle_leaf_2_close(self, leafid, level_1_id, level_0_id):
        try:

            if self.open_leaf_2_ids is None:
                self.open_leaf_2_ids = {}

            del self.open_leaf_2_ids[leafid]
        except KeyError:
            pass
        self.remove_level_3(leafid, level_1_id, level_0_id)

        self.redraw()

    def handle_leaf_2_clicked(self, leafid, level_1_id, level_0_id, leaf_open):
        # Overwrite for click handling
        pass
    
    def handle_leaf_3_clicked(self, leafid, level_2_id, level_1_id, level_0_id, leaf_open):
        # Overwrite for click handling
        pass

    def handle_drop(self,
                    drag_level, drag_level_0, drag_level_1, drag_level_2, drag_tree_cid,
                    drop_level, drop_level_0, drop_level_1, drop_level_2, drop_tree_cid):
        pass
    
    def expand_all(self):
        """
        Rebuild the tree and expand all closed nodes.
        """
        if self.open_leaf_0_ids is None:
            self.open_leaf_0_ids = []
        if self.open_leaf_1_ids is None:
            self.open_leaf_1_ids = {} 
        for level_0_id in self.tree_data:
            self.tree_data[level_0_id]["children"] = odict()
            if not level_0_id in self.open_leaf_0_ids:
                self.add_level_1(self.load_level_1(level_0_id), level_0_id)
                self.open_leaf_0_ids.append(level_0_id)
            if "children" in self.tree_data[level_0_id]:
                for level_1_id in self.tree_data[level_0_id]["children"]:
                    if not level_1_id in self.open_leaf_1_ids.keys():
                        self.add_level_2(self.load_level_2(level_1_id), level_1_id, level_0_id)
                        self.open_leaf_1_ids[level_1_id] = {"leafid": level_1_id, "level_0_id": level_0_id}
        self.expanded = True
        self.redraw()

    def collapse_all(self):
        """
        Rebuild the tree and collapse all open nodes.
        """
        if self.open_leaf_0_ids is not None:
            self.open_leaf_0_ids = []
        if self.open_leaf_1_ids is not None:
            self.open_leaf_1_ids = {} 
        for level_0_id in self.tree_data:
            if "children" in self.tree_data[level_0_id]:
                del self.tree_data[level_0_id]["children"]
                    
        self.expanded = False
        self.redraw()