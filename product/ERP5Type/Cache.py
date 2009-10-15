# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2004 Nexedi SARL and Contributors. All Rights Reserved.
#                    Yoshinori Okuji <yo@nexedi.com>
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import string
from time import time
from AccessControl.SecurityInfo import allow_class
from CachePlugins.BaseCache import CachedMethodError
from zLOG import LOG, WARNING
from Products.ERP5Type.TransactionalVariable import getTransactionalVariable
from warnings import warn

DEFAULT_CACHE_SCOPE = 'GLOBAL'
DEFAULT_CACHE_FACTORY = 'erp5_ui_short'
is_cache_initialized = 0
is_cache_ready = 0

def initializePortalCachingProperties(self):
  """ Init CachingMethod properties."""
  ## check if global CachingMethod is initialized in RAM for this ERP5 site. If not init it
  global is_cache_initialized
  global is_cache_ready
  if not is_cache_initialized:
    # we set is_cache_initialized right now to prevent infinite loops
    is_cache_initialized = 1
    ## update cache structure from portal_caches
    self.getPortalObject().portal_caches.updateCache()
    # we mark the cache as ready after initialization, because initialization
    # itself will cause cache misses that we want to ignore
    is_cache_ready = 1

class CacheFactory:
  """ CacheFactory is a RAM based object which contains different cache plugin
  objects ordered in a list.
  """

  cache_plugins = []
  cache_duration = 180

  def __init__(self, cache_plugins, cache_params):
    self.cache_plugins = cache_plugins
    self.cache_duration = cache_params.get('cache_duration')

    ## separete local and shared cache plugins
    self.quick_cache = self.cache_plugins[0]
    self._quick_cache_get = self.quick_cache.get
    try:
      self.shared_caches = self.cache_plugins[1:]
    except IndexError:
      self.shared_caches = []

    ## set 'check_expire_cache_interval' to the minimal value between
    ## individual 'check_expire_cache_interval' for each cache plugin contained
    l = []
    for cp in self.cache_plugins:
      l.append(cp.cache_expire_check_interval)
    l = filter(lambda x: x is not None and x != 0, l)
    self.cache_expire_check_interval = min(l)
    self._next_cache_expire_check_at = time() + self.cache_expire_check_interval

  def __call__(self, callable_object, cache_id, scope, cache_duration=None, *args, **kwd):
    """ When CacheFactory is called it will try to return cached value using
    appropriate cache plugin.
    """
    ## Expired Cache (if needed)
    now = time()
    if now > self._next_cache_expire_check_at:
      self.expire(now)

    try:
      return self._quick_cache_get(cache_id, scope).getValue()
    except KeyError:
      ## not in local, check if it's in shared
      for shared_cache in self.shared_caches:
        try:
          cache_entry = shared_cache.get(cache_id, scope)
        except KeyError:
          pass
        else:
          value = cache_entry.getValue()
          ## update local cache
          self.quick_cache.set(cache_id, scope, value,
                              cache_duration,
                              cache_entry.calculation_time)
          return value

    cache_duration = self.cache_duration
    ## not in any available cache plugins calculate and set to local ..
    start = time()
    value = callable_object(*args, **kwd)
    end = time()
    calculation_time = end - start
    self.quick_cache.set(cache_id, scope, value, cache_duration, calculation_time)

    ## .. and update rest of caches in chain except already updated local one
    for shared_cache in self.shared_caches:
      shared_cache.set(cache_id, scope, value, cache_duration, calculation_time)
    return value

  def expire(self, now):
    """ Expire cache plugins """
    self._next_cache_expire_check_at = now + self.cache_expire_check_interval
    for cache_plugin in self.getCachePluginList():
      cache_plugin.expireOldCacheEntries()

  def getCachePluginList(self, omit_cache_plugin_name=None):
    """ get list of all cache plugins except specified by name in omit """
    rl = []
    for cp in self.cache_plugins:
      if omit_cache_plugin_name != cp.__class__.__name__:
        rl.append(cp)
    return rl

  def getCachePluginByClassName(self, cache_plugin_name):
    """ get cache plugin by its class name """
    for cp in self.cache_plugins:
      if cache_plugin_name == cp.__class__.__name__:
        return cp
    return None

  def clearCache(self):
    """ clear cache for this cache factory """
    for cp in self.cache_plugins:
      cp.clearCache()

class CachingMethod:
  """CachingMethod is a RAM based global Zope class which contains different
  CacheFactory objects for every available ERP5 site instance.
  """

  ## cache factories will be initialized for every ERP5 site
  factories = {}

  def __init__(self, callable_object, id, cache_duration=180,
               cache_factory=DEFAULT_CACHE_FACTORY):
    """Wrap a callable object in a caching method.

    callable_object must be callable.
    id is used to identify what call should be treated as the same call.
    cache_duration is an old argument kept for backwards compatibility.
    cache_duration is specified per cache factory.
    cache_factory is the id of the cache_factory to use.
    """
    if not callable(callable_object):
      raise CachedMethodError, "callable_object %s is not callable" % str(
                                                                callable_object)
    if not id:
      raise CachedMethodError, "id must be specified"
    self.id = id
    self.callable_object = callable_object
    self.cache_duration = cache_duration
    self.cache_factory = cache_factory

  def __call__(self, *args, **kwd):
    """Call the method or return cached value using appropriate cache plugin """

    ## cache scope is based on user which is a kwd argument
    scope = kwd.get('scope', DEFAULT_CACHE_SCOPE)

    ## generate unique cache id
    cache_id = self.generateCacheId(self.id, *args, **kwd)

    try:
      ## try to get value from cache in a try block
      ## which is faster than checking for keys
      # It is very important to take the factories dictionnary
      # on CachingMethod instead of self, we want a global variable
      cache_factory = CachingMethod.factories[self.cache_factory]
    except KeyError:
      global is_cache_ready
      if is_cache_ready:
        ## no caching enabled for this site or no such cache factory
        LOG("Cache.__call__", WARNING,
            "Factory %s not found, method %s executed without cache" % (
             self.cache_factory, self.callable_object))
      value = self.callable_object(*args, **kwd)
    else:
      value = cache_factory(
              self.callable_object, cache_id, scope, self.cache_duration,
              *args, **kwd)
    return value

  def delete(self, id, cache_factory=DEFAULT_CACHE_FACTORY, scope=DEFAULT_CACHE_SCOPE):
    """ Delete cache key. """
    cache_id = self.generateCacheId(id)
    cache_factory = CachingMethod.factories[cache_factory]
    for cp in cache_factory.getCachePluginList():
      cp.delete(cache_id, scope)

  def generateCacheId(self, method_id, *args, **kwd):
    """ Generate proper cache id based on *args and **kwd  """
    ## generate cache id out of arguments passed.
    ## depending on arguments we may have different
    ## cache_id for same method_id
    return str((method_id, args, kwd))

allow_class(CachingMethod)

# TransactionCache is a cache per transaction. The purpose of this cache is
# to accelerate some heavy read-only operations. Note that this must not be
# enabled when a transaction may modify ZODB objects.
def getReadOnlyTransactionCache(context):
  """Get the transaction cache.
  """
  tv = getTransactionalVariable(context)
  try:
    return tv['read_only_transaction_cache']
  except KeyError:
    return None

def enableReadOnlyTransactionCache(context):
  """Enable the transaction cache.
  """
  tv = getTransactionalVariable(context)
  tv['read_only_transaction_cache'] = {}

def disableReadOnlyTransactionCache(context):
  """Disable the transaction cache.
  """
  tv = getTransactionalVariable(context)
  try:
    del tv['read_only_transaction_cache']
  except KeyError:
    pass

########################################################
## Old global cache functions                         ##
## TODO: Check if it make sense to keep them any more ##
########################################################

def clearCache(cache_factory_list=(DEFAULT_CACHE_FACTORY,)):
  """Clear specified cache factory list."""
  warn("Global function clearCache() is deprecated. Use"
       " portal_caches.clearCache() instead.", DeprecationWarning,
       stacklevel=2)
  cache_storage = CachingMethod.factories
  for cf_key in cache_factory_list:
    if cache_storage.has_key(cf_key):
      for cp in cache_storage[cf_key].getCachePluginList():
        cp.clearCache()

