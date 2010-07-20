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
from Products.ERP5Type import Permissions, PropertySheet
from Products.ERP5.Document.BudgetVariation import BudgetVariation
from Products.ZSQLCatalog.SQLCatalog import Query, NegatedQuery
from Products.ERP5Type.Message import translateString


class VirtualNode(object):
  """A Virtual Node for all Other Nodes.

  This virtual document can be used in budget variations.
  """
  __allow_access_to_unprotected_subobjects__ = 1
  def __init__(self, relative_url):
    """The Virtual Node will use the relative URL of the budget line for
    memberships.
    """
    self.relative_url = relative_url

  def getTitle(self):
    return str(translateString('All Others'))

  def getRelativeUrl(self):
    return self.relative_url

  def getUid(self):
    return -1L


class NodeBudgetVariation(BudgetVariation):
  """ A budget variation for node

  A script will return the list of possible nodes, or they will be configured
  explicitly on the budget variation. It is also possible to include a virtual
  node for all others not selected nodes.
  """
  # Default Properties
  property_sheets = ( PropertySheet.Base
                    , PropertySheet.XMLObject
                    , PropertySheet.SimpleItem
                    , PropertySheet.SortIndex
                    , PropertySheet.Path
                    , PropertySheet.Predicate
                    , PropertySheet.BudgetVariation
                    )

  # CMF Type Definition
  meta_type = 'ERP5 Node Budget Variation'
  portal_type = 'Node Budget Variation'
  add_permission = Permissions.AddPortalContent

  # Declarative security
  security = ClassSecurityInfo()
  security.declareObjectProtected(Permissions.AccessContentsInformation)

  # zope.interface.implements(BudgetVariation, )

  def asBudgetPredicate(self):
    """This budget variation in a predicate
    """

  def _getNodeList(self, context):
    """Returns the list of possible nodes
    """
    node_select_method_id = self.getProperty('node_select_method_id')
    if node_select_method_id:
      return guarded_getattr(context, node_select_method_id)()
    # no script defined, used the explicitly selected values
    if self.getProperty('include_virtual_other_node'):
      return self.getAggregateValueList() + [
                    VirtualNode(context.getRelativeUrl()), ]
    return self.getAggregateValueList()

  def _getNodeTitle(self, node):
    """Returns the title of a node
    """
    node_title_method_id = self.getProperty('node_title_method_id', 'getTitle')
    return guarded_getattr(node, node_title_method_id)()

  def getCellRangeForBudgetLine(self, budget_line, matrixbox=0):
    """The cell range added by this variation
    """
    base_category = self.getProperty('variation_base_category')
    prefix = ''
    if base_category:
      prefix = '%s/' % base_category

    node_item_list = [('%s%s' % (prefix, node.getRelativeUrl()),
                       self._getNodeTitle(node))
                           for node in self._getNodeList(budget_line)]
    variation_category_list = budget_line.getVariationCategoryList()
    if matrixbox:
      return [[i for i in node_item_list if i[0] in variation_category_list]]
    return [[i[0] for i in node_item_list if i[0] in variation_category_list]]

  def getInventoryQueryDict(self, budget_cell):
    """ Query dict to pass to simulation query
    """
    axis = self.getInventoryAxis()
    if not axis:
      return dict()
    base_category = self.getProperty('variation_base_category')
    if not base_category:
      return dict()
    budget_line = budget_cell.getParentValue()
    portal = self.getPortalObject()
    portal_categories = portal.portal_categories
    for criterion_category in budget_cell.getMembershipCriterionCategoryList():
      if '/' not in criterion_category: # safe ...
        continue
      criterion_base_category, node_url = criterion_category.split('/', 1)
      if criterion_base_category == base_category:
        if axis == 'movement':
          axis = 'default_%s' % base_category
        axis = '%s_uid' % axis
        if node_url == budget_line.getRelativeUrl():
          # This is the "All Other" virtual node
          other_uid_list = []
          for node in self._getNodeList(budget_line):
            if '%s/%s' % (base_category, node.getRelativeUrl()) in\
                                    budget_line.getVariationCategoryList():
              other_uid_list.append(node.getUid())
          return {axis: NegatedQuery(Query(**{axis: other_uid_list}))}
        return {axis:
                portal_categories.getCategoryValue(node_url, base_category=criterion_base_category).getUid()}

    return dict()


  def getBudgetLineVariationRangeCategoryList(self, budget_line):
    """Returns the Variation Range Category List that can be applied to this
    budget line.
    """
    base_category = self.getProperty('variation_base_category')
    prefix = ''
    if base_category:
      prefix = '%s/' % base_category
    return [(self._getNodeTitle(node), '%s%s' % (prefix, node.getRelativeUrl()))
                for node in self._getNodeList(budget_line)]

  def getBudgetVariationRangeCategoryList(self, budget):
    """Returns the Variation Range Category Listhat can be applied to this
    budget.
    """
    base_category = self.getProperty('variation_base_category')
    prefix = ''
    if base_category:
      prefix = '%s/' % base_category
    return [(self._getNodeTitle(node), '%s%s' % (prefix, node.getRelativeUrl()))
                for node in self._getNodeList(budget)]

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

