#* coding: utf-8

from solute.epfl.core import epflconfig
from zope.interface import Interface, implements
import ujson as json

# the interfaces:

class ITempDataProvider(Interface):
    """ A TempDataProvider must be able to store large binary data at least
    the life-time of a session. 
    It is only responsible for storing the data. The GC must be implemented
    at a higher level.
    """

    def __init__(self, config):
        pass
    
    def get(self, request, key, default = None):
        pass

    def set(self, request, key, value):
        pass

    def delete(self, request, key):
        pass


class INodeGlobalDataProvider(Interface):
    """ A GlobalDataProvider must be able to store not so large python objects
    for at least the life-time of the server process.
    No GC neccesary.
    """

    def __init__(self, config):
        pass



class LocalMemoryProvider(object):
    """ Does what it is called.
    Not suitable for production as TempDataProvider, because it uses up the main-memory and
    can not be used in a clustered system.
    As GlobalDataProvider you can use it in production.
    """

    def __init__(self, config):
        self.blobs = {}

    def get(self, request, key, default = None):
        return self.blobs.get(key, default)

    def set(self, request, key, value):
        self.blobs[key] = value


# the request-methods:

def get_epfl_temp_blob_meta(request, key):
    """ Store/Retrieve the meta-data of the below possibliy very large binary object temporarily but avaiable on all nodes. """
    provider = request.registry.queryUtility(ITempDataProvider)
    if not provider:
        raise ValueError, "No ITempDataProvider configured!"
    meta_key = "__meta__$" + key
    return json.loads(provider.get(request, meta_key))

def get_epfl_temp_blob(request, key):
    """ Store/Retrieve a possibliy very large binary object temporarily but avaiable on all nodes. """
    provider = request.registry.queryUtility(ITempDataProvider)
    if not provider:
        raise ValueError, "No ITempDataProvider configured!"
    return provider.get(request, key)

def set_epfl_temp_blob(request, key, data, meta = None, ttl = None):
    """ 
    Store/Retrieve a possibliy very large binary object temporarily but avaiable on all nodes. 
    meta-data (a json-dumpable) can be supplied and a ttl (in seconds)
    """
    if ttl is None:
        ttl = epflconfig.get(request, "epfl.tmp_data_ttl")        

    provider = request.registry.queryUtility(ITempDataProvider)
    if not provider:
        raise ValueError, "No ITempDataProvider configured!"

    if meta:
        provider.set(request, "__meta__$" + key, json.dumps(meta))

    provider.set(request, "__ttl__$" + key, json.dumps(ttl))
    provider.set(request, key, data)

def get_epfl_nodeglobal_aux(request, key, default = None):
    provider = request.registry.queryUtility(INodeGlobalDataProvider)
    if not provider:
        raise ValueError, "No IGlobalDataProvider configured!"
    return provider.get(request, key, default)

def set_epfl_nodeglobal_aux(request, key, value):
    provider = request.registry.queryUtility(INodeGlobalDataProvider)
    if not provider:
        raise ValueError, "No IGlobalDataProvider configured!"
    provider.set(request, key, value)

