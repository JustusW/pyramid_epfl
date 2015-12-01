#! -*- coding: utf-8 -*-
"""
Source: https://github.com/admire93/mmcq.py
Modified by mast: __init__.py use pillow instead of wand for pixel data
Algorithm is mmcq based on Color quantization using modified median cut by Dan S. Bloomb
http://www.leptonica.com/papers/mediancut.pdf
"""
from contextlib import contextmanager

from .constant import SIGBITS
from .quantize import mmcq

from PIL import Image


@contextmanager
def get_palette(blob, color_count=10,compress_image=False):
    with Image.open(blob) as image:
        if compress_image:
            image.thumbnail(size=(200, 200))
        c_map = mmcq([pixel for pixel in image.getdata()], color_count)
        yield c_map.palette
