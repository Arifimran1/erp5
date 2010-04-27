# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2002 Coramy SAS and Contributors. All Rights Reserved.
#                    Thierry_Faucher <Thierry_Faucher@coramy.com>
# Copyright (c) 2004-2010 Nexedi SA and Contributors. All Rights Reserved.
#                    Romain Courteaud <romain@nexedi.com>
#                    Łukasz Nowak <luke@nexedi.com>
#                    Jean-Paul Smets <jp@nexedi.com>
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
from zLOG import LOG, WARNING

import zope.interface

from warnings import warn
from AccessControl import ClassSecurityInfo

from Products.CMFCategory.Renderer import Renderer
from Products.ERP5Type import Permissions, PropertySheet, interfaces
from Products.ERP5.Document.MappedValue import MappedValue

from Products.ERP5.mixin.amount_generator import AmountGeneratorMixin
from Products.ERP5.mixin.variated import VariatedMixin
from Products.ERP5.mixin.composition import CompositionMixin
from Products.ERP5Type.XMLObject import XMLObject

class Transformation(MappedValue, AmountGeneratorMixin, VariatedMixin):
    """
      Build of material - contains a list of transformed resources

      Use of default_resource... (to define the variation range,
      to ...)

      XXX Transformation works only for a maximum of 3 variation base category...
      Matrixbox must be rewritten for a clean implementation of n base category

    """
    meta_type = 'ERP5 Transformation'
    portal_type = 'Transformation'

    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.AccessContentsInformation)

    # Declarative properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.CategoryCore
                      , PropertySheet.DublinCore
                      , PropertySheet.VariationRange
                      , PropertySheet.Predicate
                      , PropertySheet.Comment
                      , PropertySheet.Reference
                      , PropertySheet.Version
                      #, PropertySheet.Resource
                      , PropertySheet.TransformedResource
                      , PropertySheet.Path
                      , PropertySheet.Transformation
                      , PropertySheet.Order
                      , PropertySheet.Task
                      )

    # Declarative interfaces
    zope.interface.implements(interfaces.IVariated, 
                              interfaces.IVariationRange,
                              interfaces.IAmountGenerator
                              )

    # Predicate Value implementation
    #   asPredicate takes into account the resource
    # XXX-JPS not Impl.

    def getCellAggregateKey(self, amount_generator_cell):
      """Define a key in order to aggregate amounts at cell level

        Transformed Resource (Transformation)
          key must be None because:
            - quantity and variation are defined in different cells so that the
              user does not need to enter values depending on all axes
            - amount_generator_cell.test should filter only 1 variant
          current key = (acquired resource, acquired variation)

        Assorted Resource (Transformation)
          key = (assorted resource, assorted resource variation)
          usually resource and quantity provided together

        Payroll
          key = (payroll resource, payroll resource variation)

        Tax
          key = (tax resource, tax resource variation)
      """
      if len(amount_generator_cell.contentValues()):
        key = (amount_generator_cell.getRelativeUrl(),)
      else:
        key = (amount_generator_cell.getParentValue().getRelativeUrl(),)
      return key

    # Mapped Value implementation
    #  Transformation itself provides no properties or categories
    def getMappedValuePropertyList(self):
      return ()

    def getMappedValueBaseCategoryList(self):
      return ()

    # Amount Generator Mixin
    def _getGlobalPropertyDict(self, context, amount_list=None, rounding=False):
      """
      No global properties needed
      """
      return {
      }

    def _getAmountPropertyDict(self, amount, amount_list=None, rounding=False):
      """
      Produced amount quantity is needed to initialize transformation
      """
      # XXX 1 is for compatibility
      return {
        'produced_quantity' : amount.getQuantity(1),
      }

    def getBaseApplication(self):
      """
      
      """
      # It is OK to try to acquire
      if getattr(self, '_baseGetBaseApplication', None) is not None:
        result = self._baseGetBaseApplication()
        if result:
          return result
      return 'produced_quantity'

    # IVariationRange and IVariated Implementation
    security.declareProtected(Permissions.AccessContentsInformation,
                              'updateVariationCategoryList')
    def updateVariationCategoryList(self):
      """
        Check if variation category list of the resource has changed and update
        transformation and transformation line
      """
      self.setVariationBaseCategoryList(self.getVariationBaseCategoryList())
      transformation_line_list = self.contentValues()
      for transformation_line in transformation_line_list:
        transformation_line.updateVariationCategoryList()

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getVariationRangeBaseCategoryList')
    def getVariationRangeBaseCategoryList(self):
      """
        Returns possible variation base_category ids of the
        default resource which can be used as variation axis
        in the transformation.
      """
      resource = self.getResourceValue()
      if resource is not None:
        result = resource.getVariationBaseCategoryList()
      else:
        # XXX result = self.getBaseCategoryIds()
        # Why calling this method ?
        # Get a global variable which define a list of variation base category
        result = self.getPortalVariationBaseCategoryList()
      return result

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getVariationRangeBaseCategoryItemList')
    def getVariationRangeBaseCategoryItemList(self, display_id='getTitleOrId', **kw):
        """
          Returns possible variations of the transformation
          as a list of tuples (id, title). This is mostly
          useful in ERP5Form instances to generate selection
          menus.
        """
        return self.portal_categories.getItemList(
                              self.getVariationRangeBaseCategoryList(),
                              display_id=display_id, **kw)

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getVariationRangeCategoryItemList')
    def getVariationRangeCategoryItemList(self, base_category_list=(),
                                          omit_individual_variation=0,
                                          display_base_category=1, **kw):
        """
          Returns possible variation category values for the
          transformation according to the default resource.
          Possible category values are provided as a list of
          tuples (id, title). This is mostly
          useful in ERP5Form instances to generate selection
          menus.
          User may want to define generic transformation without
          any defined resource.
        """
        if base_category_list is ():
          base_category_list = self.getVariationBaseCategoryList()

        resource = self.getResourceValue()
        if resource is not None:
          result = resource.getVariationCategoryItemList(
                        base_category_list=base_category_list,
                        omit_individual_variation=omit_individual_variation,
                        display_base_category=display_base_category,**kw)
        else:
          # No resource is define on transformation. 
          # We want to display content of base categories
          result = self.portal_categories.getCategoryChildTitleItemList(
                         base_category_list, base=1, display_none_category=0)
        return result

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getVariationCategoryItemList')
    def getVariationCategoryItemList(self, base_category_list=(), base=1,
                                     display_id='title',
                                     current_category=None,
                                     **kw):
      """
        Returns the list of possible variations
        XXX Copied and modified from Variated
        Result is left display.
      """
      variation_category_item_list = []
      if base_category_list == ():
        base_category_list = self.getVariationBaseCategoryList()

      category_renderer = Renderer(
                             is_right_display=0,
                             display_none_category=0, base=base,
                             current_category=current_category,
                             display_id='logical_path', **kw)

      for base_category in base_category_list:
        variation_category_list = self.getVariationCategoryList(
                                            base_category_list=[base_category])

        category_list = []
        object_list = []
        for variation_category in variation_category_list:
          resource = self.portal_categories.resolveCategory(variation_category)
          if resource.getPortalType() == 'Category':
            category_list.append(resource)
          else:
            object_list.append(resource)

        variation_category_item_list.extend(category_renderer.\
                                              render(category_list))

        variation_category_item_list.extend(Renderer(
                               is_right_display=0,
                               base_category=base_category,
                               display_none_category=0, base=base,
                               current_category=current_category,
                               display_id=display_id,**kw).\
                                                 render(object_list))
      return variation_category_item_list
