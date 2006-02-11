##############################################################################
#
# Copyright (c) 2002-2006 Nexedi SARL and Contributors. All Rights Reserved.
#                         Jean-Paul Smets-Solanes <jp@nexedi.com>
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

from Products.CMFCore.utils import UniqueObject

from Acquisition import Implicit
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass, DTMLFile
from App.config import getConfiguration
import os

from Products.ERP5Type import Permissions
from Products.ERP5Type import _dtmldir
from Products.ERP5Type.Tool.BaseTool import BaseTool
from Products.ERP5Type.Document.Folder import Folder

from Products.ERP5Type.Utils import readLocalPropertySheet, writeLocalPropertySheet, getLocalPropertySheetList
from Products.ERP5Type.Utils import readLocalExtension, writeLocalExtension, getLocalExtensionList
from Products.ERP5Type.Utils import readLocalTest, writeLocalTest, getLocalTestList
from Products.ERP5Type.Utils import readLocalDocument, writeLocalDocument, getLocalDocumentList
from Products.ERP5Type.Utils import readLocalConstraint, writeLocalConstraint, getLocalConstraintList
from Products.ERP5Type.InitGenerator import getProductDocumentPathList

from Products.ERP5Type.Base import _aq_reset

from Products.ERP5Type import allowClassTool

if allowClassTool():

  class ClassTool(BaseTool):
      """
      A tool to edit code through the web
      """
      id = 'portal_classes'
      meta_type = 'ERP5 Class Tool'
  
      # Declarative Security
      security = ClassSecurityInfo()
  
      #
      #   ZMI methods
      #
      manage_options = ( ( { 'label'      : 'Overview'
                          , 'action'     : 'manage_overview'
                          }
                          ,{ 'label'      : 'Documents'
                          , 'action'     : 'manage_viewDocumentList'
                          }
                          ,{ 'label'      : 'PropertySheets'
                          , 'action'     : 'manage_viewPropertySheetList'
                          }
                          ,{ 'label'      : 'Constraints'
                          , 'action'     : 'manage_viewConstraintList'
                          }
                          ,{ 'label'      : 'Extensions'
                          , 'action'     : 'manage_viewExtensionList'
                          }
                          ,{ 'label'      : 'Tests'
                          , 'action'     : 'manage_viewTestList'
                          }
                          ,{ 'label'      : 'Product Generation'
                          , 'action'     : 'manage_viewProductGeneration'
                          }
                          ,
                          )
                      + tuple (
                          filter(lambda a: a['label'] not in ('Contents', 'View'), 
                                                        Folder.manage_options))
                      )
  
      security.declareProtected( Permissions.ManagePortal, 'manage_overview' )
      manage_overview = DTMLFile( 'explainDocumentTool', _dtmldir )
  
      security.declareProtected( Permissions.ManagePortal, 'manage_viewPropertySheetList' )
      manage_viewPropertySheetList = DTMLFile( 'viewPropertySheetList', _dtmldir )
  
      security.declareProtected( Permissions.ManagePortal, 'manage_viewDocumentList' )
      manage_viewDocumentList = DTMLFile( 'viewDocumentList', _dtmldir )
  
      security.declareProtected( Permissions.ManagePortal, 'manage_viewExtensionList' )
      manage_viewExtensionList = DTMLFile( 'viewExtensionList', _dtmldir )
  
      security.declareProtected( Permissions.ManagePortal, 'manage_viewTestList' )
      manage_viewTestList = DTMLFile( 'viewTestList', _dtmldir )
  
      security.declareProtected( Permissions.ManagePortal, 'manage_viewConstraintList' )
      manage_viewConstraintList = DTMLFile( 'viewConstraintList', _dtmldir )
  
      security.declareProtected( Permissions.ManagePortal, 'manage_editDocumentForm' )
      manage_editDocumentForm = DTMLFile( 'editDocumentForm', _dtmldir )
  
      security.declareProtected( Permissions.ManagePortal, 'manage_editExtensionForm' )
      manage_editExtensionForm = DTMLFile( 'editExtensionForm', _dtmldir )
  
      security.declareProtected( Permissions.ManagePortal, 'manage_editTestForm' )
      manage_editTestForm = DTMLFile( 'editTestForm', _dtmldir )
  
      security.declareProtected( Permissions.ManagePortal, 'manage_editConstraintForm' )
      manage_editConstraintForm = DTMLFile( 'editConstraintForm', _dtmldir )
  
      security.declareProtected( Permissions.ManagePortal, 'manage_editPropertySheetForm' )
      manage_editPropertySheetForm = DTMLFile( 'editPropertySheetForm', _dtmldir )

      security.declareProtected( Permissions.ManagePortal, 'manage_viewProductGeneration' )
      manage_viewProductGeneration = DTMLFile( 'viewProductGeneration', _dtmldir )

      # Clears the cache of all databases
      def _clearCache(self):
        database = self.Control_Panel.Database
        for name in database.getDatabaseNames():
          from zLOG import LOG
          LOG('_clearCache', 0, str(name))
          database[name].manage_minimize()
      
      security.declareProtected( Permissions.ManagePortal, 'getLocalPropertySheetList' )
      def getLocalPropertySheetList(self):
        """
          Return a list of PropertySheet id which can be modified through the web
        """
        return getLocalPropertySheetList()
  
      security.declareProtected( Permissions.ManagePortal, 'getLocalExtensionList' )
      def getLocalExtensionList(self):
        """
          Return a list of Extension id which can be modified through the web
        """
        return getLocalExtensionList()
  
      security.declareProtected( Permissions.ManagePortal, 'getLocalTestList' )
      def getLocalTestList(self):
        """
          Return a list of Test id which can be modified through the web
        """
        return getLocalTestList()
  
      security.declareProtected( Permissions.ManagePortal, 'getLocalConstraintList' )
      def getLocalConstraintList(self):
        """
          Return a list of Constraint id which can be modified through the web
        """
        return getLocalConstraintList()
  
      security.declareProtected( Permissions.ManagePortal, 'getLocalDocumentList' )
      def getLocalDocumentList(self):
        """
          Return a list of Document id which can be modified through the web
        """
        return getLocalDocumentList()
  
      security.declareProtected( Permissions.ManagePortal, 'getProductDocumentPathList' )
      def getProductDocumentPathList(self):
        """
          Return a list of Document id which can be modified through the web
        """
        return getProductDocumentPathList()
  
      security.declareProtected( Permissions.ManagePortal, 'getDocumentText' )
      def getDocumentText(self, class_id):
        """
          Updates a Document with a new text
        """
        return readLocalDocument(class_id)
  
      security.declareProtected( Permissions.ManageExtensions, 'newDocument' )
      def newDocument(self, class_id, REQUEST=None):
        """
          Updates a Document with a new text
        """
        text = """
##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
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

from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowMethod
from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5Type.XMLObject import XMLObject

class %s(XMLObject):
    # CMF Type Definition
    meta_type = 'MYPROJECT Template Document'
    portal_type = 'Template Document'
    isPortalContent = 1
    isRADContent = 1

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)

    # Default Properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.CategoryCore
                      , PropertySheet.DublinCore
                      )""" % class_id
        writeLocalDocument(class_id, text)
        if REQUEST is not None:
          REQUEST.RESPONSE.redirect('%s/manage_editDocumentForm?class_id=%s&message=Document+Created' % (self.absolute_url(), class_id))
  
      security.declareProtected( Permissions.ManageExtensions, 'editDocument' )
      def editDocument(self, class_id, text, REQUEST=None):
        """
          Updates a Document with a new text
        """
        previous_text = readLocalDocument(class_id)
        writeLocalDocument(class_id, text, create=0)
        if REQUEST is not None:
          REQUEST.RESPONSE.redirect('%s/manage_editDocumentForm?class_id=%s&message=Document+Saved' % (self.absolute_url(), class_id))
  
      security.declareProtected( Permissions.ManageExtensions, 'importDocument' )
      def importDocument(self, class_id, class_path=None, REQUEST=None):
        """
          Imports a document class
        """
        from Products.ERP5Type.Utils import importLocalDocument
        local_product = self.Control_Panel.Products.ERP5Type
        app = local_product._p_jar.root()['Application']
        importLocalDocument(class_id, document_path=class_path)
        
        # Clear object cache and reset _aq_dynamic after reload
        self._clearCache()
        _aq_reset()
        
        if REQUEST is not None and class_path is None:
          REQUEST.RESPONSE.redirect('%s/manage_editDocumentForm?class_id=%s&message=Document+Reloaded+Successfully' % (self.absolute_url(), class_id))
  
  
      security.declareProtected( Permissions.ManagePortal, 'getPropertySheetText' )
      def getPropertySheetText(self, class_id):
        """
          Updates a PropertySheet with a new text
        """
        return readLocalPropertySheet(class_id)
  
      security.declareProtected( Permissions.ManageExtensions, 'newPropertySheet' )
      def newPropertySheet(self, class_id, REQUEST=None):
        """
          Updates a PropertySheet with a new text
        """
        text = """
##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
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

class PropertySheetTemplate:
    \"\"\"
        PropertySheetTemplate properties for all ERP5 objects
    \"\"\"

    _properties = (
        {   'id'          : 'a_property',
            'description' : 'A local property description',
            'type'        : 'string',
            'mode'        : '' },
    )
  

"""
        writeLocalPropertySheet(class_id, text)
        if REQUEST is not None:
          REQUEST.RESPONSE.redirect('%s/manage_editPropertySheetForm?class_id=%s&message=PropertySheet+Created' % (self.absolute_url(), class_id))
  
      security.declareProtected( Permissions.ManageExtensions, 'editPropertySheet' )
      def editPropertySheet(self, class_id, text, REQUEST=None):
        """
          Updates a PropertySheet with a new text
        """
        previous_text = readLocalPropertySheet(class_id)
        writeLocalPropertySheet(class_id, text, create=0)
        if REQUEST is not None:
          REQUEST.RESPONSE.redirect('%s/manage_editPropertySheetForm?class_id=%s&message=PropertySheet+Saved' % (self.absolute_url(), class_id))
  
      security.declareProtected( Permissions.ManageExtensions, 'importPropertySheet' )
      def importPropertySheet(self, class_id, REQUEST=None):
        """
          Imports a PropertySheet class
        """
        from Products.ERP5Type.Utils import importLocalPropertySheet
        local_product = self.Control_Panel.Products.ERP5Type
        app = local_product._p_jar.root()['Application']
        importLocalPropertySheet(class_id)
        # Reset _aq_dynamic after reload
        # There is no need to reset the cache in this case because
        # XXX it is not sure however that class defined propertysheets will be updated
        _aq_reset() 
        if REQUEST is not None:
          REQUEST.RESPONSE.redirect('%s/manage_editPropertySheetForm?class_id=%s&message=PropertySheet+Reloaded+Successfully' % (self.absolute_url(), class_id))
  
      security.declareProtected( Permissions.ManagePortal, 'getExtensionText' )
      def getExtensionText(self, class_id):
        """
          Updates a Extension with a new text
        """
        return readLocalExtension(class_id)
  
      security.declareProtected( Permissions.ManageExtensions, 'newExtension' )
      def newExtension(self, class_id, REQUEST=None):
        """
          Updates a Extension with a new text
        """
        text = """
##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
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

def myExtensionMethod(self, param=None):
  pass
"""
        writeLocalExtension(class_id, text)
        if REQUEST is not None:
          REQUEST.RESPONSE.redirect('%s/manage_editExtensionForm?class_id=%s&message=Extension+Created' % (self.absolute_url(), class_id))
  
      security.declareProtected( Permissions.ManageExtensions, 'editExtension' )
      def editExtension(self, class_id, text, REQUEST=None):
        """
          Updates a Extension with a new text
        """
        previous_text = readLocalExtension(class_id)
        writeLocalExtension(class_id, text, create=0)
        if REQUEST is not None:
          REQUEST.RESPONSE.redirect('%s/manage_editExtensionForm?class_id=%s&message=Extension+Saved' % (self.absolute_url(), class_id))
  
      security.declareProtected( Permissions.ManagePortal, 'getTestText' )
      def getTestText(self, class_id):
        """
          Updates a Test with a new text
        """
        return readLocalTest(class_id)
  
      security.declareProtected( Permissions.ManageExtensions, 'newTest' )
      def newTest(self, class_id, REQUEST=None):
        """
          Updates a Test with a new text
        """
        text = '''
##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
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

from Products.ERP5Type.tests.ERP5TypeTestCase import ERP5TypeTestCase

class Test(ERP5TypeTestCase):
  """
  A Sample Test Class
  """

  def getTitle(self):
    return "SampleTest"

  def getBusinessTemplateList(self):
    """
    Tuple of Business Templates we need to install
    """
    return (,)

  def enableLightInstall(self):
    """
    Return if we should do a light install (1) or not (0)
    """
    return 1

  def enableActivityTool(self):
    """
    Return if we should create (1) or not (0) an activity tool
    """
    return 1

  def afterSetUp(self):
    """
    This is ran before anything, used to set the environment
    """
    # here, you can create the categories and objects your test will depend on
    pass

  def test_01_sampleTest(self):
    """
    A Sample Test
    
    For the method to be called during the test,
    its name must start with 'test'.
    The '_01_' part of the name is not mandatory,
    it just allows you to define in which order the tests are to be launched.
    Tests methods (self.assert... and self.failIf...)
    are defined in /usr/lib/python/unittest.py.
    """
    self.assertEqual(0, 1)
'''
        writeLocalTest(class_id, text)
        if REQUEST is not None:
          REQUEST.RESPONSE.redirect('%s/manage_editTestForm?class_id=%s&message=Test+Created' % (self.absolute_url(), class_id))
  
      security.declareProtected( Permissions.ManageExtensions, 'editTest' )
      def editTest(self, class_id, text, REQUEST=None):
        """
          Updates a Test with a new text
        """
        previous_text = readLocalTest(class_id)
        writeLocalTest(class_id, text, create=0)
        if REQUEST is not None:
          REQUEST.RESPONSE.redirect('%s/manage_editTestForm?class_id=%s&message=Test+Saved' % (self.absolute_url(), class_id))
  
      security.declareProtected( Permissions.ManagePortal, 'getConstraintText' )
      def getConstraintText(self, class_id):
        """
          Updates a Constraint with a new text
        """
        return readLocalConstraint(class_id)
  
      security.declareProtected( Permissions.ManageExtensions, 'newConstraint' )
      def newConstraint(self, class_id, REQUEST=None):
        """
          Updates a Constraint with a new text
        """
        text = """
##############################################################################
#
# Copyright (c) 2002 Nexedi SARL and Contributors. All Rights Reserved.
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

from Products.ERP5Type.Constraint import Constraint

class ConstraintTemplate(Constraint):
    \"\"\"
      Explain here what this constraint checker does
    \"\"\"

    def checkConsistency(self, object, fixit = 0):
      \"\"\"
        Implement here the consistency checker
        whenever fixit is not 0, object data should be updated to 
        satisfy the constraint
      \"\"\"

      errors = []
      
      # Do the job here
      
      return errors
"""
        writeLocalConstraint(class_id, text)
        if REQUEST is not None:
          REQUEST.RESPONSE.redirect('%s/manage_editConstraintForm?class_id=%s&message=Constraint+Created' % (self.absolute_url(), class_id))

      security.declareProtected( Permissions.ManageExtensions, 'editConstraint' )
      def editConstraint(self, class_id, text, REQUEST=None):
        """
          Updates a Constraint with a new text
        """
        previous_text = readLocalConstraint(class_id)
        writeLocalConstraint(class_id, text, create=0)
        if REQUEST is not None:
          REQUEST.RESPONSE.redirect('%s/manage_editConstraintForm?class_id=%s&message=Constraint+Saved' % (self.absolute_url(), class_id))

      security.declareProtected( Permissions.ManageExtensions, 'generateProduct' )
      def generateProduct(self, product_id,
                          document_id_list=(), property_sheet_id_list=(), constraint_id_list=(),
                          extension_id_list=(), test_id_list=(), REQUEST=None):
        """Generate a Product
        """
        # Ensure that Products exists.
        product_path = os.path.join(getConfiguration().instancehome, 'Products')
        if not os.path.exists(product_path):
          os.mkdir(product_path)

        # Make a new Product directory if not present.
        base_path = os.path.join(product_path, product_id)
        if not os.path.exists(base_path):
          os.mkdir(base_path)

        # Make sub-directories if not present.
        for d in ('Interface', 'Document', 'PropertySheet', 'Extensions', 'Tool', 'Constraint',
                  'tests', 'help', 'skins', 'dtml', ):
          path = os.path.join(base_path, d)
          if not os.path.exists(path):
            os.mkdir(path)
          # Create an empty __init__.py.
          init = os.path.join(path, '__init__.py')
          if not os.path.exists(init):
            f = open(init, 'w')
            f.close()
          # For convenience, make .cvsignore.
          cvsignore = os.path.join(path, '.cvsignore')
          if not os.path.exists(cvsignore):
            f = open(cvsignore, 'w')
            try:
              f.write('*.pyc' + os.linesep)
            finally:
              f.close()

        # Create a Permissions module for this Product.
        permissions = os.path.join(base_path, 'Permissions.py')
        if not os.path.exists(permissions):
          f = open(permissions, 'w')
          f.close()

        # Make .cvsignore for convenience.
        cvsignore = os.path.join(base_path, '.cvsignore')
        if not os.path.exists(cvsignore):
          f = open(cvsignore, 'w')
          try:
            f.write('*.pyc' + os.linesep)
          finally:
            f.close()

        # Create an init file for this Product.
        init = os.path.join(base_path, '__init__.py')
        if not os.path.exists(init):
          text = '''
##############################################################################
#
# Copyright (c) 2006 Nexedi SARL and Contributors. All Rights Reserved.
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
"""
    ERP5 Free Software ERP
"""

# Update ERP5 Globals
from Products.ERP5Type.Utils import initializeProduct, updateGlobals
import sys, Permissions
this_module = sys.modules[ __name__ ]
document_classes = updateGlobals( this_module, globals(), permissions_module = Permissions)

# Finish installation
def initialize( context ):
  import Document
  initializeProduct(context, this_module, globals(),
                         document_module = Document,
                         document_classes = document_classes,
                         object_classes = (),
                         portal_tools = (),
                         content_constructors = (),
                         content_classes = ())
'''
          f = open(init, 'w')
          try:
            f.write(text)
          finally:
            f.close()

        # Create a skeleton README.txt.
        readme = os.path.join(base_path, 'README.txt')
        if not os.path.exists(readme):
          text = '''
%s

  %s was automatically generated by ERP5 Class Tool.
''' % (product_id, product_id)
          f = open(readme, 'w')
          try:
            f.write(text)
          finally:
            f.close()

        # Now, copy selected code.
        for d, m, id_list in (('Document', readLocalDocument, document_id_list),
                              ('PropertySheet', readLocalPropertySheet, property_sheet_id_list),
                              ('Constraint', readLocalConstraint, constraint_id_list),
                              ('tests', readLocalTest, test_id_list),
                              ('Extensions', readLocalExtension, extension_id_list)):
          for class_id in id_list:
            path = os.path.join(base_path, d, class_id) + '.py'
            text = m(class_id)
            f = open(path, 'w')
            try:
              f.write(text)
            finally:
              f.close()

        if REQUEST is not None:
          REQUEST.RESPONSE.redirect('%s/manage_viewProductGeneration?message=New+Product+Saved+In+%s' % (self.absolute_url(), base_path))

else:

  class ClassTool(BaseTool):
      """
      A tool to edit code through the web
      """
      id = 'portal_classes'
      meta_type = 'ERP5 Dummy Class Tool'

      # Declarative Security
      security = ClassSecurityInfo()

      security.declareProtected( Permissions.ManagePortal, 'manage_overview' )
      manage_overview = DTMLFile( 'explainDummyClassTool', _dtmldir )        

InitializeClass(ClassTool)
