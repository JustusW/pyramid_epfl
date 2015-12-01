

def assert_with_a_twist(name, page, target_value):
    __tracebackhide__ = True

    with_a_twist = '1234'
    assert page.root_node._url is None, '{name} contains unset parameter "with_a_twist" but _url is {_url}'.format(
        _url=page.root_node._url,
        name=name,
    )

    page.request.matchdict['with_a_twist'] = with_a_twist
    assert page.root_node._url == target_value.format(with_a_twist=with_a_twist), \
        '{name} parameter "with_a_twist" set to {with_a_twist} but _url is {_url}'.format(
            with_a_twist=with_a_twist,
            _url=page.root_node._url,
            name=name,
        )

    return target_value.format(with_a_twist=with_a_twist)


def assert_href_is(name, params, compo, target_value):
    __tracebackhide__ = True

    errors = (
        '%s is set to {%s} but rendered html contains href.' % (name, name),
        '%s is set to {%s} but rendered html contains no href.' % (name, name),
        '%s is set to {%s} but rendered html contains wrong href.' % (name, name),
    )

    compo.render_cache = None

    if target_value is None:
        assert 'href=' not in compo.render(), errors[0].format(**params)
    else:
        assert 'href=' in compo.render(), errors[1].format(**params)
        assert 'href="{0}"'.format(target_value) in compo.render(), errors[2].format(**params)


def assert_breadcrumb(compo):
    __tracebackhide__ = True

    assert 'class="breadcrumb-link' in compo.render(), \
        'breadcrumb set to True but class is missing or malformed in html.'

    if compo.is_first():
        assert 'class="breadcrumb-link first"' in compo.render(), \
            'breadcrumb is first in container but class is missing or malformed in html.'
    else:
        assert 'class="breadcrumb-link "' in compo.render(), \
            'breadcrumb is not first in container but class is missing or malformed in html.'

    compo.render_cache = None


def assert_list_element(compo):
    assert 'class="list-group-item col-sm-12' in compo.render(), \
        'list_element set to True but class is missing or malformed in html.'

    if compo.is_current_url():
        assert 'class="list-group-item col-sm-12 active"' in compo.render(), \
            'Link is the current link but active class is missing or malformed in html.'
    else:
        assert 'class="list-group-item col-sm-12"' in compo.render(), \
            'Link is not the current link but active class is present or malformed in html.'

    compo.render_cache = None
