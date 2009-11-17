##############################################################################
#
# Copyright (c) 2008 Nexedi SA and Contributors. All Rights Reserved.
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

from AccessControl.ZopeGuards import guarded_getattr
from Products.ERP5Type import Permissions, PropertySheet, Constraint, interfaces
from Products.ERP5.Document.BudgetVariation import BudgetVariation


class CategoryBudgetVariation(BudgetVariation):
  """ A budget variation based on a category
  """
  # Default Properties
  property_sheets = ( PropertySheet.Base
                    , PropertySheet.XMLObject
                    , PropertySheet.SimpleItem
                    , PropertySheet.CategoryCore
                    , PropertySheet.SortIndex
                    , PropertySheet.Path
                    , PropertySheet.Predicate
                    , PropertySheet.BudgetVariation
                    )

  # CMF Type Definition
  meta_type = 'ERP5 Category Budget Variation'
  portal_type = 'Category Budget Variation'
  add_permission = Permissions.AddPortalContent

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  # zope.interface.implements(BudgetVariation, )

  def asBudgetPredicate(self):
    """This budget variation in a predicate
    """

  def getCellRangeForBudgetLine(self, budget_line, matrixbox=0):
    """The cell range added by this variation
    """
    item_list = self.getBudgetLineVariationRangeCategoryList(budget_line)
    variation_category_list = budget_line.getVariationCategoryList()
    if matrixbox:
      return [[(i[1], i[0]) for i in item_list if i[1] in variation_category_list]]
    return [[i[1] for i in item_list if i[1] in variation_category_list]]

  def getInventoryQueryDict(self, budget_cell):
    """ Query dict to pass to simulation query
    """
    axis = self.getInventoryAxis()
    if not axis:
      return dict()
    base_category = self.getProperty('variation_base_category')
    if not base_category:
      return dict()
    for criterion_category in budget_cell.getMembershipCriterionCategoryList():
      if '/' not in criterion_category: # safe ...
        continue
      criterion_base_category, category_url = criterion_category.split('/', 1)
      if criterion_base_category == base_category:
        category_uid = self.getPortalObject().portal_categories\
                                .getCategoryUid(criterion_category)
        # Different possible inventory axis here
        if axis == 'movement':
          return {'default_%s_uid' % base_category: category_uid}
        if axis in ('node', 'section', 'payment', 'function', 'project',
                    'mirror_section', 'mirror_node' ):
          return {'%s_uid' % axis: category_uid}
        return {axis: criterion_category}
    return dict()

  def getBudgetVariationRangeCategoryList(self, context):
    """Returns the Variation Range Category List that can be applied to this
    budget.
    """
    base_category = self.getProperty('variation_base_category')
    if not base_category:
      return []

    portal = self.getPortalObject()
    item_list_method = portal.portal_preferences.getPreference(
                          'preferred_category_child_item_list_method_id',
                          'getCategoryChildCompactLogicalPathItemList')
    
    return getattr(portal.portal_categories._getOb(base_category),
                        item_list_method)(
                                base=1,
                                local_sort_id=('int_index',
                                               'translated_title'),
                                checked_permission='View')
    

  def getBudgetLineVariationRangeCategoryList(self, budget_line):
    """Returns the Variation Range Category List that can be applied to this
    budget line.
    """
    base_category = self.getProperty('variation_base_category')
    if not base_category:
      return []

    portal = self.getPortalObject()
    item_list_method = portal.portal_preferences.getPreference(
                          'preferred_category_child_item_list_method_id',
                          'getCategoryChildCompactLogicalPathItemList')
    
    item_list_method_parameter_dict = dict(
          base=1,
          local_sort_id=('int_index', 'translated_title'),
          checked_permission='View')

    # If this category is defined on budget level, starts at this level
    budget = budget_line.getParentValue()
    if base_category in budget.getVariationBaseCategoryList():
      for budget_variation_category in budget.getVariationCategoryList():
        if budget_variation_category.split('/')[0] == base_category:
          base_category = budget_variation_category
          item_list_method_parameter_dict['is_self_excluded'] = False
          break
      
    return getattr(portal.portal_categories.unrestrictedTraverse(base_category),
                        item_list_method)(**item_list_method_parameter_dict)

  def initializeBudgetLine(self, budget_line):
    """Initialize a budget line
    """
    budget_line_variation_category_list =\
       list(budget_line.getVariationBaseCategoryList() or [])
    budget_line_membership_criterion_base_category_list =\
       list(budget_line.getMembershipCriterionBaseCategoryList() or [])
    base_category = self.getProperty('variation_base_category')
    if base_category:
      budget_line_variation_category_list.append(base_category)
      budget_line.setVariationBaseCategoryList(
              budget_line_variation_category_list)
    if self.isMemberOf('budget_variation/budget_line'):
      budget_line_membership_criterion_base_category_list.append(base_category)
      budget_line.setMembershipCriterionBaseCategoryList(
          budget_line_membership_criterion_base_category_list)

  def initializeBudget(self, budget):
    """Initialize a budget.
    """
    budget_variation_base_category_list =\
       list(budget.getVariationBaseCategoryList() or [])
    budget_membership_criterion_base_category_list =\
       list(budget.getMembershipCriterionBaseCategoryList() or [])
    base_category = self.getProperty('variation_base_category')
    if base_category:
      if base_category not in budget_variation_base_category_list:
        budget_variation_base_category_list.append(base_category)
      if base_category not in budget_membership_criterion_base_category_list:
        budget_membership_criterion_base_category_list.append(base_category)
      budget.setVariationBaseCategoryList(
              budget_variation_base_category_list)
      budget.setMembershipCriterionBaseCategoryList(
              budget_membership_criterion_base_category_list)


