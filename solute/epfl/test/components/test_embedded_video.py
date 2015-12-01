# * encoding: utf-8

from lxml import etree

from solute.epfl import components


def test_render_with_no_options(page):
    page.root_node = components.EmbeddedVideo(
    )
    page.handle_transaction()

    compo = page.root_node
    compo_html = etree.fromstring(compo.render())
    assert compo_html.attrib.get('epflid', None) == "%s" % compo.cid, "epflid not found"
    assert compo_html.attrib.get('id', None) == "%s" % compo.cid, "id not found"
    assert compo_html.attrib.get('class', None) == "epfl-embedded-video", "class not found"
    assert len(compo_html) == 0, "wrong template output"

def test_render_youtube(page):
    page.root_node = components.EmbeddedVideo(
        video_type= components.EmbeddedVideo.VIDEO_TYPE_YOUTUBE,
        video_id = "this_id_dont_exits",
        force_youtube_html5=False
    )
    page.handle_transaction()

    compo = page.root_node
    assert "iframe" in compo.render(), "iframe not found"
    assert 'src="https://www.youtube.com/embed/this_id_dont_exits"' in compo.render(), "iframe src wrong or not found"
    assert 'width="100%"' in compo.render(), "iframe wrong size"
    assert 'height="100%"' in compo.render(), "iframe wrong size"

def test_render_vimeo(page):
    page.root_node = components.EmbeddedVideo(
        video_type= components.EmbeddedVideo.VIDEO_TYPE_VIMEO,
        video_id = "this_id_dont_exits"
    )
    page.handle_transaction()

    compo = page.root_node
    assert "iframe" in compo.render(), "iframe not found"
    assert 'src="https://player.vimeo.com/video/this_id_dont_exits"' in compo.render(), "iframe src wrong or not found"
    assert 'width="100%"' in compo.render(), "iframe wrong size"
    assert 'height="100%"' in compo.render(), "iframe wrong size"

def test_render_width_height(page):
    page.root_node = components.EmbeddedVideo(
        video_type= components.EmbeddedVideo.VIDEO_TYPE_YOUTUBE,
        video_id = "this_id_dont_exits",
        width="250px",
        height="150px",
        force_youtube_html5=False
    )
    page.handle_transaction()

    compo = page.root_node
    assert "iframe" in compo.render(), "iframe not found"
    assert 'src="https://www.youtube.com/embed/this_id_dont_exits"' in compo.render(), "iframe src wrong or not found"
    assert 'width="250px"' in compo.render(), "iframe wrong size"
    assert 'height="150px"' in compo.render(), "iframe wrong size"

