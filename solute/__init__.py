from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
try:
    from solute.init import *
except (ImportError,):
    pass
