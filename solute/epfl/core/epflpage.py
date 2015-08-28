# coding: utf-8

import epflcomponentbase, epfltransaction

from collections2 import OrderedDict as odict
from collections import MutableMapping
import jinja2

from pyramid.response import Response
from pyramid import security

import ujson as json
import socket

from solute.epfl.core import epflclient, epflutil, epflacl
from solute.epfl.core.epflutil import Lifecycle


class LazyProperty(object):
    """
    Wrapper function used for just in time initialization of components by calling the registered callback.
    """
    __unbound_component__ = 'LazyProperty'

    def __init__(self, callback):
        self.callback = callback

    def __call__(self):
        self.callback(overwrite=True)


@epflacl.epfl_acl(['access'])
class Page(object):
    """
    Handles the request-processing-flow of EPFL requests for all its contained :class:`.epflcomponentbase.BaseComponent`
    instances. The parameter "name" must be unique for the complete application!

    There are three response-modes:

    - Full Page:
        A complete html-page (including <script>-tags) are returned and rendered by the browser. This is normally
        requested by a link (GET) or a submit (POST)
    - event-queue-response:
        Multiple js-snippets are returned and evaluated at client side. This is requested by a epfl.send(...) request
        from the client side.
    - ajax-json-response:
        A single json-string returned to an manually created ajax-request. (eventually generated by a js-library, called
        on the client by epfl.ajax_request(...) )

    """

    __name = None  #: cached value from get_name()

    asset_spec = "solute.epfl:static"

    #: JavaScript files to be statically loaded.
    js_name = [
        "js/jquery-1.11.3.js",
        "js/jquery-ui.js",
        "js/history.js",
        "js/epfl.js",
        "js/epflcomponentbase.js",
        "js/json2-min.js",
        "js/bootstrap.min.js",
        "js/toastr.min.js"
    ]
    #: JavaScript files to be statically loaded but never in a bundle.
    js_name_no_bundle = []

    #: CSS files to be statically loaded.
    css_name = ["css/epfl.css",
                "css/jquery-ui-lightness/jquery-ui-1.8.23.custom.css",
                "css/font-awesome/css/font-awesome.css",
                "css/bootstrap.min.css",
                "css/toastr.min.css"]
    #: CSS files to be statically loaded but never in a bundle.
    css_name_no_bundle = []

    template = "page.html"  #: The name of the template used to render this page.
    base_html = 'base.html'  #: The template used as base for this page, given in get_render_environment.

    title = 'Empty Page'  #: Title of the page.

    _active_initiations = 0  #: Static count of currently active init cycles.
    remember_cookies = []  #: Cookies used by the authentication mechanism.

    #: Put a class here, it will be instantiated each request by epfl and provided as model. May be a list or a dict.
    model = None
    redrawn_components = None

    def __init__(self, request, transaction=None):
        """
        The optional parameter "transaction" is needed when creating page_objects manually. So the transaction is not
        the same as the requests one.
        The lazy_mode is setup here if the request is an ajax request and all events in it are requesting lazy_mode.

        :param request: Pyramid Request object.
        :param transaction: EPFL Transaction object.
        """
        self.request = request
        self.request.page = self
        self.page_request = PageRequest(request, self)
        self.response = epflclient.EPFLResponse(self)
        self.components = PageComponents(self)  # all registered components of this page

        if transaction:
            self.transaction = transaction

        if not hasattr(self, 'transaction'):
            try:
                self.transaction = self.__get_transaction_from_request()
            except epfltransaction.TransactionRouteViolation:
                # This ensures that a transaction is only used for the route it was created on. A new transaction is
                # created in case of a differing route.
                self.transaction = epfltransaction.Transaction(request)
                self.transaction.set_page_obj(self)

    @Lifecycle(name=('page', 'main'), log_time=True)
    def __call__(self):
        """
        The page is called by pyramid as view, it returns a rendered page for every request. Uses :meth:`call_ajax`,
        :meth:`call_default`, :meth:`call_cleanup`.
        [request-processing-flow]
        """

        self.setup_model()

        # Check if we lost our transaction to a timeout.
        transaction_loss = self.prevent_transaction_loss()
        if transaction_loss:
            return transaction_loss

        self.handle_transaction()

        content_type = "text/html"

        if self.request.is_xhr:
            self.handle_ajax_events()
            content_type = "text/javascript"
        else:
            # Reset the rendered_extra_content list since none actually has been rendered yet!
            self.transaction['rendered_extra_content'] = set()

        self.after_event_handling()

        out = self.render()

        out += self.call_cleanup(self.request.is_xhr)

        response = Response(body=out.encode("utf-8"),
                            status=200,
                            content_type=content_type)
        response.headerlist.extend(self.remember_cookies)
        return response

    @Lifecycle(name=('page', 'after_event_handling'))
    def after_event_handling(self):
        for compo in self.get_active_components():
            compo.after_event_handling()

    @Lifecycle(name=('page', 'prevent_transaction_loss'))
    def prevent_transaction_loss(self):
        """In case the transaction has been lost, we need a full page reload and also a bit of housekeeping on the
        transaction itself.
        """
        if '__initialized_components__' not in self.transaction:
            if self.request.is_xhr:
                return Response(body='window.location.reload();',
                                status=200,
                                content_type='text/javascript')
            self.transaction.set_page_obj(self)

    def call_cleanup(self, check_tid):
        """
        Sub-method of :meth:`__call__` used to cleanup after a request has been handled.
        """
        self.done_request()

        if self.request.params.get('unqueued'):
            return ''

        self.transaction.store()

        if check_tid and self.transaction.tid_new:
            return 'epfl.new_tid("%s");' % self.transaction.tid_new
        return ''

    @Lifecycle(name=('page', 'setup_model'))
    def setup_model(self):
        """
        Used every request to instantiate the model.
        """
        if self.model is not None:
            model = self.model
            if type(self.model) is list:
                self.model = []
                for m in model:
                    self.model.append(m(self.request))
            elif type(self.model) is dict:
                self.model = {}
                for k, v in model.items():
                    self.model[k] = v(self.request)
            else:
                self.model = self.model(self.request)

    def done_request(self):
        """ [request-processing-flow]
        The main request teardown.
        """
        for compo_obj in self.get_active_components():
            if self.transaction.has_component(compo_obj.cid):
                compo_obj.finalize()

        other_pages = self.page_request.get_handeled_pages()
        for page_obj in other_pages:
            page_obj.done_request()

    @classmethod
    def get_name(cls):
        if not cls.__name:
            cls.__name = cls.__module__ + ":" + cls.__name__

        return cls.__name

    @classmethod
    def discover(cls):
        pass

    def __getattribute__(self, item):
        """
        Used to provide special handling for components in lazy_mode. Uses default behaviour of super otherwise. If the
        requested value is an instance of :class:`LazyProperty` it will be called, then reloaded using the default
        behaviour of super.
        """
        if item not in ['components', 'transaction', '_active_initiations', 'request', 'response'] \
                and hasattr(self, 'transaction') \
                and self.transaction.has_component(item):
            return self.transaction.get_component_instance(self, item)

        return super(Page, self).__getattribute__(item)

    def __getitem__(self, key):
        return getattr(self, key)

    def __delitem__(self, key):
        return self.__delattr__(key)

    def __delattr__(self, key):
        value = getattr(self, key)
        if isinstance(value, epflcomponentbase.ComponentBase):
            raise Exception('This shouldn\'t happen!')
        self.__dict__.pop(key)

    def __setattr__(self, key, value):
        """
        By assigning components as attributes to the page, they are registered on this page object. Their name is used
        as cid.
        """
        if isinstance(value, epflcomponentbase.ComponentBase):
            self.add_static_component(key, value)
        else:
            super(Page, self).__setattr__(key, value)  # Use normal behaviour.

    def add_static_component(self, cid, compo_obj, overwrite=False):
        """ Registers the component in the page. """
        if self.request.registry.settings.get('epfl.debug', 'false') == 'true' \
                and self.transaction.get_component(cid) is not None and not overwrite:
            raise Exception('A component with CID %(cid)s is already present in this page!\n'
                            'Existing component: %(existing_compo)r of type %(existing_compo_unbound)r\n'
                            'New component: %(new_compo)r of type %(new_compo_unbound)r\n'
                            'Call epfl.page.add_static_component(cid, compo_obj, overwrite=True) instead of page.cid = '
                            'compo_obj if you really want to do this.' % {'cid': cid,
                                                                          'existing_compo': self.__dict__[cid],
                                                                          'existing_compo_unbound': self.__dict__[
                                                                              cid].__unbound_component__,
                                                                          'new_compo_unbound': compo_obj.__unbound_component__,
                                                                          'new_compo': compo_obj})
        if not self.transaction.has_component(cid):
            self.transaction.set_component(cid, compo_obj)

    def get_active_components(self, sorted_by_depth=False):
        """
        If :attr:`active_components` is set this method returns a list of the :class:`.epflcomponentbase.ComponentBase`
        instances that have registered there upon initialization and are still present on this page.
        """
        active_components = self.transaction.get_active_components()[:]
        if sorted_by_depth:
            active_components.sort(key=lambda x: self.transaction.get_component_depth(x.cid))
        return active_components

    def has_access(self):
        """ Checks if the current user has sufficient rights to see/access this page.
        """

        if security.has_permission("access", self, self.request):
            return True
        else:
            return False

    def __get_transaction_from_request(self):
        """
        Retrieve the correct transaction for the tid this request contains.
        """

        tid = self.page_request.get_tid()
        transaction = epfltransaction.Transaction(self.request, tid)

        if transaction.created:
            transaction.set_page_obj(self)

        return transaction

    @Lifecycle(name=('page', 'setup_components'))
    def setup_components(self):
        """
        Overwrite this function!
        In this method all components needed by this page must be initialized and assigned to the page (self). It is
        called only once per transaction to register the "static" components of this page. No need to call this (super)
        method in derived classes.

        [request-processing-flow]
        """
        self.root_node = self.root_node(self, 'root_node', __instantiate__=True)

    def get_page_init_js(self):
        """ returns a js-snipped which initializes the page. called only once per page """

        opts = {"tid": self.transaction.get_id(),
                "ptid": self.transaction.get_pid(),
                "log_time": self.request.registry.settings.get('epfl.performance_log.enabled') == 'True'}

        return "epfl.init_page(" + json.encode(opts) + ")"

    def get_render_environment(self):
        """ Returns a freshly created dict with all the global variables for the template rendering """

        env = {"epfl_base_html": self.base_html,
               "epfl_base_title": self.title,
               "css_imports": self.get_css_imports,
               "js_imports": self.get_js,
               "root_node": self.root_node}

        env.update([(value.cid, value) for value in self.get_active_components() if value.container_compo is None])
        return env

    @Lifecycle(name=('page', 'render'))
    def render(self):
        """Central entry point for all rendering processes including partial rendering during AJAX requests.

        .. graphviz::

            digraph foo {
                "Page.render" -> "request.is_xhr";
                "Page.render" -> "not request.is_xhr";
                "request.is_xhr" -> "Page.get_active_components" -> "compo.render()" -> "ComponentBase.render";
                "not request.is_xhr" -> "root_node.render()";
                "root_node.render()" -> "ComponentBase.render";
                "ComponentBase.render" -> "EPFLResponse.render_jinja";
                "ComponentBase.render" -> "EPFLResponse.render_ajax_response";
            }

        """
        out = ''

        if not self.request.is_xhr:
            self.root_node.render()
            self.add_js_response(self.root_node.render('js_raw'))

            render_env = self.get_render_environment()
            out = self.response.render_jinja(self.template, **render_env)
        else:
            # Get render entry points.
            for compo in self.get_active_components(sorted_by_depth=True)[:]:
                if compo.redraw_requested and not compo.is_rendered:
                    self.add_js_response("epfl.replace_component('{cid}', {parts})".format(
                        cid=compo.cid,
                        parts=json.encode({'js': compo.render('js_raw'),
                                           'main': compo.render()})))

            extra_content = self.get_css_imports(only_fresh_imports=True) + self.get_js_imports(only_fresh_imports=True)
            if len(extra_content) > 0:
                out = "epfl.handle_dynamic_extra_content([%s]);\r\n" % json.dumps(extra_content)
            out += self.response.render_ajax_response()

        return out

    @Lifecycle(name=('page', 'handle_transaction'))
    def handle_transaction(self):
        """ This method is called just before the event-handling takes place.
        It calles the init_transaction-methods of all components, that the event handlers have
        a complete setup transaction-state.

        [request-processing-flow]
        """

        # Calling self.setup_components once and remember the compos as compo_info and their structure as compo_struct.
        if not self.transaction.get("components_assigned"):
            self.setup_components()
            self.transaction["components_assigned"] = True

        if 'root_node' not in self.transaction['__initialized_components__']:
            self.root_node.init_transaction()
            self.transaction['__initialized_components__'].add('root_node')

        for compo in self.get_active_components():
            compo.setup_component()

    def make_new_tid(self):
        """
        Call this function to create a new transaction to be in effect after this request. The old transaction and its
        state is preserved, the browser navigation allows for easy skipping between both states.
        """
        self.transaction.store_as_new()

    @Lifecycle(name=('page', 'handle_ajax_events'))
    def handle_ajax_events(self):
        """ Is called by the view-controller directly after the definition of all components (self.instanciate_components).
        Returns "True" if we are in a ajax-request. self.render_ajax_response must be called in this case.
        A "False" means we have a full-page-request. In this case self.render must be called.

        [request-processing-flow]
        """

        ajax_queue = self.page_request.get_queue()
        for event in ajax_queue:
            event_type = event["t"]

            if event_type == "ce":  # component-event
                event_id = event["id"]
                cid = event["cid"]
                event_name = event["e"]
                event_params = event["p"]

                component_obj = self.components[cid]
                component_obj.handle_event(event_name, event_params)

            elif event_type == "pe":  # page-event
                event_id = event["id"]
                event_name = event["e"]
                event_params = event["p"]

                event_handler = getattr(self, "handle_" + event_name)
                event_handler(**event_params)

            elif event_type == "upl":  # upload-event
                event_id = event["id"]
                cid = event["cid"]
                component_obj = self.components[cid]
                component_obj.handle_event("UploadFile", {"widget_name": event["widget_name"]})

            else:
                raise Exception("Unknown ajax-event: " + repr(event))

    def handle_redraw_all(self):
        """
        Trigger a redraw for the root_node.
        """
        self.root_node.redraw()

    def handle_log_time(self, time_used):
        request = self.request
        settings = request.registry.settings

        route_name = request.matched_route.name

        key = settings.get(
            'epfl.performance_log.prefix',
            'epfl.performance.{route_name}.{lifecycle_name}'
        ).format(
            host=socket.gethostname().replace('.', '_'),
            fqdn=socket.getfqdn().replace('.', '_'),
            route_name=route_name.replace('.', '_'),
            lifecycle_name="js_parsing",
        )

        epflutil.log_timing(key, time_used, request=self.request)

    def add_js_response(self, js_string):
        """
        Adds the js either to the ajax-response or to the bottom of the page - depending of the type of the request
        """
        if type(js_string) is str:
            js_string += ";"
        if self.request.is_xhr:
            self.response.add_ajax_response(js_string)
        else:
            if type(js_string) is tuple:
                js_string = js_string[1]
            self.response.add_extra_content(epflclient.JSBlockContent(js_string))

    def show_fading_message(self, msg, typ="info"):
        """ Shows a message to the user. The message is non evasive - it will show up and fade away nicely.
        typ = "info" | "ok" | "error" | "success" | "warning"
        """
        self.show_message(msg, typ, fading=True)

    def show_message(self, msg, typ=None, fading=False):
        """
        Displays a simple alert box to the user.
        typ = "info" | "ok" | "error" | "alert" | "warning" | "success"
        """
        js = "epfl.show_message(%s)" % (json.encode({'msg': msg, 'typ': typ, 'fading': fading}))
        self.add_js_response(js)

    def get_names(self, name, only_fresh_names=False):
        names = []
        for compo in [self] + self.get_active_components():
            if not getattr(compo, 'is_rendered', True):
                continue

            name_list = getattr(compo, name)
            if type(name_list) is not list:
                name_list = [name_list]
            for sub_name in name_list:
                if type(sub_name) is not tuple:
                    sub_name = compo.asset_spec, sub_name
                if sub_name in getattr(self, 'bundled_names', []):
                    continue
                static_url = epflutil.create_static_url(self, sub_name[1], sub_name[0])
                if static_url not in names:
                    names.append(static_url)

        if only_fresh_names:
            names = [name for name in names if name not in self.transaction.get('rendered_extra_content', set())]

        return names

    def get_css_imports(self, only_fresh_imports=False):
        """ This function delivers the <style src=...>-tags for all stylesheets needed by this page and it's components.
        It is available in the template by the jinja-variable {{ css_imports() }}
        """
        imports = self.get_names('css_name', only_fresh_names=only_fresh_imports)

        self.transaction.setdefault('rendered_extra_content', set()).update(imports)

        return jinja2.Markup(''.join(['<link rel="stylesheet" type="text/css" href="%s"/>\r\n'
                                      % css for css in imports]))

    def get_js(self):
        return self.get_js_imports() + self.get_js_parts()

    def get_js_parts(self):
        self.add_js_response(self.get_page_init_js())
        return self.response.render_extra_content('footer')

    def get_js_imports(self, only_fresh_imports=False):
        """ This function delivers the <script src=...>-tags for all js needed by this page and it's components.
        Additionally it delivers all generated js-snippets from the components or page.
        It is available in the template by the jinja-variable {{ js_imports() }}
        """
        imports = self.get_names('js_name', only_fresh_names=only_fresh_imports)

        self.transaction.setdefault('rendered_extra_content', set()).update(imports)

        return jinja2.Markup(''.join(['<script type="text/javascript" src="%s"></script>\r\n'
                                      % js for js in imports]))

    def reload(self):
        """ Reloads the complete page.
        Normally, you only need to redraw the components.
        """
        self.add_js_response("epfl.reload_page();")

    def jump(self, route, **route_params):
        """ Jumps to a new page.
        The target is given as route/route_params.
        The transactions (current an target-page-transaction) are not joined and
        therefore are completely unrelated.
        If you need the data of the current page in the next one (or vice versa), you must
        use "page.go_next(...)" instead.
        """

        target_url = self.get_route_path(route, **route_params)

        js = "epfl.jump('" + target_url + "');"
        self.add_js_response(js)

    def jump_extern(self, target_url, target="_blank"):
        """ Jumps to an external URL.
        Do not use this to jump to an internal page of this appliaction. Use page.jump instead.
        """

        js = "epfl.jump_extern('" + target_url + "', '" + target + "');"
        self.add_js_response(js)

    def go_next(self, route=None, target_url=None, **route_params):
        """ Jumps to a new page and relates the transactions as parent/child.
        So in the new page-object you can access the current page-object as self.parent .
        The target is given as route/route_params or as target_url.
        E.g. use this in wizards.
        """

        if route:
            target_url = self.page_request.route_url(route, **(route_params or {}))

        js = "epfl.go_next('" + target_url + "');"
        self.add_js_response(js)

    def remember(self, user_id):
        """
        Expose the remember function of pyramid.security for easy access to the pyramid authorization handler.
        """
        self.remember_cookies = security.remember(self.request, user_id)

    def forget(self):
        """
        Expose the forget function of pyramid.security for easy access to the pyramid authorization handler.
        """
        self.remember_cookies = security.forget(self.request)

    def toast(self, message, message_type):
        raise Exception('This function is deprecated.')

    def get_route_path(self, route, abs_path=False, **kwargs):
        """
        Convenience handle for pyramid.request.route_path.
        """
        if not abs_path:
            return self.request.route_path(route, **kwargs)

        return self.request.route_url(route, **kwargs)


class PageRequest(object):
    """
    Abstraction of the "request"-object provided by pyramid. The framework's request-object is global, so creating
    sub-requests (needed when handling events in page-objects other than the page-object created by the framework's
    request) can be hard. Since all classes of EPFL only rely on this abstraction (page_request) it can be created on
    the fly every time such a page-object needs one specific to it.
    """

    def __init__(self, request, page_obj):
        self.request = request
        self.page_obj = page_obj
        self.handeled_pages = []
        self.upload_mode = False

        if self.request.content_type.startswith("multipart/"):
            self.upload_mode = True
            self.params = request.params
        elif self.request.is_xhr:
            try:
                self.params = request.json_body
            except:
                # TODO: Bad bad hack fix this
                pass
        else:
            self.params = request.params

    def is_upload_mode(self):
        return self.upload_mode

    def get_tid(self):
        return self.params.get("tid")

    def get_queue(self):
        if self.upload_mode:
            return [self.params]
        else:
            return self.params["q"]

    def get(self, key, default=None):
        return self.params.get(key, default)

    def getall(self, key):
        return self.request.params.getall(key)

    def __getitem__(self, key):
        return self.params[key]

    def add_handeled_page(self, page_obj):
        """ This page was created and handeled in this request too! """
        self.handeled_pages.append(page_obj)

    def get_handeled_pages(self):
        return self.handeled_pages

    def get_uploads(self):
        if not self.is_upload_mode:
            return {}
        else:
            return {self.params["widget_name"]: self.request.POST[self.params["widget_name"] + "[]"]}


class PageComponents(object):
    """
    Wrapper dict that just holds the information which component is actually supposed to be present while leaving the
    actual instances stored only in :attr:`Page.__dict__`.
    Implements MutableMapping_.

.. _MutableMapping: https://docs.python.org/2/library/collections.html#collections.MutableMapping
"""

    def __init__(self, page):
        self.page = page

    def __getitem__(self, key):
        return getattr(self.page, key)
