# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2002 Coramy SAS and Contributors. All Rights Reserved.
#                    Thierry_Faucher <Thierry_Faucher@coramy.com>
# Copyright (c) 2004-2009 Nexedi SA and Contributors. All Rights Reserved.
#                    Romain Courteaud <romain@nexedi.com>
#                    Łukasz Nowak <luke@nexedi.com>
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

import zope.interface
from AccessControl import ClassSecurityInfo

from Products.ERP5Type import Permissions, PropertySheet, interfaces
from Products.ERP5Type.XMLObject import XMLObject

from Products.ERP5.Variated import Variated

from Products.ERP5.Document.Predicate import Predicate

from Products.CMFCategory.Renderer import Renderer
from Products.ERP5.AggregatedAmountList import AggregatedAmountList

from zLOG import LOG, WARNING

class Transformation(XMLObject, Predicate, Variated):
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
                      )

    # Declarative interfaces
    zope.interface.implements(interfaces.IVariated, 
                              interfaces.IAmountGenerator
                              )



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
                              '_setVariationBaseCategoryList')
    def _setVariationBaseCategoryList(self, value):
      """
        Define the possible base categories
      """
#      XXX TransformedResource works only for a maximum of 3 variation base category...
#      Matrixbox must be rewrite for a clean implementation of n base category
      if len(value) <= 3:
        self._baseSetVariationBaseCategoryList(value)
      else:
        raise MoreThan3VariationBaseCategory

      # create relations between resource variation and transformation
      self._setVariationCategoryList( self.getVariationRangeCategoryList() )

    security.declareProtected(Permissions.AccessContentsInformation,
                              'setVariationBaseCategoryList')
    def setVariationBaseCategoryList(self, value):
      """
        Define the possible base categories and reindex object
      """
      self._setVariationBaseCategoryList(value)
      self.reindexObject()

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

    def updateAggregatedAmountList(self, context, **kw):
      raise NotImplementedError, 'need?'

    security.declareProtected(Permissions.AccessContentsInformation,
                              'getAggregatedAmountList')
    def getAggregatedAmountList(self, context=None, REQUEST=None,
                                trade_phase_list=None,
                                # obsolete, use trade_phase_list instead
                                ind_phase_url_list=None,
                                rejected_resource_uid_list=None,
                                **kw):
      """
        getAggregatedAmountList returns an AggregatedAmountList which
        can be used either to do some calculation (ex. price, BOM)
        or to display a detailed view of a transformation.
      """
      context = self.asContext(context=context, REQUEST=REQUEST, **kw)

      # A list of functions taking a transformation_line as sole argument
      # and returning True iif the line should be kept in the result
      filter_list = []

      # Get only lines related to a precise trade_phase
      if trade_phase_list is not None:
        def trade_phase_filter(line):
          return line.getTradePhase() in trade_phase_list

        filter_list.append(trade_phase_filter)

      # Get only lines related to a precise industrial_phase
      if ind_phase_url_list is not None:
        LOG("Transformation", WARNING, "ind_phase_list is obsolete")
        def industrial_phase_filter(line):
          ind_ph = line.getIndustrialPhaseValue()
          if ind_ph is not None:
            return ind_ph.getRelativeUrl() in ind_phase_url_list
          return False

        filter_list.append(industrial_phase_filter)

      # Filter lines with resource we do not want to see
      if rejected_resource_uid_list is not None:
        def rejected_uid_filter(line):
          return line.getResourceUid() not in rejected_resource_uid_list

        filter_list.append(rejected_uid_filter)

      def line_is_included(line):
        # XXX > 2.5 : all(f(line) for f in filter_list)
        for filterr in filter_list:
          if not filterr(line):
            return False
        return True

      # First we need to get the list of transformations which this
      # transformation depends on
      # At this moment, we only consider 1 dependency
      template_transformation_list = self.getSpecialiseValueList()

      # Browse all involved transformations and create one line per
      # line of transformation
      # Currently, we do not consider abstractions, we just add
      # whatever we find in all transformations
      result = AggregatedAmountList()
      for transformation in ([self] + template_transformation_list):
        for transformation_line in transformation.objectValues():
          # Browse each transformed or assorted resource of the current
          # transformation
          if line_is_included(transformation_line):
            try:
              line_result = transformation_line.getAggregatedAmountList(context)
            except KeyError:
              # KeyError is raised by TransformedResource.getAggregatedAmountList
              # in case of misconfiguration of a Cell.
              # Just ignore the line
              pass
            else:
              result.extend(line_result)

      return result
