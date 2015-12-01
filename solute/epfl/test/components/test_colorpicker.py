# * encoding: utf-8

from __future__ import unicode_literals
from solute.epfl import components


def test_render_with_no_options(page):
    page.root_node = components.ColorPicker(
        value_options=[]
    )
    page.handle_transaction()

    compo = page.root_node

    assert 'class="epfl-colorpicker"' in compo.render(), 'general rendering problem class'
    assert 'id="%s' % compo.cid in compo.render(), 'general rendering problem id'
    assert 'epflid="%s"' % compo.cid in compo.render(), 'general rendering problem epflid'
    assert 'class="epfl-colorpicker-colorfield"' not in compo.render(), "a field got rendered where no one is excepted"
    assert 'class="epfl-colorpicker-specialfield"' not in compo.render(), "a field got rendered where no one is excepted"


def test_render_with_rgb_values(page):
    page.root_node = components.ColorPicker(
        value_options=[{"data": "#FFFFFF", "type": components.ColorPicker.TYPE_RGB, "text": "white"},
                       {"data": "#000000", "type": components.ColorPicker.TYPE_RGB, "text": "black"}]
    )

    page.handle_transaction()

    compo = page.root_node
    assert 'class="epfl-colorpicker-colorfield pull-left text-center"' in compo.render(), "no rgb color field found"
    assert 'title="#FFFFFF white"' in compo.render(), "white color field not found"
    assert 'title="#000000 black"' in compo.render(), "black color field not found"
    assert 'style="background-color: #FFFFFF"' in compo.render(), "white color field not found by style"
    assert 'style="background-color: #000000"' in compo.render(), "black color field not found by style"


def test_render_with_special_values(page):
    page.root_node = components.ColorPicker(
        value_options=[{"data": "transparent", "type": components.ColorPicker.TYPE_SPECIAL, "text": "transparent"},
                       {"data": "color", "type": components.ColorPicker.TYPE_SPECIAL, "text": "color"}]
    )

    page.handle_transaction()

    compo = page.root_node
    assert 'class="epfl-colorpicker-specialfield pull-left text-center"' in compo.render(), "no special field found"
    assert 'title="transparent transparent"' in compo.render(), "transparent field not found"
    assert 'title="color color"' in compo.render(), "color field not found"


def test_change(page):
    page.root_node = components.ColorPicker(
        value_options=[{"data": "#FFFFFF", "type": components.ColorPicker.TYPE_RGB, "text": "white"},
                       {"data": "#000000", "type": components.ColorPicker.TYPE_RGB, "text": "black"},
                       {"data": "transparent", "type": components.ColorPicker.TYPE_SPECIAL, "text": "transparent"},
                       {"data": "color", "type": components.ColorPicker.TYPE_SPECIAL, "text": "color"}]
    )

    page.handle_transaction()
    compo = page.root_node

    assert compo.get_value() == None, "wrong default value"
    assert '<i class="fa fa-check fa-lg text-primary"></i>' not in compo.render(), "check icon found before handle change"

    compo.handle_change("#FFFFFF")  # Click the white color field
    compo.render_cache = None

    assert compo.get_value() == [
        {u'type': 0, u'data': u'#FFFFFF', u'text': u'white'}], "value incorrect after handle change"
    assert '<i class="fa fa-check fa-lg text-primary"></i>' in compo.render(), "check icon not found after handle change"

    compo.handle_change("transparent")  # click the transparent special color field
    compo.render_cache = None

    assert compo.get_value() == [{u'type': 0, u'data': u'#FFFFFF', u'text': u'white'},
                                 {u'type': 1, u'data': u'transparent',
                                  u'text': u'transparent'}], "value incorrect after handle change"

    assert 'style="background-color: #000000"' in compo.render(), "check color not found after handle change"

    compo.handle_change("#FFFFFF")  # click the white color field again to remove it from selection
    compo.render_cache = None

    assert compo.get_value() == [
        {u'data': u'transparent', u'type': 1, u'text': u'transparent'}], "value incorrect after handle change"
    assert '<i class="fa fa-check fa-lg text-primary"></i>' in compo.render(), "check icon not found after handle change"

    compo.handle_change("transparent")  # click the transparent special color field again to remove it from selection
    compo.render_cache = None

    assert compo.get_value() == [], "value incorrect after handle change"
    assert 'style="background-color:#00FF00"' not in compo.render(), "check color not found after handle change"
