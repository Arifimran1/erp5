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

from Products.CMFCore.CatalogTool import CatalogTool as CMFCoreCatalogTool
from Products.ZSQLCatalog.ZSQLCatalog import ZCatalog
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo, getSecurityManager
from Products.CMFCore.CatalogTool import IndexableObjectWrapper as CMFCoreIndexableObjectWrapper
from Products.CMFCore.utils import UniqueObject, _checkPermission, _getAuthenticatedUser, getToolByName
from Products.CMFCore.utils import _mergedLocalRoles
from Globals import InitializeClass, DTMLFile, package_home
from Acquisition import aq_base, aq_inner, aq_parent
from DateTime.DateTime import DateTime
from Products.CMFActivity.ActiveObject import ActiveObject

from AccessControl.PermissionRole import rolesForPermissionOn

from Products.PageTemplates.Expressions import SecureModuleImporter
from Products.CMFCore.Expression import Expression
from Products.PageTemplates.Expressions import getEngine
from MethodObject import Method

import os, time, urllib
from zLOG import LOG

SECURITY_USING_NUX_USER_GROUPS, SECURITY_USING_PAS = range(2)
try:
  from Products.PluggableAuthService import PluggableAuthService
  PAS_meta_type = PluggableAuthService.PluggableAuthService.meta_type
except ImportError:
  PAS_meta_type = ''

try:
  from Products.NuxUserGroups import UserFolderWithGroups
  NUG_meta_type = UserFolderWithGroups.meta_type
except ImportError:
  NUG_meta_type = ''
    
def getSecurityProduct(acl_users):
  """returns the security used by the user folder passed.
  (NuxUserGroup, ERP5Security, or None if anything else).
  """
  if acl_users.meta_type == PAS_meta_type:
    return SECURITY_USING_PAS
  elif acl_users.meta_type == NUG_meta_type:
    return SECURITY_USING_NUX_USER_GROUPS

try:
  from Products.NuxUserGroups.CatalogToolWithGroups import mergedLocalRoles
  from Products.NuxUserGroups.CatalogToolWithGroups import _getAllowedRolesAndUsers
except ImportError:
  pass

class IndexableObjectWrapper(CMFCoreIndexableObjectWrapper):

    def __setattr__(self, name, value):
      # We need to update the uid during the cataloging process
      if name == 'uid':
        setattr(self.__ob, name, value)
      else:
        self.__dict__[name] = value

    def allowedRolesAndUsers(self):
        """
        Return a list of roles and users with Access contents
        information permission.
        Used by PortalCatalog to filter out items you're not allowed to see.
        """
        ob = self.__ob
        withnuxgroups = getSecurityProduct(ob.acl_users)\
                              == SECURITY_USING_NUX_USER_GROUPS
        allowed = {}
        for r in rolesForPermissionOn('Access contents information', ob):
          allowed[r] = 1
        if withnuxgroups:
          localroles = mergedLocalRoles(ob, withgroups=1)
        else:
          # CMF
          localroles = _mergedLocalRoles(ob)
        # For each group or user, we have a list of roles, this list
        # give in this order : [roles on object, roles acquired on the parent,
        # roles acquired on the parent of the parent....]
        # So if we have ['-Author','Author'] we should remove the role 'Author'
        # but if we have ['Author','-Author'] we have to keep the role 'Author'
        new_dict = {}
        for key in localroles.keys():
          new_list = []
          remove_list = []
          for role in localroles[key]:
            if role.startswith('-'):
              if not role[1:] in new_list and not role[1:] in remove_list:
                remove_list.append(role[1:])
            elif not role in remove_list:
              new_list.append(role)
          if len(new_list)>0:
            new_dict[key] = new_list
        localroles = new_dict
        for user, roles in localroles.items():
          for role in roles:
            if allowed.has_key(role):
              if withnuxgroups:
                allowed[user] = 1
              else:
                allowed['user:' + user] = 1
            # Added for ERP5 project by JP Smets
            if role != 'Owner':
              if withnuxgroups:
                allowed[user + ':' + role] = 1
              else:
                allowed['user:' + user + ':' + role] = 1
        if allowed.has_key('Owner'):
          del allowed['Owner']
        return list(allowed.keys())

class RelatedBaseCategory(Method):
    """A Dynamic Method to act as a related key.
    """
    def __init__(self, id):
      self._id = id

    def __call__(self, instance, table_0, table_1, query_table='catalog',**kw):
      """Create the sql code for this related key."""
      base_category_uid = instance.portal_categories._getOb(self._id).getUid()
      expression_list = []
      append = expression_list.append
      append('%s.uid = %s.category_uid' % (table_1,table_0))
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

    manage_options = ( { 'label' : 'Overview', 'action' : 'manage_overview' },
                     ) + ZCatalog.manage_options


    def __init__(self):
        ZCatalog.__init__(self, self.getId())

    # Explicite Inheritance
    __url = CMFCoreCatalogTool.__url
    manage_catalogFind = CMFCoreCatalogTool.manage_catalogFind

    security.declareProtected( CMFCorePermissions.ManagePortal
                , 'manage_schema' )
    manage_schema = DTMLFile( 'dtml/manageSchema', globals() )

    security.declareProtected( 'Import/Export objects', 'addDefaultSQLMethods' )
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

      # Common methods
      if config_id.lower() == 'erp5_mysql':
        zsql_dirs.append(os.path.join(product_path, 'sql', 'common_mysql'))
        zsql_dirs.append(os.path.join(product_path, 'sql', 'erp5_mysql'))
      elif config_id.lower() == 'cps3_mysql':
        zsql_dirs.append(os.path.join(product_path, 'sql', 'common_mysql'))
        zsql_dirs.append(os.path.join(product_path, 'sql', 'cps3_mysql'))
      # XXX TODO : add other cases

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
     
    security.declareProtected( 'Import/Export objects', 'exportSQLMethods' )
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
        result = list( user.getRoles() )
        result.append( 'Anonymous' )
        result.append( 'user:%s' % user.getId() )
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


    security.declarePublic( 'getAllowedRolesAndUsers' )
    def getAllowedRolesAndUsers(self, **kw):
      """
        Return allowed roles and users.

        This is supposed to be used with Z SQL Methods to check permissions
        when you list up documents. It is also able to take into account
        a parameter named local_roles so that list documents only include
        those documents for which the user (or the group) was
        associated one of the given local roles.
      """
      user = _getAuthenticatedUser(self)
      allowedRolesAndUsers = self._listAllowedRolesAndUsers(user)

      # Patch for ERP5 by JP Smets in order
      # to implement worklists and search of local roles
      if kw.has_key('local_roles'):
        # XXX user is not enough - we should also include groups of the user
        # Only consider local_roles if it is not empty
        if kw['local_roles'] != '' and  kw['local_roles'] != [] and  kw['local_roles'] is not None:
          local_roles = kw['local_roles']
          new_allowedRolesAndUsers = []
          # Turn it into a list if necessary according to ';' separator
          if type(local_roles) == type('a'):
            local_roles = local_roles.split(';')
          # Local roles now has precedence (since it comes from a WorkList)
          for user_or_group in allowedRolesAndUsers:
            for role in local_roles:
              new_allowedRolesAndUsers.append('%s:%s' % (user_or_group, role))
          allowedRolesAndUsers = new_allowedRolesAndUsers

      return allowedRolesAndUsers

    # searchResults has inherited security assertions.
    def searchResults(self, REQUEST=None, **kw):
        """
            Calls ZCatalog.searchResults with extra arguments that
            limit the results to what the user is allowed to see.
        """
        kw[ 'allowedRolesAndUsers' ] = self.getAllowedRolesAndUsers(**kw) # XXX allowedRolesAndUsers naming is wrong

        if not _checkPermission(
            CMFCorePermissions.AccessInactivePortalContent, self ):
            base = aq_base( self )
            now = DateTime()
            kw[ 'effective' ] = { 'query' : now, 'range' : 'max' }
            kw[ 'expires'   ] = { 'query' : now, 'range' : 'min' }

        
        if not kw.has_key('limit'):
          kw['limit'] = 1000

        #LOG("search allowedRolesAndUsers",0,str(kw[ 'allowedRolesAndUsers' ]))
        return apply(ZCatalog.searchResults, (self, REQUEST), kw)

    __call__ = searchResults

    def countResults(self, REQUEST=None, **kw):
        """
            Calls ZCatalog.countResults with extra arguments that
            limit the results to what the user is allowed to see.
        """
        kw[ 'allowedRolesAndUsers' ] = self.getAllowedRolesAndUsers(**kw) # XXX allowedRolesAndUsers naming is wrong
        
        # Forget about permissions in statistics
        # (we should not count lines more than once with statistic expressions)
        if kw.has_key('select_expression'): del kw[ 'allowedRolesAndUsers' ]

        # XXX This needs to be set again
        #if not _checkPermission(
        #    CMFCorePermissions.AccessInactivePortalContent, self ):
        #    base = aq_base( self )
        #    now = DateTime()
        #    #kw[ 'effective' ] = { 'query' : now, 'range' : 'max' }
        #    #kw[ 'expires'   ] = { 'query' : now, 'range' : 'min' }

        return apply(ZCatalog.countResults, (self, REQUEST), kw)

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

        w = IndexableObjectWrapper(vars, object)

        object_path = object.getPhysicalPath()
        portal_path = object.portal_url.getPortalObject().getPhysicalPath()
        if len(object_path) > len(portal_path) + 2 and getattr(object, 'isRADContent', 0):
          # This only applied to ERP5 Contents (not CPS)
          # We are now in the case of a subobject of a root document
          # We want to return single security information
          document_object = aq_inner(object)
          for i in range(0, len(object_path) - len(portal_path) - 2):
            document_object = document_object.aq_parent
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

        return w

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
    def unindexObject(self, object, path=None, sql_catalog_id=None):
        """
          Remove from catalog.
        """
        if path is None:
          url = self.__url(object)
        else:
          url = path
        self.uncatalog_object(url, sql_catalog_id=sql_catalog_id)

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
    def getDynamicRelatedKeyList(self, sql_catalog_id=None, **kw):
      """
      Return the list of dynamic related keys.
      This method will try to automatically generate new related key
      by looking at the category tree.

      For exemple it will generate:
      destination_title | category,catalog/title/z_related_destination
      default_destination_title | category,catalog/title/z_related_destination
      """
      related_key_list = []
      base_cat_id_list = self.portal_categories.getBaseCategoryList()
      default_string = 'default_'
      for key in kw.keys():
        prefix = ''
        if key.startswith(default_string):
          key = key[len(default_string):]
          prefix = default_string
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
        method_name_length = len(DYNAMIC_METHOD_NAME)
        zope_security = '__roles__'
        if (name.startswith(DYNAMIC_METHOD_NAME) and \
          (not name.endswith(zope_security))):
          base_category_id = name[len(DYNAMIC_METHOD_NAME):]
          method = RelatedBaseCategory(base_category_id)
          setattr(self.__class__, name, 
                  method)
          klass = aq_base(self).__class__
          if hasattr(klass, 'security'):
            from Products.ERP5Type import Permissions as ERP5Permissions
            klass.security.declareProtected(ERP5Permissions.View, name)
          else:
            # XXX security declaration always failed....
            LOG('WARNING ERP5Form SelectionTool, security not defined on',
                0, klass.__name__)
          return getattr(self, name)
        else:
          return aq_base_name
      return aq_base_name



InitializeClass(CatalogTool)
