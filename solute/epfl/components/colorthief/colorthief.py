# * encoding: utf-8

from solute.epfl.components.form.form import FormInputBase
from urllib2 import urlopen
import io
from solute.epfl.components.colorthief.mmcq import get_palette


class ColorThief(FormInputBase):
    js_name = FormInputBase.js_name + [("solute.epfl.components:colorthief/static", "colorthief.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:colorthief/static", "colorthief.css")]
    template_name = "colorthief/colorthief.html"
    js_parts = []
    compo_state = FormInputBase.compo_state + ["image_src", "dominat_colors_count"]

    height = None  #: Compo height in px if none nothing is set

    width = None  #: Compo width in px if none nothing is set

    image_src = None  #: image src if set the drop zone is hidden

    color_count = 7  #: Count of colors which got extracted from the image

    new_style_compo = True
    compo_js_params = ['fire_change_immediately', 'color_count']
    compo_js_name = 'ColorThief'
    compo_js_extras = ['handle_click', 'handle_drop']

    def __init__(self, page, cid, height=None, width=None, image_src=None, color_count=None, **extra_params):
        """ColorThief Compo: A Drop Area where images can be dropped and their colors get extracted

        :param height: Compo height in px if none nothing is set
        :param width: Compo width in px if none nothing is set
        :param image_src: image src if set the drop zone is hidden
        :param color_count: Count of colors which got extracted from the image
        :return:
        """
        super(ColorThief, self).__init__(page=page, cid=cid, height=height, width=width, image_src=image_src,
                                         color_count=color_count, **extra_params)

    def __new__(cls, *args, **config):
        try:
            import PIL
        except ImportError:
            raise ImportError("Colorthief needs pillow, "
                              "check: http://pillow.readthedocs.org/installation.html#basic-installation ")
        
        return super(ColorThief, cls).__new__(cls,*args,**config)

    def handle_change(self, value, image_src=None):
        if image_src is not None:
            dominant_colors = set(self.get_dominant_colors_from_url(image_src, color_count=self.color_count))
            self.value = [{"rgb": "#%x%x%x" % (val[0], val[1], val[2]), "selected": False} for val in dominant_colors]
        else:
            self.value = None
        self.image_src = image_src
        self.redraw()

    def handle_drop_accepts(self, cid, moved_cid):
        self.add_ajax_response('true')

    def handle_click_color(self, color):
        for val in self.value:
            if val["rgb"] == color:
                val["selected"] = not val["selected"]
                break

        self.redraw()

    def get_dominant_colors_from_url(self, url, color_count=8):
        """Fetch the image from the url and extract the dominant colors

        :param url: image url
        :param color_count: count of dominant colors
        """
        bytes = io.BytesIO(urlopen(url).read())
        with get_palette(blob=bytes, color_count=color_count) as palette:
            return palette
