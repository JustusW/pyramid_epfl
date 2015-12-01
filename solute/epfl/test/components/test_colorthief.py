# * encoding: utf-8

from __future__ import unicode_literals
from lxml import etree

from solute.epfl import components


def test_render_with_no_options(page):
    page.root_node = components.ColorThief(
    )
    page.handle_transaction()

    compo = page.root_node
    compo_html = etree.fromstring(compo.render())
    assert compo_html.attrib.get('epflid', None) == "%s" % compo.cid, "epflid not found"
    assert compo_html.attrib.get('id', None) == "%s" % compo.cid, "epflid not found"
    assert compo_html.attrib.get('class', None) == "epfl-colorthief", "epflid not found"

    dropzone = compo_html.find("div[@class='epfl-colorthief-dropzone text-center']")
    assert dropzone is not None, "No Dropzone found"
    assert dropzone.find("i") is not None, "No icon in Dropzone found"

    img = compo_html.find("img[@class='epfl-colorthief-image']")
    assert img is not None, "Could not found image"
    assert img.attrib.get("data-cid", None) == "%s" % compo.cid, "image has no or wrong data-cid attribute"


def test_render_with_options(page):
    page.root_node = components.ColorThief(
        height=250,
        width=150,
        image_src="test.png"
    )
    page.handle_transaction()

    compo = page.root_node
    compo_html = etree.fromstring(compo.render())
    assert compo_html.attrib.get("style", None) == "height:250px; width:150px;", "Height and Width not set"
    remove_icon = compo_html.find("i[@class='fa fa-times fa-lg text-danger epfl-colorthief-remove-icon']")
    assert remove_icon is not None, "No remove icon found"

    img = compo_html.find("img[@class='epfl-colorthief-image']")
    assert img is not None, "Could not found image"
    assert img.attrib.get("src", None) == "test.png", "Image src not set"


def test_change(page):
    page.root_node = components.ColorThief(
    )
    page.handle_transaction()

    compo = page.root_node
    compo_html = etree.fromstring(compo.render())

    assert compo.get_value() is None, "Wrong default value"
    assert compo.image_src is None, "Wrong default image_src"

    image_url = "http://img.billiger.de/dynimg/fDOSgmniU-I6cJkqJkaG0p-Y2ZWCCa7D3DrU21LmKOZAF4c0q9hDHVZIsylZxw-LKyiGUplXAslyh82QGAHE-6ijM_eUuPnKi8t5Uc1ly_S/Apple-MacBook-Pro-Retina-15-4-i7-2-2GHz-16GB-RAM-256GB-SSD-MJLQ2D-A.jpg"
    compo.handle_change(value=None, image_src=image_url)

    compo.render_cache = None
    compo_html = etree.fromstring(compo.render())

    assert compo.get_value() is not None, "Wrong value after handle change"
    assert compo.image_src == image_url, "wrong image_src after handle_change"

    color_divs = compo_html.findall("div[@class='epfl-colorthief-color pull-left text-center']")
    assert len(color_divs), "No or not all color divs got renderd"
