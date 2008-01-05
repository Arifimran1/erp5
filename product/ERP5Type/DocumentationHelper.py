from Acquisition import Implicit
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

from Products.CMFCore.utils import getToolByName

from Products.ERP5Type.Accessor.Accessor import Accessor
from Products.ERP5Type.Base import WorkflowMethod
from Products.ERP5Type import Permissions

class DocumentationSection(Implicit):

  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  def __init__(self, id, title, class_name, uri_list):
    self.id = id
    self.title = title
    self.class_name = class_name
    self.uri_list = uri_list

  security.declareProtected(Permissions.AccessContentsInformation, 'getClassName')
  def getClassName(self):
    return self.class_name

  security.declareProtected(Permissions.AccessContentsInformation, 'getURIList')
  def getURIList(self):
    return self.uri_list

  # more API needed XXX

InitializeClass(DocumentationSection)

class DocumentationHelper(Implicit):
  """
    Example URIs

    person_module/23
    person_module/23#title
    person_module/23#getTitle
    portal_worklows/validation_workflow
    portal_worklows/validation_workflow/states/draft
    portal_worklows/validation_workflow/states/draft#title
    Products.ERP5Type.Document.Person.notify
    Products.ERP5Type.Document.Person.isRAD
    portal_types/Person
    portal_types/Person/actions#view
  """
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  # Methods to override
  def __init__(self, uri):
    self.uri = uri

  def getDocumentedObject(self):
    if '/' in self.uri and '#' not in self.uri:
      # URI refers to a portal object
      # and is a relative URL
      documented_object = self.getPortalObject().portal_categories.resolveCategory(self.uri)  
    elif '/' in self.uri and '#' in self.uri:
      url, method = self.uri.split('#') 
      # if / in method, method's not an acessor but a workflow method
      documented_object = self.getPortalObject().unrestrictedTraverse(url)
      if '/' not in method:
        documented_object = self.getPortalObject().unrestrictedTraverse(url)
        documented_object = getattr(documented_object, method, None)
      else:
        wf_url = 'portal_workflow/%s' % method
        documented_object = self.getPortalObject().unrestrictedTraverse(wf_url)
    else:
      # URI refers to a python class / method
      import imp
      module_list = self.uri.split('.')
      base_module = module_list[0]
      if base_module == 'Products':
        # For now, we do not even try to import
        # or locate objects which are not in Products
        import Products
        documented_object = Products
        for key in module_list[1:]:
          LOG('loop in module_list', 0, repr(documented_object))
          documented_object = getattr(documented_object, key)
      else:
        raise NotImplemented
        #fp, pathname, description = imp.find_module(base_module)
        #documented_object = imp.load_module(fp, pathname, description)

    return documented_object

  def getTitle(self):
    """
    Returns the title of the documentation helper
    (ex. class name)
    """
    raise NotImplemented

  def getType(self):
    """
    Returns the type of the documentation helper
    (ex. Class, float, string, Portal Type, etc.)
    """
    raise NotImplemented

  security.declareProtected(Permissions.AccessContentsInformation, 'getSectionList')
  def getSectionList(self):
    """
    Returns a list of documentation sections
    """
    raise NotImplemented

  security.declareProtected(Permissions.AccessContentsInformation, 'getURI')
  def getURI(self):
    """
    Returns a URI to later access this documentation
    from portal_classes
    """
    return self.uri

  # Generic methods which all subclasses should inherit
  security.declareProtected(Permissions.AccessContentsInformation, 'getClassName')
  def getClassName(self):
    """
    Returns our own class name
    """
    return self.__class__.__name__

  security.declareProtected(Permissions.AccessContentsInformation, 'view')
  def view(self):
    """
    Renders the documentation with a standard form
    ex. PortalTypeInstanceDocumentationHelper_view
    """
    return getattr(self, '%s_view' % self.getClassName())()

  security.declareProtected(Permissions.AccessContentsInformation, '__call__')
  def __call__(self):
    return self.view()

InitializeClass(DocumentationHelper)

class PortalTypeInstanceDocumentationHelper(DocumentationHelper):
  """
    Provides access to all documentation information
    of a portal type instance.
  """

  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  def __init__(self, uri):
    self.uri = uri

  def getInstance(self):
    return self.getPortalObject().restrictedTraverse(self.uri)

  # API Implementation
  security.declareProtected( Permissions.AccessContentsInformation, 'getTitle' )
  def getTitle(self):
    """
    Returns the title of the documentation helper
    """
    return self.getInstance().getTitleOrId()

  security.declareProtected( Permissions.AccessContentsInformation, 'getType' )
  def getType(self):
    """
    Returns the type of the documentation helper
    """
    return "Portal Type Instance"

  security.declareProtected( Permissions.AccessContentsInformation, 'getSectionList' )
  def getSectionList(self):
    """
    Returns a list of documentation sections
    """
    return [
      #DocumentationSection(
        #id='instance_property',
        #title='Instance Properties',
        #class_name='InstancePropertyDocumentationHelper',
        #uri_list=self.getClassPropertyURIList(),
      #),
      DocumentationSection(
        id='workflow_method',
        title='Workflow Method',
        class_name='WorkflowMethodDocumentationHelper',
        uri_list=self.getWorkflowMethodURIList(inherited=0),
      ),
      DocumentationSection(
        id='accessor',
        title='Accessor',
        class_name='AccessorMethodDocumentationHelper',
        uri_list=self.getAccessorMethodURIList(inherited=0),
      ),
      DocumentationSection(
        id='class_method',
        title='Class Methods',
        class_name='ClassMethodDocumentationHelper',
        uri_list=self.getClassMethodURIList(inherited=0),
      ).__of__(self.getInstance()),
    ]

  # Specific methods
  security.declareProtected( Permissions.AccessContentsInformation, 'getPortalType' )
  def getPortalType(self):
    """
    """
    return self.getInstance().getPortalType()

  def _getPropertyHolder(self):
    from Products.ERP5Type.Base import Base
    return Base.aq_portal_type[(self.getPortalType(), self.getInstance().__class__)]

  security.declareProtected( Permissions.AccessContentsInformation, 'getAccessorMethodItemList' )
  def getAccessorMethodItemList(self):
    """
    """
    return self._getPropertyHolder().getAccessorMethodItemList()

  security.declareProtected( Permissions.AccessContentsInformation, 'getAccessorMethodIdList' )
  def getAccessorMethodIdList(self):
    """
    """
    return self._getPropertyHolder().getAccessorMethodIdList()

  security.declareProtected( Permissions.AccessContentsInformation, 'getAccessorMethodURIList' )
  def getAccessorMethodURIList(self, inherited=1, local=1):
    """
    Returns a list of URIs to accessor methods
    """
    method_id_list = self.getAccessorMethodIdList(inherited=inherited, local=local)
    klass = self.getInstance().__class__
    class_name = klass.__name__
    module = klass.__module__
    uri_prefix = '%s.%s.' % (module, class_name)
    return map(lambda x: '%s%s' % (uri_prefix, x), method_id_list)

  security.declareProtected(Permissions.AccessContentsInformation, 'getWorkflowMethodItemList' )
  def getWorkflowMethodItemList(self):
    """
    """
    return self._getPropertyHolder().getWorkflowMethodItemList()

  security.declareProtected(Permissions.AccessContentsInformation, 'getWorkflowObject' )
  def getWorkflowObject(self):
    """
    """
    return self._getPropertyHolder()
  
  security.declareProtected(Permissions.AccessContentsInformation, 'getWorkflowMethodIdList' )
  def getWorkflowMethodIdList(self):
    """
    """
    return self._getPropertyHolder().getWorkflowMethodIdList()    

  def getWorkflowMethodURIList(self, inherited=1, local=1):
    """
    Returns a list of URIs to workflow  methods
    """
    method_id_list = self.getWorkflowMethodIdList(inherited=inherited, local=local)
    klass = self.getInstance().__class__
    class_name = klass.__name__
    module = klass.__module__
    uri_prefix = '%s.%s.' % (module, class_name)
    return map(lambda x: '%s%s' % (uri_prefix, x), method_id_list)


  security.declareProtected(Permissions.AccessContentsInformation, 'getActionMethodItemList' )
  def getActionMethodItemList(self):
    """
    """
    return self._getPropertyHolder().getActionMethodItemList()

  security.declareProtected( Permissions.AccessContentsInformation, 'getActionMethodIdList' )
  def getActionMethodIdList(self):
    """
    """
    return self._getPropertyHolder().getActionMethodIdList()

  security.declareProtected( Permissions.AccessContentsInformation, 'getClassMethodItemList' )
  def getClassMethodItemList(self, inherited=1, local=1):
    """
    Return a list of tuple (id, method) for every class method
    """
    klass = self.getInstance().__class__
    return self._getPropertyHolder().getClassMethodItemList(klass, inherited=inherited, local=local)

  security.declareProtected( Permissions.AccessContentsInformation, 'getClassMethodIdList' )
  def getClassMethodIdList(self, inherited=1, local=1):
    """
    Return a list of tuple (id, method) for every class method
    """
    klass = self.getInstance().__class__
    return self._getPropertyHolder().getClassMethodIdList(klass, inherited=inherited, local=local)

  security.declareProtected( Permissions.AccessContentsInformation, 'getClassMethodURIList' )
  def getClassMethodURIList(self, inherited=1, local=1):
    """
    Returns a list of URIs to class methods
    """
    method_id_list = self.getClassMethodIdList(inherited=inherited, local=local)
    klass = self.getInstance().__class__
    class_name = klass.__name__
    module = klass.__module__
    uri_prefix = '%s.%s.' % (module, class_name)
    return map(lambda x: '%s%s' % (uri_prefix, x), method_id_list)

  security.declareProtected( Permissions.AccessContentsInformation, 'getClassPropertyItemList' )
  def getClassPropertyItemList(self, inherited=1, local=1):
    """
    Return a list of tuple (id, method) for every class method
    """
    klass = self.getInstance().__class__
    return self._getPropertyHolder().getClassPropertyItemList(klass, inherited=inherited, local=local)

  security.declareProtected( Permissions.AccessContentsInformation, 'getClassPropertyIdList' )
  def getClassPropertyIdList(self, inherited=1, local=1):
    """
    Return a list of tuple (id, method) for every class method
    """
    klass = self.getInstance().__class__
    return self._getPropertyHolder().getClassPropertyIdList(klass, inherited=inherited, local=local)

  security.declareProtected( Permissions.AccessContentsInformation, 'getGeneratedPropertyIdList' )
  def getGeneratedPropertyIdList(self):
    """
    """

  security.declareProtected( Permissions.AccessContentsInformation, 'getGeneratedBaseCategoryIdList' )
  def getGeneratedBaseCategoryIdList(self):
    """
    """

InitializeClass(PortalTypeInstanceDocumentationHelper)

class PortalDocumentationHelper(DocumentationHelper):
  """
  """

class PortalTypeDocumentationHelper(DocumentationHelper):
  """
  """

class ClassDocumentationHelper(DocumentationHelper):
  """
  """

class AccessorDocumentationHelper(DocumentationHelper):
  """
  """

class ClassMethodDocumentationHelper(DocumentationHelper):
  """
    Provides documentation about a class method
  """
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  security.declareProtected(Permissions.AccessContentsInformation, 'getDescription')
  def getDescription(self):
    return self.getDocumentedObject().__doc__

  security.declareProtected( Permissions.AccessContentsInformation, 'getType' )
  def getType(self):
    """
    Returns the type of the documentation helper
    """
    return "Class Method"

  security.declareProtected( Permissions.AccessContentsInformation, 'getTitle' )
  def getTitle(self):
    """
    Returns the type of the documentation helper
    """
    return self.getDocumentedObject().__name__

InitializeClass(ClassMethodDocumentationHelper)

class AccessorMethodDocumentationHelper(DocumentationHelper):
  """
    Provides documentation about an accessor
  """
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  def __init__(self, uri):
    self.uri = uri

  security.declareProtected(Permissions.AccessContentsInformation, 'getDescription')
  def getDescription(self):
    return self.getDocumentedObject().__doc__

  security.declareProtected( Permissions.AccessContentsInformation, 'getType' )
  def getType(self):
    """
    Returns the type of the documentation helper
    """
    return self.getDocumentedObject().func_code.__module__

  security.declareProtected( Permissions.AccessContentsInformation, 'getTitle' )
  def getTitle(self):
    """
    Returns the title of the documentation helper
    """
    return self.getDocumentedObject().__name__

  security.declareProtected( Permissions.AccessContentsInformation, 'getArgCount' )
  def getArgCount(self):
    """
    Returns the number of args of the accessor
    """
    return self.getDocumentedObject().func_code.co_argcount

  security.declareProtected( Permissions.AccessContentsInformation, 'getVarNames' )
  def getVarNames(self):
    """
    Returns the list of args of the accessor
    """
    return self.getDocumentedObject().func_code.co_varnames


InitializeClass(AccessorMethodDocumentationHelper)

class CallableDocumentationHelper(DocumentationHelper):
  """
  """

class InstancePropertyDocumentationHelper(DocumentationHelper):
  """
  """

class PropertyDocumentationHelper(DocumentationHelper):
  """
  """

class WorkflowMethodDocumentationHelper(DocumentationHelper):
  """
    Provides documentation about a workflow method
  """
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  def __init__(self, uri):
    self.uri = uri

  security.declareProtected(Permissions.AccessContentsInformation, 'getDescription')
  def getDescription(self):
    return self.getDocumentedObject().__dict__['description']

  security.declareProtected(Permissions.AccessContentsInformation, 'getType' )
  def getType(self):
    """
    Returns the type of the documentation helper
    """
    return self.getDocumentedObject().__module__

  security.declareProtected(Permissions.AccessContentsInformation, 'getTitle' )
  def getTitle(self):
    """
    Returns the title of the documentation helper
    """
    return self.getDocumentedObject().__dict__['title']

  security.declareProtected(Permissions.AccessContentsInformation, 'getDestinationState' )
  def getDestinationState(self):
    """
    Returns the destination_state of the transition workflow method
    """
    return self.getDocumentedObject().__dict__['new_state_id']

  security.declareProtected(Permissions.AccessContentsInformation, 'getTriggerType' )
  def getTriggerType(self):
    """
    Returns the trigger type of the workflow method
    """
    TT = ['Automatic','Initiated by user action','Initiated by WorkflowMethod']
    TT_id = self.getDocumentedObject().__dict__['trigger_type']
    return TT[TT_id]

  security.declareProtected(Permissions.AccessContentsInformation, 'getLocalRoles' )
  def getLocalRoles(self):
    """
    Returns the local roles of the workflow method
    """
    return self.getDocumentedObject().__ac_local_roles__

  security.declareProtected(Permissions.AccessContentsInformation, 'getAvailableStateIds' )
  def getAvailableStateIds(self):
    """
    Returns available states in the workflow
    """
    return self.getDocumentedObject().getAvailableStateIds()

InitializeClass(WorkflowMethodDocumentationHelper)

class DCWorkflowDocumentationHelper(DocumentationHelper):
  """
    Provides access to all documentation information
    of a workflow.
  """

  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  # API Implementation
  security.declareProtected( Permissions.AccessContentsInformation, 'getTitle' )
  def getTitle(self):
    """
    Returns the title of the documentation helper
    """
    return self.getDocumentedObject().getTitleOrId()

  security.declareProtected( Permissions.AccessContentsInformation, 'getType' )
  def getType(self):
    """
    Returns the type of the documentation helper
    """
    return "DC Workflow"

  security.declareProtected( Permissions.AccessContentsInformation, 'getSectionList' )
  def getSectionList(self):
    """
    Returns a list of documentation sections
    """
    return map(lamda x: x.__of__(self), [
      DocumentationSection(
        id='state',
        title='Workflow States',
        class_name='DCWorkflowStateDocumentationHelper',
        uri_list=self.getStateURIList(),
      ),
      DocumentationSection(
        id='transition',
        title='Workflow Transitions',
        class_name='DCWorkflowTransitionDocumentationHelper',
        uri_list=self.getStateURIList(),
      ),
      DocumentationSection(
        id='variable',
        title='Workflow Variables',
        class_name='DCWorkflowVariableDocumentationHelper',
        uri_list=self.getVariableURIList(),
      ),
      DocumentationSection(
        id='variable',
        title='Workflow Permissions',
        class_name='PermissionDocumentationHelper',
        uri_list=self.getPermissionURIList(),
      ),
    ])

  # Specific methods
  security.declareProtected( Permissions.AccessContentsInformation, 'getDescription' )
  def getDescription(self):
    """
    Returns the title of the documentation helper
    """
    raise NotImplemented

  security.declareProtected( Permissions.AccessContentsInformation, 'getVariableURIList' )
  def getVariableURIList(self):
    """
    """
    raise NotImplemented

  security.declareProtected( Permissions.AccessContentsInformation, 'getStateURIList' )
  def getStateURIList(self):
    """
    """
    raise NotImplemented

  security.declareProtected( Permissions.AccessContentsInformation, 'getVariableURIList' )
  def getVariableURIList(self):
    """
    """
    raise NotImplemented

  security.declareProtected( Permissions.AccessContentsInformation, 'getPermissionURIList' )
  def getPermissionURIList(self):
    """
    """
    raise NotImplemented

  security.declareProtected( Permissions.AccessContentsInformation, 'getGraphImageURL' )
  def getGraphImageURL(self):
    """
      Returns a URL to a graphic representation of the workflow
    """
    raise NotImplemented

  security.declareProtected( Permissions.AccessContentsInformation, 'getGraphImageData' )
  def getGraphImageData(self):
    """
      Returns the graphic representation of the workflow as a PNG file
    """
    raise NotImplemented

InitializeClass(DCWorkflowDocumentationHelper)


#############################################################################
#############################################################################

if 0:
  if 0:
    static_method_list = []    # Class methods
    static_property_list = []  # Class attributes
    dynamic_method_list = []   # Workflow methods
    dynamic_property_list = [] # Document properties
    dynamic_category_list = [] # Categories
    dynamic_accessor_list = [] # Accessors


  security.declareProtected( Permissions.ManagePortal, 'asDocumentationHelper' )
  def asDocumentationHelper(self, item_id=None):
    """
      Fills and return a DocHelper object from context.
      Overload this in any object the has to fill the DocHelper in its own way.

      item_id : If specified, the documented item will be
                getattr(self, item_title) if it exists, otherwise None will
                be returned.

      TODO:
       - Check that filtering is correct : display only and every things
         defined on the class itself.
       - Add a list of all accessible things in the documented item context
         (heritated methods & attributes) in a light way that still allows to
         link directly to the corresponding documentation.
       - Rewrite accessor generation system so that it can generate accessor
         names when given a property/category.

       KEEPMEs:
         There are pieces of code in this function that can have interesting
         results, but who are also very verbose. They are disabled (commented
         out) by default, but they should be kept.
         Explanation of the interest :
         The accessors are gathered from 2 sources : the ones defined on the
         PortalType, and systematically generated names, and tested for
         presence on the documented item.
         There are 4 cases then :
         -Accessor whose name was generated exists both on the PortalType and
          on the documented item. That's normal.
         -Accessor whose name was generated exists neither on the PortalType
          nor on the documented item. That's normal, but could mean that the
          accessor name generator isn't optimal.
         -Accessor whose name was generated is found on the object but not on
          the PortalType. This is a problem.
         -Accessors gathered from PortalType aren't all found by guessing
          systematically the names. That means that the accessor name
          generation is not perfect and requires improvement.

         nb: the accessors are gathered from 2 sources, the first is somehow
         accidental when searching for workflow methods defined on the
         PortalType, and are browsed a second time to be able to group them
         by property or category.
    """
    if item_id is None:
      documented_item = self
      item_id = documented_item.getTitle()
    elif getattr(self, item_id, None) is not None:
      documented_item = getattr(self, item_id)
    else:
      return None

    # The documented object is an instance (or not) of this class.
    item_class = getattr(documented_item, '__bases__', None) is None \
                 and documented_item.__class__ \
                 or documented_item

    static_method_list = []    # Class methods
    static_property_list = []  # Class attributes
    dynamic_method_list = []   # Workflow methods
    dynamic_property_list = [] # Document properties
    dynamic_category_list = [] # Categories
    dynamic_accessor_list = [] # Accessors
    found_accessors = {}       # Accessor names : filled by PortalType-level
                               # scan, and used in PropertySheet-level scan.
    dochelper = newTempDocumentationHelper(self.getParentValue(), self.getId(),
                  title=item_id, type=item_class.__name__,
                  description=inspect.getdoc(documented_item),
                )
    dochelper.setInheritanceList([x.__name__ for x in item_class.__bases__])
    try:
      dochelper.setSourcePath(inspect.getsourcefile(item_class))
    except (IOError, TypeError):
      pass
    # dochelper.setSecurity() # (maybe) TODO: Add class instance security gthering.

    # Class-level method & properties
    for k, v in item_class.__dict__.items():
      subdochelper = newTempDocumentationHelper(dochelper, k,
                  title=k, description=inspect.getdoc(v),
                  security=repr(getattr(documented_item, '%s__roles__' % (k,),None)))
      try:
        subdochelper.setType(v.__class__.__name__)
      except AttributeError:
        pass
      try:
        subdochelper.setSourcePath(inspect.getsourcefile(v))
      except (IOError, TypeError), err:
        pass
      try:
        subdochelper.setSourceCode(inspect.getsource(v))
      except (IOError, TypeError), err:
        pass
      try:
        subdochelper.setArgumentList(inspect.getargspec(v))
      except (IOError, TypeError), err:
        pass
      if subdochelper.getType() in ('function',): # This is a method
        static_method_list.append(subdochelper)
      elif subdochelper.getType() in ('int', 'float', 'long', 'str', 'tuple', 'dict', 'list') \
           and not subdochelper.getTitle().startswith('__'): # This is a property
        subdochelper.setContent(pformat(v))
        static_property_list.append(subdochelper)
      # FIXME: Is there any other interesting type ?

    # PortalType-level methods
    # XXX: accessing portal_type directly because accessors are not generated on instances
    if getattr(documented_item, 'portal_type', None) is not None:
      for k, v in Base.aq_portal_type[documented_item.portal_type].__dict__.items():
        if callable(v) and not (k.startswith('_base') or k.startswith('_category')):
          subdochelper = newTempDocumentationHelper(dochelper, k,
                    title=k, description=inspect.getdoc(v),
                    security=repr(getattr(documented_item, '%s__roles__' % (k,),None)))
          try:
            my_type = v.__class__.__name__
            subdochelper.setType(my_type)
          except AttributeError:
            pass
          if 'Setter' not in my_type and \
             'Getter' not in my_type and \
             'Tester' not in my_type: # Accessors are handled separatelly.
            dynamic_method_list.append(subdochelper)
# KEEPME: usefull to track the differences between accessors defined on
# PortalType and the one detected on the documented item.
#          else:
#            found_accessors[k] = v

    def generatePropertyAccessorNameList(property):
      """
        Generates the possible accessor names for given property.

        FIXME: Should not exist here, but as accessor generation system.
      """
      from Products.ERP5Type.Utils import UpperCase
      res=[]
      cased_id = UpperCase(property['id'])
      for hidden in ('', '_'):
        for getset in ('get', 'set', 'has'): # 'is',
          for default in ('', 'Default', 'Translated'):
            for value in ('', 'Value', 'TranslationDomain'):
              for multivalued in ('', 'List', 'Set'):
                res.append('%s%s%s%s%s%s' % (hidden, getset, default, cased_id, value, multivalued))
      if property.has_key('acquired_property_id') and \
         property['type'] == 'content':
        for aq_property_id in property['acquired_property_id']:
          cased_id = UpperCase('%s_%s' % (property['id'], aq_property_id))
          for hidden in ('', '_'):
            for getset in ('get', 'set'):
              for default in ('', 'Default'):
                for multivalued in ('', 'List'):
                  res.append('%s%s%s%s%s' % (hidden, getset, default, cased_id, multivalued))
      return res

    def generateCategoryAccessorNameList(category):
      """
        Generates the possible accessor names for given category.

        FIXME: Should not exist here, but as accessor generation system.
      """
      from Products.ERP5Type.Utils import UpperCase
      cased_id=UpperCase(category)
      res=['%s%sIds' % (cased_id[0].lower(), cased_id[1:]),
           '%s%sValues' % (cased_id[0].lower(), cased_id[1:])]
      for hidden in ('', '_'):
        for default in ('', 'Default'):
          for multivalued in ('', 'List', 'Set'):
            for attribute in ('', 'TranslatedTitle', 'Uid', 'LogicalPath', 'Id', 'TitleOrId', 'Reference', 'Title'):
              res.append('%sget%s%s%s%s' % (hidden, default, cased_id, attribute, multivalued))
            for attribute in ('', 'Value', 'Uid'):
              res.append('%sset%s%s%s%s' % (hidden, default, cased_id, attribute, multivalued))
      return res

    def accessorAsDocumentationHelper(accessor):
      """
        Generates a documentation helper about a given accessor.
      """
      accessor_dochelper = newTempDocumentationHelper(subdochelper, accessor_name,
                                                      title=accessor_name,
                                                      description=inspect.getdoc(accessor))
      try:
        accessor_dochelper.setSourcePath(inspect.getsourcefile(accessor))
      except (IOError, TypeError), err:
        pass
      try:
        accessor_dochelper.setSourceCode(inspect.getsource(accessor))
      except (IOError, TypeError), err:
        pass
# KEEPME: usefull to track the differences between accessors defined on
# PortalType and the one detected on the documented item.
#      if found_accessors.has_key(accessor_name):
#        del(found_accessors[accessor_name])
#      else:
#        LOG('asDocumentationHelper', 0,
#            'Found but not in the accessor list : %s of type %s' % \
#            (accessor_name, accessor.__class__.__name__))
      return accessor_dochelper

    # PropertySheet-level properties & categories
    # Also handles accessors.
    seen_properties=[]
    seen_categories=[]
    if getattr(documented_item, 'property_sheets', None) is not None:
      for property_sheet in documented_item.property_sheets:
        if getattr(property_sheet, '_properties', None) is not None:
          for property in property_sheet._properties:
            if property in seen_properties:
              continue
            seen_properties.append(property)
            subdochelper = newTempDocumentationHelper(dochelper, k,
                      title=property['id'], description=property['description'],
                      type=property['type'], security=property['mode'],
                      content=pformat(documented_item.getProperty(property['id'])))
            subdochelper_dynamic_accessor_list = []
            for accessor_name in generatePropertyAccessorNameList(property):
              accessor = getattr(item_class, accessor_name, getattr(documented_item, accessor_name, None))
              # First get it on the class, and if not on the instance, thereby among dynamic accessors.
              if accessor is not None:
                subdochelper_dynamic_accessor_list.append(accessorAsDocumentationHelper(accessor))
            subdochelper_dynamic_accessor_list.sort()
            subdochelper.setDynamicAccessorList(subdochelper_dynamic_accessor_list)
            dynamic_accessor_list.append(subdochelper)
            if getattr(documented_item, property['id'], None) is not None:
              dynamic_property_list.append(subdochelper)
        if getattr(property_sheet, '_categories', None) is not None:
          for category in property_sheet._categories:
            if category in seen_categories:
              continue
            seen_categories.append(category)
            subdochelper = newTempDocumentationHelper(dochelper, category, title=category,
                      content=pformat(documented_item.getCategoryMembershipList(category)))
            subdochelper_dynamic_accessor_list = []
            for accessor_name in generateCategoryAccessorNameList(category):
              accessor = getattr(item_class, accessor_name, getattr(documented_item, accessor_name, None))
              # First get it on the class, and if not on the instance, thereby among dynamic accessors.
              if accessor is not None:
                subdochelper_dynamic_accessor_list.append(accessorAsDocumentationHelper(accessor))
            subdochelper_dynamic_accessor_list.sort()
            subdochelper.setDynamicAccessorList(subdochelper_dynamic_accessor_list)
            dynamic_accessor_list.append(subdochelper)
            dynamic_category_list.append(subdochelper)

# KEEPME: usefull to track the differences between accessors defined on
# PortalType and the one detected on the documented item.
#    LOG('asDocumentationHelper', 0, found_accessors)
    static_method_list.sort()
    dochelper.setStaticMethodList(static_method_list)
    static_property_list.sort()
    dochelper.setStaticPropertyList(static_property_list)
    dynamic_method_list.sort()
    dochelper.setDynamicMethodList(dynamic_method_list)
    dynamic_accessor_list.sort()
    dochelper.setDynamicAccessorList(dynamic_accessor_list)
    dynamic_category_list.sort()
    dochelper.setDynamicCategoryList(dynamic_category_list)
    dynamic_property_list.sort()
    dochelper.setDynamicPropertyList(dynamic_property_list)
    return dochelper

