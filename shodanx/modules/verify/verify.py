import importlib.metadata as data


def verify(pkg): #After version verified call the updatelog for updates information
    
    version = data.version(pkg)
    
    return version
