from types import ModuleType
import sys
import threading

class DynamicModule(ModuleType):
  """This module may generate new objects at runtime."""
  # it's useful to have such a generic utility
  # please subclass it if you need ERP5-specific behaviors

  __file__ = __file__

  def __init__(self, name, factory, doc=None):
    super(DynamicModule, self).__init__(name, doc=doc)
    self._factory = factory
    self._lock = threading.Lock()

  def __getattr__(self, name):
    if name[:2] == '__':
      raise AttributeError('%r module has no attribute %r'
                           % (self.__name__, name))
    with self._lock:
      try:
        return super(DynamicModule, self).__getattribute__(name)
      except AttributeError:
        obj = self._factory(name)
        # _factory can return an instance, a constant, or a class
        if isinstance(obj, type):
          # if it's a class we want to set __module__
          obj.__module__ = self.__name__
        elif isinstance(obj, ModuleType):
          # if it's a module we want to set the name according to the
          # module it's being added to
          obj.__name__ = "%s.%s" % (self.__name__, name)
        setattr(self, name, obj)
        return obj

def registerDynamicModule(name, factory):
  d = DynamicModule(name, factory)
  sys.modules[name] = d
  return d
