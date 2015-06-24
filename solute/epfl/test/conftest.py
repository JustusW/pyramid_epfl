from pyramid import testing
import pytest
import inspect

from solute.epfl.core.epflcomponentbase import ComponentBase, ComponentContainerBase
from solute.epfl import get_epfl_jinja2_environment, includeme, epflpage, components
from pyramid_jinja2 import get_jinja2_environment


class DummyRoute(object):
    def __init__(self, name='dummy_route'):
        self.name = name


@pytest.fixture
def route():
    return DummyRoute()


@pytest.fixture
def pyramid_req(route):
    config = testing.setUp()

    testing.DummyRequest.get_jinja2_environment = get_jinja2_environment
    testing.DummyRequest.get_epfl_jinja2_environment = get_epfl_jinja2_environment

    includeme(config)

    config.add_route('dummy_route', pattern='/')

    r = testing.DummyRequest()
    r.matched_route = route
    r.content_type = ''
    r.is_xhr = False
    r.registry.settings['epfl.transaction.store'] = 'memory'

    return r


@pytest.fixture
def pyramid_xhr_req(pyramid_req):
    pyramid_req.is_xhr = True
    return pyramid_req


@pytest.fixture
def page(pyramid_req):
    return epflpage.Page(pyramid_req)


def component_base_type_predicate(cls):
    return inspect.isclass(cls) and issubclass(cls, ComponentBase) and not issubclass(cls, ComponentContainerBase)


def component_container_type_predicate(cls):
    return inspect.isclass(cls) and issubclass(cls, ComponentContainerBase)


@pytest.fixture(
    params=inspect.getmembers(components, predicate=component_base_type_predicate) + [('ComponentBase', ComponentBase)])
def component_base_type_class(request):
    return request.param[1]


@pytest.fixture(
    params=inspect.getmembers(components, predicate=component_container_type_predicate) + [
        ('ComponentContainerBase', ComponentContainerBase)])
def component_container_type_class(request):
    return request.param[1]
