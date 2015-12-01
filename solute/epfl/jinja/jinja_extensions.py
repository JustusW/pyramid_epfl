# coding: utf-8

import time
import ujson as json
import jinja2
from jinja2 import nodes, Markup
from jinja2.ext import Extension
from jinja2.lexer import Token

def ping(arg):
    print "PING", repr(arg)


def format_bool(value):
    if value:
        return 'true'
    else:
        return 'false'

def tojson_ifjson(value):
    if isinstance(value, str) or isinstance(value, unicode):
        return value
    else:
        return json.encode(value)

def tojson(value):
    return Markup(json.encode(value))

def nony(value):
    if value is None:
        return ""
    else:
        return value

def checked_if_equal(value, comparison):
    return "CHECKED" if value == comparison else ""

def selected_if_equal(value, comparison):
    return "SELECTED" if value == comparison else ""

def optional_html_attr(value, attr_name):
    if not value:
        return ""
    else:
        value = unicode(value).replace("\"", "\\\"")
        return jinja2.Markup("{attr_name}={value}".format(attr_name = attr_name, value = jinja2.escape(value)))

def field_states(states):
    if states:
        state_list = []

        if 'writeable' in states and states['writeable'] is False:
           state_list.append(u'readonly="READONLY"')
        if 'enabled' in states and states['enabled'] is False:
           state_list.append(u'disabled="DISABLED"')
        if 'mandatory' in states and states['mandatory'] is True:
         state_list.append(u'required="REQUIRED"')

        return jinja2.Markup(u' '.join(state_list))


class EpflComponentExtension(Extension):

    tags = set(['compo', "compodef", "compopartdef", "component_exports", "compopart"])

    def __init__(self, environment):
        super(EpflComponentExtension, self).__init__(environment)

        self.environment.epfl_compoext_data = {}

    def filter_stream(self, stream):

        self.environment.epfl_compoext_data[stream.name] = {"component_exports": [], # these values are accessed from
                                                            "component_parents": {}, # epfl-page
                                                            "component_children": {}}

        lineno = 0
        for token in stream:
            yield token
            lineno = token.lineno + 1

        yield Token(lineno, 'block_begin', None)
        yield Token(lineno, 'name', 'component_exports')
        yield Token(lineno, 'block_end', None)

    def parse(self, parser):
        """
        Syntax is:

        Only inside a template:
        {% compo COMPO-ID[:COMPO_PART_NAME](kwargs) %}
            ...
        {% endcompo %}
        This calls the component-main-macro (or another part using the ":" syntax) of a defined (in the page) macro.
        The logic is nearly the same as a {% call ... %}-statement. In the called component, there is
        the component it self available as "self" and the body of the {% compodef ... %}-call as "caller".

        Only inside a component-template (as the component definition):
        {% compodef (arg1, arg2, ...) %}
            ...
        {% endcompodef %}
        This defines the main-component-part of the component itself. It does not render the component.

        Only inside a component-template (as the component definition):
        {% compopartdef PART_NAME (arg1, args2, ...) %}
            ...
        {% endcompopartdef %}
        This defines a component-part. You can access it by self.parts.PART_NAME (self beeing the component). It renders nothing.
        A special part-name is "js" which denotes the javascript shipped with the component.

        Inside the all statements you have the component bound to {{self}}.
        """

        token = parser.stream.next()

        if token.value == "compopartdef":
            return self.parse_componentpart(parser, token)
        elif token.value == "compopart":
            return self.parse_part(parser, token)
        elif token.value == "compodef":
            return self.parse_componentdef(parser, token)
        elif token.value == "compo":
            return self.parse_component(parser, token)
        elif token.value == "component_exports":
            return self.parse_component_exports(parser, token)

    def make_open_div(self, id):
        return nodes.TemplateData("<div id=\"" + id + "\">")

    def make_close_div(self):
        return nodes.TemplateData("</div>")

    def parse_component(self, parser, token):


        # first: just make a call to the corresponding macro of the component.
        # now define a second - nearly identical macro - for redrawing
        # "node" is the node which will be returned in place
        node = nodes.CallBlock(lineno = token.lineno)

        node.call = parser.parse_expression()

        if not isinstance(node.call, nodes.Call):
            parser.fail('the component call must be a "call": {% compo compo_name() %}', node.lineno)
        component_name = node.call.node.name

        if parser.stream.current.type == 'lparen':
            parser.parse_signature(node)
        else:
            node.args = []
            node.defaults = []

        original_body = parser.parse_statements(('name:endcompo',), drop_needle=True)

        # inject a {% set self = COMPO_OBJ %}
        assign_node = nodes.Assign()
        assign_node.target = nodes.Name("self", "store")
        assign_node.node = nodes.Name(component_name, "load")

        node.body = [assign_node] + original_body # node gets the additional "self"-hack

##        # overwrites the local-name of the compo {% set COMPO_OBJ = self %}
##        rev_assign_node = nodes.Assign()
##        rev_assign_node.target = nodes.Name(component_name, "store")
##        rev_assign_node.node = nodes.Name("self", "load")

        return node


    def parse_componentpart(self, parser, token):
        node = nodes.Macro(lineno = token.lineno)
        node.name = "compopart_" + parser.stream.expect('name').value
        parser.parse_signature(node)
        node.args = [nodes.Name("self", "param"), nodes.Name("has_caller", "param")] + node.args# + [nodes.Name("caller", "param")]
        node.body = parser.parse_statements(('name:endcompopartdef',), drop_needle=True)
        return node

    def parse_part(self, parser, token):

        node = nodes.Macro(lineno = token.lineno)
        part_name = parser.stream.expect('name').value
        node.name = "compopart_" + part_name
        parser.parse_signature(node)
        node.args = [nodes.Name("self", "param"), nodes.Name("has_caller", "param")] + node.args# + [nodes.Name("caller", "param")]

        assign_node = nodes.Assign()
        assign_node.target = nodes.Name("dummy", "store")

        call_node = nodes.Call()
        call_node.node = nodes.Getattr()
        call_node.node.node = nodes.Name("self", "load")
        call_node.node.attr = "overwrite_compopart" # calls the method "self.overwrite_compopart()" from the components
        call_node.node.ctx = "load"
        call_node.args = [nodes.Const(part_name), 
                                 nodes.Name('compopart_' + part_name, 'load')]
        call_node.kwargs = []
        call_node.dyn_args = None
        call_node.dyn_kwargs = None

        assign_node.node = call_node

        node.body = parser.parse_statements(('name:endcompopart',), drop_needle=True)

        return [node, assign_node]

    def parse_componentdef(self, parser, token):
        node = nodes.Macro(lineno = token.lineno)
        node.name = "main"
        parser.parse_signature(node)
        node.args = [nodes.Name("self", "param"), nodes.Name("has_caller", "param")] + node.args# + [nodes.Name("caller", "param")]
        node.body = parser.parse_statements(('name:endcompodef',), drop_needle=True)
        return node

    def parse_component_exports(self, parser, token):
        compo_exports = self.environment.epfl_compoext_data[parser.stream.name]["component_exports"]
        return compo_exports

def extend_environment(env):
    """ this one extends the global namespace of all processed jinja templates """
    env.filters["tojson"] = tojson
    env.filters["tojson_ifjson"] = tojson_ifjson
    env.filters["format_bool"] = format_bool
    env.filters["nony"] = nony
    env.filters["checked_if_equal"] = checked_if_equal
    env.filters["selected_if_equal"] = selected_if_equal
    env.filters["optional_html_attr"] = optional_html_attr
    env.filters["field_states"] = field_states

    env.globals["ping"] = ping
    env.globals["ctime"] = time.ctime

def get_jinja_extensions():
    """ this one returns a list of 'regular' jinja2 extensions used with epfl """
    # return [EpflComponentExtension, jinja2.ext.do]
    return [jinja2.ext.do]
