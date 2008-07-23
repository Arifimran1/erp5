##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
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

from ZODB.POSException import ConflictError
from Products.CMFCore.CatalogTool import CatalogTool as CMFCoreCatalogTool
from Products.ZSQLCatalog.ZSQLCatalog import ZCatalog
from Products.ZSQLCatalog.SQLCatalog import Query, ComplexQuery
from Products.ERP5Type import Permissions
from Products.ERP5Type.Cache import CachingMethod
from AccessControl import ClassSecurityInfo, getSecurityManager
from Products.CMFCore.CatalogTool import IndexableObjectWrapper as CMFCoreIndexableObjectWrapper
from Products.CMFCore.utils import UniqueObject, _checkPermission, _getAuthenticatedUser, getToolByName
from Products.CMFCore.utils import _mergedLocalRoles
from Globals import InitializeClass, DTMLFile, package_home
from Acquisition import aq_base, aq_inner, aq_parent, ImplicitAcquisitionWrapper
from DateTime.DateTime import DateTime
from Products.CMFActivity.ActiveObject import ActiveObject
from Products.ERP5Type.TransactionalVariable import getTransactionalVariable

from AccessControl.PermissionRole import rolesForPermissionOn

from Products.PageTemplates.Expressions import SecureModuleImporter
from Products.CMFCore.Expression import Expression
from Products.PageTemplates.Expressions import getEngine
from MethodObject import Method

from Products.ERP5Security.ERP5UserManager import SUPER_USER

import os, time, urllib, warnings
import sys
from zLOG import LOG, PROBLEM, WARNING, INFO
import sets

SECURITY_USING_NUX_USER_GROUPS, SECURITY_USING_PAS = range(2)
ACQUIRE_PERMISSION_VALUE = []

try:
  from Products.PluggableAuthService import PluggableAuthService
  PAS_meta_type = PluggableAuthService.PluggableAuthService.meta_type
except ImportError:
  PAS_meta_type = ''
try:
  from Products.ERP5Security import mergedLocalRoles as PAS_mergedLocalRoles
except ImportError:
  pass

try:
  from Products.NuxUserGroups import UserFolderWithGroups
  NUG_meta_type = UserFolderWithGroups.meta_type
except ImportError:
  NUG_meta_type = ''
try:
  from Products.NuxUserGroups.CatalogToolWithGroups import mergedLocalRoles
  from Products.NuxUserGroups.CatalogToolWithGroups import _getAllowedRolesAndUsers
except ImportError:
  pass

from Persistence import Persistent
from Acquisition import Implicit

def getSecurityProduct(acl_users):
  """returns the security used by the user folder passed.
  (NuxUserGroup, ERP5Security, or None if anything else).
  """
  if acl_users.meta_type == PAS_meta_type:
    return SECURITY_USING_PAS
  elif acl_users.meta_type == NUG_meta_type:
    return SECURITY_USING_NUX_USER_GROUPS


class IndexableObjectWrapper(CMFCoreIndexableObjectWrapper):

    def __setattr__(self, name, value):
      # We need to update the uid during the cataloging process
      if name == 'uid':
        setattr(self.__ob, name, value)
      else:
        self.__dict__[name] = value

    def allowedRolesAndUsers(self):
        """
        Return a list of roles and users with View permission.
        Used by Portal Catalog to filter out items you're not allowed to see.

        WARNING (XXX): some user base local role association is currently
        being stored (ex. to be determined). This should be prevented or it will
        make the table explode. To analyse the symptoms, look at the
        user_and_roles table. You will find some user:foo values
        which are not necessary.
        """
        ob = self.__ob
        security_product = getSecurityProduct(ob.acl_users)
        withnuxgroups = security_product == SECURITY_USING_NUX_USER_GROUPS
        withpas = security_product == SECURITY_USING_PAS

        if withnuxgroups:
          localroles = mergedLocalRoles(ob, withgroups=1)
        elif withpas:
          localroles = PAS_mergedLocalRoles(ob)
        else:
          # CMF
          localroles = _mergedLocalRoles(ob)
        # For each group or user, we have a list of roles, this list
        # give in this order : [roles on object, roles acquired on the parent,
        # roles acquired on the parent of the parent....]
        # So if we have ['-Author','Author'] we should remove the role 'Author'
        # but if we have ['Author','-Author'] we have to keep the role 'Author'
        flat_localroles = {}
        skip_role_set = sets.Set()
        skip_role = skip_role_set.add
        clear_skip_role = skip_role_set.clear
        for key, role_list in localroles.iteritems():
          new_role_list = []
          new_role = new_role_list.append
          clear_skip_role()
          for role in role_list:
            if role[:1] == '-':
              skip_role(role[1:])
            elif role not in skip_role_set:
              new_role(role)
          if len(new_role_list)>0:
            flat_localroles[key] = new_role_list
        localroles = flat_localroles
        # For each local role of a user:
        #   If the local role grants View permission, add it.
        # Every addition implies 2 lines:
        #   user:<user_id>
        #   user:<user_id>:<role_id>
        # A line must not be present twice in final result.
        allowed = sets.Set(rolesForPermissionOn('View', ob))
        allowed.discard('Owner')
        add = allowed.add
        for user, roles in localroles.iteritems():
          if withnuxgroups:
            prefix = user
          else:
            prefix = 'user:' + user
          for role in roles:
            if role in allowed:
              add(prefix)
              add(prefix + ':' + role)
        return list(allowed)


class RelatedBaseCategory(Method):
    """A Dynamic Method to act as a related key.
    """
    def __init__(self, id,strict_membership=0):
      self._id = id
      self.strict_membership=strict_membership

    def __call__(self, instance, table_0, table_1, query_table='catalog', **kw):
      """Create the sql code for this related key."""
      base_category_uid = instance.portal_categories._getOb(self._id).getUid()
      expression_list = []
      append = expression_list.append
      append('%s.uid = %s.category_uid' % (table_1,table_0))
      if self.strict_membership:
        append('AND %s.category_strict_membership = 1' % table_0)
      append('AND %s.base_category_uid = %s' % (table_0,base_category_uid))
      append('AND %s.uid = %s.uid' % (table_0,query_table))
      return ' '.join(expression_list)

class CatalogTool (UniqueObject, ZCatalog, CMFCoreCatalogTool, ActiveObject):
    """
    This is a ZSQLCatalog that filters catalog queries.
    It is based on ZSQLCatalog
    """
    id = 'portal_catalog'
    meta_type = 'ERP5 Catalog'
    security = ClassSecurityInfo()

    default_result_limit = 1000
    default_count_limit = 1
    
    manage_options = ({ 'label' : 'Overview', 'action' : 'manage_overview' },
                     ) + ZCatalog.manage_options

    def __init__(self):
        ZCatalog.__init__(self, self.getId())

    # Explicit Inheritance
    __url = CMFCoreCatalogTool.__url
    manage_catalogFind = CMFCoreCatalogTool.manage_catalogFind

    security.declareProtected(Permissions.ManagePortal
                , 'manage_schema')
    manage_schema = DTMLFile('dtml/manageSchema', globals())

    def getPreferredSQLCatalogId(self, id=None):
      """
      Get the SQL Catalog from preference.
      """
      if id is None:
        # Check if we want to use an archive
        #if getattr(aq_base(self.portal_preferences), 'uid', None) is not None:
        archive_path = self.portal_preferences.getPreferredArchive(sql_catalog_id=self.default_sql_catalog_id)
        if archive_path not in ('', None):
          try:
            archive = self.restrictedTraverse(archive_path)
          except KeyError:
            # Do not fail if archive object has been removed,
            # but preference is not up to date
            return None
          if archive is not None:
            catalog_id = archive.getCatalogId()
            if catalog_id not in ('', None):
              return catalog_id
        return None
      else:
        return id
      
    security.declareProtected('Import/Export objects', 'addDefaultSQLMethods')
    def addDefaultSQLMethods(self, config_id='erp5'):
      """
        Add default SQL methods for a given configuration.
      """
      # For compatibility.
      if config_id.lower() == 'erp5':
        config_id = 'erp5_mysql'
      elif config_id.lower() == 'cps3':
        config_id = 'cps3_mysql'

      addSQLCatalog = self.manage_addProduct['ZSQLCatalog'].manage_addSQLCatalog
      if config_id not in self.objectIds():
        addSQLCatalog(config_id, '')

      catalog = self.getSQLCatalog(config_id)
      addSQLMethod = catalog.manage_addProduct['ZSQLMethods'].manage_addZSQLMethod
      product_path = package_home(globals())
      zsql_dirs = []

      # Common methods - for backward compatibility
      # SQL code distribution is supposed to be business template based nowadays
      if config_id.lower() == 'erp5_mysql':
        zsql_dirs.append(os.path.join(product_path, 'sql', 'common_mysql'))
        zsql_dirs.append(os.path.join(product_path, 'sql', 'erp5_mysql'))
      elif config_id.lower() == 'cps3_mysql':
        zsql_dirs.append(os.path.join(product_path, 'sql', 'common_mysql'))
        zsql_dirs.append(os.path.join(product_path, 'sql', 'cps3_mysql'))

      # Iterate over the sql directory. Add all sql methods in that directory.
      for directory in zsql_dirs:
        for entry in os.listdir(directory):
          if entry.endswith('.zsql'):
            id = entry[:-5]
            # Create an empty SQL method first.
            addSQLMethod(id = id, title = '', connection_id = '', arguments = '', template = '')
            #LOG('addDefaultSQLMethods', 0, 'catalog = %r' % (catalog.objectIds(),))
            sql_method = getattr(catalog, id)
            # Set parameters of the SQL method from the contents of a .zsql file.
            sql_method.fromFile(os.path.join(directory, entry))
          elif entry == 'properties.xml':
            # This sets up the attributes. The file should be generated by manage_exportProperties.
            catalog.manage_importProperties(os.path.join(directory, entry))

      # Make this the default.
      self.default_sql_catalog_id = config_id
     
    security.declareProtected('Import/Export objects', 'exportSQLMethods')
    def exportSQLMethods(self, sql_catalog_id=None, config_id='erp5'):
      """
        Export SQL methods for a given configuration.
      """
      # For compatibility.
      if config_id.lower() == 'erp5':
        config_id = 'erp5_mysql'
      elif config_id.lower() == 'cps3':
        config_id = 'cps3_mysql'

      catalog = self.getSQLCatalog(sql_catalog_id)
      product_path = package_home(globals())
      common_sql_dir = os.path.join(product_path, 'sql', 'common_mysql')
      config_sql_dir = os.path.join(product_path, 'sql', config_id)
      common_sql_list = ('z0_drop_record', 'z_read_recorded_object_list', 'z_catalog_paths',
                         'z_record_catalog_object', 'z_clear_reserved', 'z_record_uncatalog_object',
                         'z_create_record', 'z_related_security', 'z_delete_recorded_object_list',
                         'z_reserve_uid', 'z_getitem_by_path', 'z_show_columns', 'z_getitem_by_path',
                         'z_show_tables', 'z_getitem_by_uid', 'z_unique_values', 'z_produce_reserved_uid_list',)
    
      msg = ''
      for id in catalog.objectIds(spec=('Z SQL Method',)):
        if id in common_sql_list:
          d = common_sql_dir
        else:
          d = config_sql_dir
        sql = catalog._getOb(id)
        # First convert the skin to text
        text = sql.manage_FTPget()
        name = os.path.join(d, '%s.zsql' % (id,))
        msg += 'Writing %s\n' % (name,)
        f = open(name, 'w')
        try:
          f.write(text)
        finally:
          f.close()
          
      properties = self.manage_catalogExportProperties(sql_catalog_id=sql_catalog_id)
      name = os.path.join(config_sql_dir, 'properties.xml')
      msg += 'Writing %s\n' % (name,)
      f = open(name, 'w')
      try:
        f.write(properties)
      finally:
        f.close()
        
      return msg
        
    def _listAllowedRolesAndUsers(self, user):
      security_product = getSecurityProduct(self.acl_users)
      if security_product == SECURITY_USING_PAS:
        # We use ERP5Security PAS based authentication
        try:
          # check for proxy role in stack
          eo = getSecurityManager()._context.stack[-1]
          proxy_roles = getattr(eo, '_proxy_roles',None)
        except IndexError:
          proxy_roles = None
        if proxy_roles:
          # apply proxy roles
          user = eo.getOwner()
          result = list(proxy_roles)
        else:
          result = list(user.getRoles())
        result.append('Anonymous')
        result.append('user:%s' % user.getId())
        # deal with groups
        getGroups = getattr(user, 'getGroups', None)
        if getGroups is not None:
            groups = list(user.getGroups())
            groups.append('role:Anonymous')
            if 'Authenticated' in result:
                groups.append('role:Authenticated')
            for group in groups:
                result.append('user:%s' % group)
        # end groups
        return result
      elif security_product == SECURITY_USING_NUX_USER_GROUPS:
        return _getAllowedRolesAndUsers(user)
      else:
        return CMFCoreCatalogTool._listAllowedRolesAndUsers(self, user)

    # Schema Management
    def editColumn(self, column_id, sql_definition, method_id, default_value, REQUEST=None, RESPONSE=None):
      """
        Modifies a schema column of the catalog
      """
      new_schema = []
      for c in self.getIndexList():
        if c.id == index_id:
          new_c = {'id': index_id, 'sql_definition': sql_definition, 'method_id': method_id, 'default_value': default_value}
        else:
          new_c = c
        new_schema.append(new_c)
      self.setColumnList(new_schema)

    def setColumnList(self, column_list):
      """
      """
      self._sql_schema = column_list

    def getColumnList(self):
      """
      """
      if not hasattr(self, '_sql_schema'): self._sql_schema = []
      return self._sql_schema

    def getColumn(self, column_id):
      """
      """
      for c in self.getColumnList():
        if c.id == column_id:
          return c
      return None

    def editIndex(self, index_id, sql_definition, REQUEST=None, RESPONSE=None):
      """
        Modifies the schema of the catalog
      """
      new_index = []
      for c in self.getIndexList():
        if c.id == index_id:
          new_c = {'id': index_id, 'sql_definition': sql_definition}
        else:
          new_c = c
        new_index.append(new_c)
      self.setIndexList(new_index)

    def setIndexList(self, index_list):
      """
      """
      self._sql_index = index_list

    def getIndexList(self):
      """
      """
      if not hasattr(self, '_sql_index'): self._sql_index = []
      return self._sql_index

    def getIndex(self, index_id):
      """
      """
      for c in self.getIndexList():
        if c.id == index_id:
          return c
      return None


    security.declarePublic('getAllowedRolesAndUsers')
    def getAllowedRolesAndUsers(self, sql_catalog_id=None, **kw):
      """
        Return allowed roles and users.

        This is supposed to be used with Z SQL Methods to check permissions
        when you list up documents. It is also able to take into account
        a parameter named local_roles so that listed documents only include
        those documents for which the user (or the group) was
        associated one of the given local roles.
      
        The use of getAllowedRolesAndUsers is deprecated, you should use
        getSecurityQuery instead
      """
      user = _getAuthenticatedUser(self)
      user_str = str(user)
      user_is_superuser = (user_str == SUPER_USER)
      allowedRolesAndUsers = self._listAllowedRolesAndUsers(user)
      role_column_dict = {}
      local_role_column_dict = {}
      catalog = self.getSQLCatalog(sql_catalog_id)
      column_map = catalog.getColumnMap()

      # Patch for ERP5 by JP Smets in order
      # to implement worklists and search of local roles
      if kw.has_key('local_roles'):
        local_roles = kw['local_roles']
        local_role_dict = dict(catalog.getSQLCatalogLocalRoleKeysList())
        role_dict = dict(catalog.getSQLCatalogRoleKeysList())
        # XXX user is not enough - we should also include groups of the user
        # Only consider local_roles if it is not empty
        if local_roles not in (None, '', []): # XXX: Maybe "if local_roles:" is enough.
          new_allowedRolesAndUsers = []
          # Turn it into a list if necessary according to ';' separator
          if isinstance(local_roles, str):
            local_roles = local_roles.split(';')
          # Local roles now has precedence (since it comes from a WorkList)
          for user_or_group in allowedRolesAndUsers:
            for role in local_roles:
              # Performance optimisation
              if local_role_dict.has_key(role):
                # XXX This should be a list
                # If a given role exists as a column in the catalog,
                # then it is considered as single valued and indexed
                # through the catalog.
                if not user_is_superuser:
                  # XXX This should be a list
                  # which also includes all user groups
                  column_id = local_role_dict[role]
                  local_role_column_dict[column_id] = user_str
              if role_dict.has_key(role):
                # XXX This should be a list
                # If a given role exists as a column in the catalog,
                # then it is considered as single valued and indexed
                # through the catalog.
                if not user_is_superuser:
                  # XXX This should be a list
                  # which also includes all user groups
                  column_id = role_dict[role]
                  role_column_dict[column_id] = user_str
              else:
                # Else, we use the standard approach
                new_allowedRolesAndUsers.append('%s:%s' % (user_or_group, role))
          if local_role_column_dict == {}:
            allowedRolesAndUsers = new_allowedRolesAndUsers

      else:
        # We only consider here the Owner role (since it was not indexed)
        # since some objects may only be visible by their owner
        # which was not indexed
        for role, column_id in catalog.getSQLCatalogRoleKeysList():
          # XXX This should be a list
          if not user_is_superuser:
            try:
              # if called by an executable with proxy roles, we don't use
              # owner, but only roles from the proxy.
              eo = getSecurityManager()._context.stack[-1]
              proxy_roles = getattr(eo, '_proxy_roles', None)
              if not proxy_roles:
                role_column_dict[column_id] = user_str
            except IndexError:
              role_column_dict[column_id] = user_str

      return allowedRolesAndUsers, role_column_dict, local_role_column_dict

    def getSecurityUidListAndRoleColumnDict(self, sql_catalog_id=None, **kw):
      """
        Return a list of security Uids and a dictionnary containing available
        role columns.

        XXX: This method always uses default catalog. This should not break a
        site as long as security uids are considered consistent among all
        catalogs.
      """
      allowedRolesAndUsers, role_column_dict, local_role_column_dict = \
          self.getAllowedRolesAndUsers(**kw)
      catalog = self.getSQLCatalog(sql_catalog_id)
      method = getattr(catalog, catalog.sql_search_security, None)
      if allowedRolesAndUsers:
        allowedRolesAndUsers.sort()
        cache_key = tuple(allowedRolesAndUsers)
        tv = getTransactionalVariable(self)
        try:
          security_uid_cache = tv['getSecurityUidListAndRoleColumnDict']
        except KeyError:
          security_uid_cache = tv['getSecurityUidListAndRoleColumnDict'] = {}
        try:
          security_uid_list = security_uid_cache[cache_key]
        except KeyError:
          if method is None:
            warnings.warn("The usage of allowedRolesAndUsers is "\
                          "deprecated. Please update your catalog "\
                          "business template.", DeprecationWarning)
            security_uid_list = [x.security_uid for x in \
              self.unrestrictedSearchResults(
                allowedRolesAndUsers=allowedRolesAndUsers,
                select_expression="security_uid",
                group_by_expression="security_uid")]
          else:
            # XXX: What with this string transformation ?! Souldn't it be done in
            # dtml instead ?
            allowedRolesAndUsers = ["'%s'" % (role, ) for role in allowedRolesAndUsers]
            security_uid_list = [x.uid for x in method(security_roles_list = allowedRolesAndUsers)]
          security_uid_cache[cache_key] = security_uid_list
      else:
        security_uid_list = []
      return security_uid_list, role_column_dict, local_role_column_dict

    security.declarePublic('getSecurityQuery')
    def getSecurityQuery(self, query=None, sql_catalog_id=None, **kw):
      """
        Build a query based on allowed roles or on a list of security_uid
        values. The query takes into account the fact that some roles are
        catalogued with columns.
      """
      original_query = query
      security_uid_list, role_column_dict, local_role_column_dict = \
          self.getSecurityUidListAndRoleColumnDict(
              sql_catalog_id=sql_catalog_id, **kw)
      if role_column_dict:
        query_list = []
        for key, value in role_column_dict.items():
          new_query = Query(**{key : value})
          query_list.append(new_query)
        operator_kw = {'operator': 'AND'}
        query = ComplexQuery(*query_list, **operator_kw)
        # If security_uid_list is empty, adding it to criterions will only
        # result in "false or [...]", so avoid useless overhead by not
        # adding it at all.
        if security_uid_list:
          query = ComplexQuery(Query(security_uid=security_uid_list, operator='IN'),
                               query, operator='OR')
      else:
        query = Query(security_uid=security_uid_list, operator='IN')

      if local_role_column_dict:
        query_list = []
        for key, value in local_role_column_dict.items():
          new_query = Query(**{key : value})
          query_list.append(new_query)
        operator_kw = {'operator': 'AND'}
        local_role_query = ComplexQuery(*query_list, **operator_kw)
        query = ComplexQuery(query, local_role_query, operator='AND')

      if original_query is not None:
        query = ComplexQuery(query, original_query, operator='AND')
      return query

    # searchResults has inherited security assertions.
    def searchResults(self, query=None, **kw):
        """
        Calls ZCatalog.searchResults with extra arguments that
        limit the results to what the user is allowed to see.
        """
        if not _checkPermission(
            Permissions.AccessInactivePortalContent, self):
            now = DateTime()
            kw[ 'effective' ] = { 'query' : now, 'range' : 'max' }
            kw[ 'expires'   ] = { 'query' : now, 'range' : 'min' }

        catalog_id = self.getPreferredSQLCatalogId(kw.pop("sql_catalog_id", None))
        query = self.getSecurityQuery(query=query, sql_catalog_id=catalog_id, **kw)
        kw.setdefault('limit', self.default_result_limit)
        # get catalog from preference
        #LOG("searchResult", INFO, catalog_id)
        #         LOG("searchResult", INFO, ZCatalog.searchResults(self, query=query, sql_catalog_id=catalog_id, src__=1, **kw))
        return ZCatalog.searchResults(self, query=query, sql_catalog_id=catalog_id, **kw)

    __call__ = searchResults

    security.declarePrivate('beforeCatalogClear')
    def beforeCatalogClear(self):
      """
      Clears the catalog by calling a list of methods
      """
      id_tool = self.getPortalObject().portal_ids
      try:
        # Call generate new id in order to store the last id into
        # the zodb
        id_tool.generateNewLengthId(id_group='portal_activity')
        id_tool.generateNewLengthId(id_group='portal_activity_queue')
      except ConflictError:
        raise
      except:
        # Swallow exceptions to allow catalog clear to happen.
        # For example, is portal_ids table does not exist and exception will
        # be thrown by portal_id methods.
        LOG('ERP5Catalog.beforeCatalogClear', WARNING,
            'beforeCatalogClear failed', error=sys.exc_info())

    security.declarePrivate('unrestrictedSearchResults')
    def unrestrictedSearchResults(self, REQUEST=None, **kw):
        """Calls ZSQLCatalog.searchResults directly without restrictions.
        """
        kw.setdefault('limit', self.default_result_limit)
        return ZCatalog.searchResults(self, REQUEST, **kw)

    # We use a string for permissions here due to circular reference in import
    # from ERP5Type.Permissions
    security.declareProtected('Search ZCatalog', 'getResultValue')
    def getResultValue(self, query=None, **kw):
        """
        A method to factor common code used to search a single
        object in the database.
        """
        result = self.searchResults(query=query, **kw)
        try:
          return result[0].getObject()
        except IndexError:
          return None

    security.declarePrivate('unrestrictedGetResultValue')
    def unrestrictedGetResultValue(self, query=None, **kw):
        """
        A method to factor common code used to search a single
        object in the database. Same as getResultValue but without
        taking into account security.
        """
        result = self.unrestrictedSearchResults(query=query, **kw)
        try:
          return result[0].getObject()
        except IndexError:
          return None

    def countResults(self, query=None, **kw):
        """
            Calls ZCatalog.countResults with extra arguments that
            limit the results to what the user is allowed to see.
        """
        # XXX This needs to be set again
        #if not _checkPermission(
        #    Permissions.AccessInactivePortalContent, self):
        #    base = aq_base(self)
        #    now = DateTime()
        #    #kw[ 'effective' ] = { 'query' : now, 'range' : 'max' }
        #    #kw[ 'expires'   ] = { 'query' : now, 'range' : 'min' }
        catalog_id = self.getPreferredSQLCatalogId(kw.pop("sql_catalog_id", None))        
        query = self.getSecurityQuery(query=query, sql_catalog_id=catalog_id, **kw)
        kw.setdefault('limit', self.default_count_limit)
        # get catalog from preference
        return ZCatalog.countResults(self, query=query, sql_catalog_id=catalog_id, **kw)
    
    security.declarePrivate('unrestrictedCountResults')
    def unrestrictedCountResults(self, REQUEST=None, **kw):
        """Calls ZSQLCatalog.countResults directly without restrictions.
        """
        return ZCatalog.countResults(self, REQUEST, **kw)

    def wrapObject(self, object, sql_catalog_id=None, **kw):
        """
          Return a wrapped object for reindexing.
        """
        catalog = self.getSQLCatalog(sql_catalog_id)
        if catalog is None:
          # Nothing to do.
          LOG('wrapObject', 0, 'Warning: catalog is not available')
          return (None, None)

        wf = getToolByName(self, 'portal_workflow')
        if wf is not None:
          vars = wf.getCatalogVariablesFor(object)
        else:
          vars = {}
        #LOG('catalog_object vars', 0, str(vars))

        # Find the parent definition for security
        document_object = aq_inner(object)
        is_acquired = 0
        w = IndexableObjectWrapper(vars, document_object)
        while getattr(document_object, 'isRADContent', 0):
          # This condition tells which object should acquire 
          # from their parent.
          # XXX Hardcode _View_Permission for a performance point of view
          if getattr(aq_base(document_object), '_View_Permission', ACQUIRE_PERMISSION_VALUE) == ACQUIRE_PERMISSION_VALUE\
             and document_object._getAcquireLocalRoles():
            document_object = document_object.aq_parent
            is_acquired = 1
          else:
            break
        if is_acquired:
          document_w = IndexableObjectWrapper({}, document_object)
        else:
          document_w = w

        (security_uid, optimised_roles_and_users) = catalog.getSecurityUid(document_w)
        #LOG('catalog_object optimised_roles_and_users', 0, str(optimised_roles_and_users))
        # XXX we should build vars begore building the wrapper
        if optimised_roles_and_users is not None:
          vars['optimised_roles_and_users'] = optimised_roles_and_users
        else:
          vars['optimised_roles_and_users'] = None
        predicate_property_dict = catalog.getPredicatePropertyDict(object)
        if predicate_property_dict is not None:
          vars['predicate_property_dict'] = predicate_property_dict
        vars['security_uid'] = security_uid

        return ImplicitAcquisitionWrapper(w, aq_parent(document_object))

    security.declarePrivate('reindexObject')
    def reindexObject(self, object, idxs=None, sql_catalog_id=None,**kw):
        '''Update catalog after object data has changed.
        The optional idxs argument is a list of specific indexes
        to update (all of them by default).
        '''
        if idxs is None: idxs = []
        url = self.__url(object)
        self.catalog_object(object, url, idxs=idxs, sql_catalog_id=sql_catalog_id,**kw)


    security.declarePrivate('unindexObject')
    def unindexObject(self, object=None, path=None, uid=None,sql_catalog_id=None):
        """
          Remove from catalog.
        """
        if path is None and uid is None:
          if object is None:
            raise TypeError, 'One of uid, path and object parameters must not be None'
          path = self.__url(object)
        if uid is None:
          raise TypeError, "unindexObject supports only uid now"
        self.uncatalog_object(path=path, uid=uid, sql_catalog_id=sql_catalog_id)

    security.declarePrivate('beforeUnindexObject')
    def beforeUnindexObject(self, object, path=None, uid=None,sql_catalog_id=None):
        """
          Remove from catalog.
        """
        if path is None and uid is None:
          path = self.__url(object)
        self.beforeUncatalogObject(path=path,uid=uid, sql_catalog_id=sql_catalog_id)

    security.declarePrivate('getUrl')
    def getUrl(self, object):
      return self.__url(object)

    security.declarePrivate('moveObject')
    def moveObject(self, object, idxs=None):
        """
          Reindex in catalog, taking into account
          peculiarities of ERP5Catalog / ZSQLCatalog

          Useless ??? XXX
        """
        if idxs is None: idxs = []
        url = self.__url(object)
        self.catalog_object(object, url, idxs=idxs, is_object_moved=1)

    security.declarePublic('getPredicatePropertyDict')
    def getPredicatePropertyDict(self, object):
      """
      Construct a dictionnary with a list of properties
      to catalog into the table predicate
      """
      if not getattr(object,'isPredicate',None):
        return None
      object = object.asPredicate()
      if object is None:
        return None
      property_dict = {}
      identity_criterion = getattr(object,'_identity_criterion',None)
      range_criterion = getattr(object,'_range_criterion',None)
      if identity_criterion is not None:
        for property, value in identity_criterion.items():
          if value is not None:
            property_dict[property] = value
      if range_criterion is not None:
        for property, (min, max) in range_criterion.items():
          if min is not None:
            property_dict['%s_range_min' % property] = min
          if max is not None:
            property_dict['%s_range_max' % property] = max
      property_dict['membership_criterion_category_list'] = object.getMembershipCriterionCategoryList()
      return property_dict

    security.declarePrivate('getDynamicRelatedKeyList')
    def getDynamicRelatedKeyList(self, key_list, sql_catalog_id=None):
      """
      Return the list of dynamic related keys.
      This method will try to automatically generate new related key
      by looking at the category tree.

      For exemple it will generate:
      destination_title | category,catalog/title/z_related_destination
      default_destination_title | category,catalog/title/z_related_destination
      strict_destination_title | category,catalog/title/z_related_strict_destination

      strict_ related keys only returns documents which are strictly member of
      the category.
      """
      related_key_list = []
      base_cat_id_list = self.portal_categories.getBaseCategoryDict()
      default_string = 'default_'
      strict_string = 'strict_'
      for key in key_list:
        prefix = ''
        strict = 0
        if key.startswith(default_string):
          key = key[len(default_string):]
          prefix = default_string
        if key.startswith(strict_string):
          strict = 1
          key = key[len(strict_string):]
          prefix = prefix + strict_string
        splitted_key = key.split('_')
        # look from the end of the key from the beginning if we
        # can find 'title', or 'portal_type'...
        for i in range(1,len(splitted_key))[::-1]:
          expected_base_cat_id = '_'.join(splitted_key[0:i])
          if expected_base_cat_id != 'parent' and \
             expected_base_cat_id in base_cat_id_list:
            # We have found a base_category
            end_key = '_'.join(splitted_key[i:])
            # accept only some catalog columns
            if end_key in ('title', 'uid', 'description',
                           'relative_url', 'id', 'portal_type'):
              if strict:
                related_key_list.append(
                      '%s%s | category,catalog/%s/z_related_strict_%s' %
                      (prefix, key, end_key, expected_base_cat_id))
              else:
                related_key_list.append(
                      '%s%s | category,catalog/%s/z_related_%s' %
                      (prefix, key, end_key, expected_base_cat_id))

      return related_key_list

    def _aq_dynamic(self, name):
      """
      Automatic related key generation.
      Will generate z_related_[base_category_id] if possible
      """
      aq_base_name = getattr(aq_base(self), name, None)
      if aq_base_name == None:
        DYNAMIC_METHOD_NAME = 'z_related_'
        STRICT_DYNAMIC_METHOD_NAME = 'z_related_strict_'
        method_name_length = len(DYNAMIC_METHOD_NAME)
        zope_security = '__roles__'
        if (name.startswith(DYNAMIC_METHOD_NAME) and \
          (not name.endswith(zope_security))):
          if name.startswith(STRICT_DYNAMIC_METHOD_NAME):
            base_category_id = name[len(STRICT_DYNAMIC_METHOD_NAME):]
            method = RelatedBaseCategory(base_category_id, strict_membership=1)
          else:
            base_category_id = name[len(DYNAMIC_METHOD_NAME):]
            method = RelatedBaseCategory(base_category_id)
          setattr(self.__class__, name, method)
          klass = aq_base(self).__class__
          if hasattr(klass, 'security'):
            from Products.ERP5Type import Permissions as ERP5Permissions
            klass.security.declareProtected(ERP5Permissions.View, name)
          else:
            LOG('ERP5Catalog', PROBLEM,
                'Security not defined on %s' % klass.__name__)
          return getattr(self, name)
        else:
          return aq_base_name
      return aq_base_name

InitializeClass(CatalogTool)
