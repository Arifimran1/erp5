##############################################################################
#
# Copyright (c) 2002, 2005 Nexedi SARL and Contributors. All Rights Reserved.
#                    Jean-Paul Smets-Solanes <jp@nexedi.com>
#                    Romain Courteaud <romain@nexedi.com>
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
from Acquisition import aq_base, aq_parent, aq_inner, aq_acquire
from Products.CMFCore.utils import getToolByName

from Products.ERP5Type import Permissions, PropertySheet, Constraint, Interface
from Products.ERP5.Document.Rule import Rule
from Products.ERP5.Document.TransformationSourcingRule import\
                                            TransformationSourcingRuleMixin

from zLOG import LOG

class TransformationRule(Rule):
    """
      Order Rule object make sure an Order in the similation
      is consistent with the real order
    """
    # CMF Type Definition
    meta_type = 'ERP5 Transformation Rule'
    portal_type = 'Transformation Rule'
    # Declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(Permissions.View)
    # Default Properties
    property_sheets = ( PropertySheet.Base
                      , PropertySheet.XMLObject
                      , PropertySheet.CategoryCore
                      , PropertySheet.DublinCore
                      )
    # Class variable 
    simulation_movement_portal_type = "Simulation Movement"

    security.declareProtected(Permissions.AccessContentsInformation, 'test')
    def test(self, movement):
      """
        Tests if the rule (still) applies
      """
      # Test if we must transform
      # The test should actually be based on nodes, paths
      # and capacities, which is not possible now
      result = 1
      # Only apply to Order applied rule
      root_applied_rule = movement.getRootAppliedRule()
      root_rule = root_applied_rule.getSpecialiseValue()
      order = root_applied_rule.getCausalityValue()
      root_movement = movement.getRootSimulationMovement()
      # Test movement
      if (root_rule is None) or\
         (root_rule.getPortalType() != "Production Order Rule") or\
         (order is None) or\
         (movement.getResourceValue() is None) or\
         (movement.getSourceValue() is None) or\
         (movement.getResourceValue() != root_movement.getResourceValue()):
         # We only produced what is asked on the Production Order
           result = 0
      else:
        supply_chain = self.getSupplyChain(movement.getParent())
        parent_supply_link = self.getCurrentSupplyLink(movement)
        current_tranfo_link_list = supply_chain.\
                       getPreviousProductionSupplyLinkList(parent_supply_link)
        length = len(current_tranfo_link_list)
        if length == 0:
          result = 0
        elif length > 1:
          result = 0
          # XXX FIXME: implementation needed
          raise "TransformationRuleError",\
                "TransformationRule not able to use multiple SupplyLink."
      return result

    # Simulation workflow
    security.declareProtected(Permissions.ModifyPortalContent, 'expand')
    def expand(self, applied_rule, **kw):
      """
        Expands the current movement downward.
        -> new status -> expanded
        An applied rule can be expanded only if its parent movement
        is expanded.
      """
      parent_movement = applied_rule.getParent()
      # Get production node and production section
      production = parent_movement.getSource()
      production_section = parent_movement.getSourceSection()
      # Get the current supply link used to calculate consumed resource
      # The current supply link is calculated from the parent AppliedRule.
      supply_chain = self.getSupplyChain(parent_movement.getParent())
      parent_supply_link = self.getCurrentSupplyLink(parent_movement)
      current_supply_link_list = supply_chain.\
                     getPreviousProductionSupplyLinkList(parent_supply_link)
      if len(current_supply_link_list) != 1:
        # We shall no pass here.
        # The test method returned a wrong value !
        raise "TransformationRuleError",\
              "Expand must not be called on %r" %\
                  applied_rule.getRelativeUrl()
      else:
        current_supply_link = current_supply_link_list[0]
        # Generate produced movement
        movement_dict = self._expandProducedResource(applied_rule, 
                                                     production,
                                                     production_section,
                                                     current_supply_link)
        # Generate consumed movement
        consumed_mvt_dict = self._expandConsumedResource(applied_rule, 
                                                         production,
                                                         production_section,
                                                         current_supply_link)
        movement_dict.update(consumed_mvt_dict)
        # Finally, build movement
        self._buildMovementList(applied_rule, movement_dict)
      # Expand each movement created
      Rule.expand(self, applied_rule, **kw)

    def _expandProducedResource(self, applied_rule, production,
                                production_section, current_supply_link):
      """
        Produced resource.
        Create a movement for the resource produced by the transformation.
        Only one produced movement can be created.
      """
      parent_movement = applied_rule.getParent()
      stop_date = parent_movement.getStartDate()
      produced_movement_dict = {
        'pr': {
          "resource": parent_movement.getResource(),
          # XXX what is lost quantity ?
          "quantity": parent_movement.getQuantity(),# + lost_quantity,
          "quantity_unit": parent_movement.getQuantityUnit(),
          "variation_category_list":\
                        parent_movement.getVariationCategoryList(),
          "source_list": (),
          "source_section_list": (),
          "destination": production,
          "destination_section": production_section,
          "deliverable": 1,
          'start_date': current_supply_link.getStartDate(stop_date),
          'stop_date': stop_date,
          'causality_value': current_supply_link,
        }
      }
      return produced_movement_dict

    def _expandConsumedResource(self, applied_rule, production,
                                production_section, current_supply_link):
      """
        Consumed resource.
        Create a movement for each resource consumed by the transformation,
        and for the previous variation of the produced resource.
      """
      # Calculate all consumed resource
      # Store each value in a dictionnary before created them.
      # { movement_id: {property_name: property_value,} ,}
      consumed_movement_dict = {}
      parent_movement = applied_rule.getParent()
      supply_chain = self.getSupplyChain(parent_movement.getParent())
      # Consumed previous variation
      previous_variation_dict = self._expandConsumedPreviousVariation(
                                                        applied_rule, 
                                                        production, 
                                                        production_section,
                                                        supply_chain,
                                                        current_supply_link)
      consumed_movement_dict.update(previous_variation_dict)
      # Consumed raw materials
      raw_material_dict = self._expandConsumedRawMaterials(
                                                        applied_rule, 
                                                        production, 
                                                        production_section,
                                                        supply_chain,
                                                        current_supply_link)
      consumed_movement_dict.update(raw_material_dict)
      return consumed_movement_dict

    def _expandConsumedPreviousVariation(self, applied_rule, production,
                                         production_section, supply_chain,
                                         current_supply_link):
      """
        Create a movement for the previous variation of the produced resource.
      """
      id_count = 1
      consumed_movement_dict = {}
      parent_movement = applied_rule.getParent()
      # Calculate the variation category list of parent movement
      base_category_list = parent_movement.getVariationBaseCategoryList()
      if "industrial_phase" in base_category_list:
        # We do not want to get the industrial phase variation
        base_category_list.remove("industrial_phase")
      category_list = parent_movement.getVariationCategoryList(
                                  base_category_list=base_category_list)
      # Calculate the previous variation
      for previous_supply_link in supply_chain.\
            getPreviousSupplyLinkList(current_supply_link):
        previous_ind_phase_list = supply_chain.\
            getPreviousProductionIndustrialPhaseList(previous_supply_link,
                                                     all=1)
        if previous_ind_phase_list != []:
          # Industrial phase is a category
          ind_phase_list = [x.getCategoryRelativeUrl() for x in \
                            previous_ind_phase_list]
          consumed_mvt_id = "%s_%s" % ("mr", id_count)
          id_count += 1
          stop_date = parent_movement.getStartDate()
          consumed_movement_dict[consumed_mvt_id] = {
            'start_date': current_supply_link.getStartDate(stop_date),
            'stop_date': stop_date,
            "resource": parent_movement.getResource(),
            # XXX Is the quantity value correct ?
            "quantity": parent_movement.getQuantity(),
            "quantity_unit": parent_movement.getQuantityUnit(),
            "destination_list": (),
            "destination_section_list": (),
            "source": production,
            "source_section": production_section,
            "deliverable": 1,
            "variation_category_list": category_list,
            'causality_value': current_supply_link,
            "industrial_phase_list": ind_phase_list}
      return consumed_movement_dict

    def _expandConsumedRawMaterials(self, applied_rule, production,
                                    production_section, supply_chain,
                                    current_supply_link):
      """
        Create a movement for each resource consumed by the transformation,
      """
      parent_movement = applied_rule.getParent()
      # Calculate the context for getAggregatedAmountList
      base_category_list = parent_movement.getVariationBaseCategoryList()
      if "industrial_phase" in base_category_list:
        # We do not want to get the industrial phase variation
        base_category_list.remove("industrial_phase")
      category_list = parent_movement.getVariationCategoryList(
                                  base_category_list=base_category_list)
      # Get the transformation to use
      production_order_movement = applied_rule.getRootSimulationMovement().\
                                                     getOrderValue()
      # XXX Acquisition can be use instead
      parent_uid = production_order_movement.getParent().getUid()
      explanation_uid = production_order_movement.getExplanationUid()
      if parent_uid == explanation_uid:
        production_order_line = production_order_movement
      else:
        production_order_line = production_order_movement.getParent()
      line_transformation = production_order_line.objectValues(portal_type=self.getPortalTransformationTypeList())
      if len(line_transformation)==1:
        transformation = line_transformation[0]
      else:
        transformation = production_order_line.getSpecialiseValue(
                           portal_type=self.getPortalTransformationTypeList())
      # Generate the fake context 
      tmp_context = parent_movement.asContext(
                   context=parent_movement, 
                   REQUEST={'categories':category_list})
      # Calculate the industrial phase list
      previous_ind_phase_list = supply_chain.\
          getPreviousPackingListIndustrialPhaseList(current_supply_link)
      ind_phase_id_list = [x.getId() for x in previous_ind_phase_list]
      # Call getAggregatedAmountList
      # XXX expand failed if transformation is not defined.
      # Do we need to catch the exception ?
      amount_list = transformation.getAggregatedAmountList(
                   tmp_context,
                   ind_phase_id_list=ind_phase_id_list)
      # Add entries in the consumed_movement_dict
      consumed_movement_dict = {}
      for amount in amount_list:
        consumed_mvt_id = "%s_%s" % ("cr", amount.getId())
        stop_date = parent_movement.getStartDate()
        consumed_movement_dict[consumed_mvt_id] = {
          'start_date': current_supply_link.getStartDate(stop_date),
          'stop_date': stop_date,
          "resource": amount.getResource(),
          "variation_category_list":\
                        amount.getVariationCategoryList(),
          "quantity": amount.getQuantity() * parent_movement.getQuantity(),
          "quantity_unit": amount.getQuantityUnit(),
          "destination_list": (),
          "destination_section_list": (),
          "source": production,
          "source_section": production_section,
          "deliverable": 1,
          'causality_value': current_supply_link,
        }
      return consumed_movement_dict

    security.declareProtected(Permissions.ModifyPortalContent, 'solve')
    def solve(self, applied_rule, solution_list):
      """
        Solve inconsitency according to a certain number of solutions
        templates. This updates the

        -> new status -> solved

        This applies a solution to an applied rule. Once
        the solution is applied, the parent movement is checked.
        If it does not diverge, the rule is reexpanded. If not,
        diverge is called on the parent movement.
      """

    security.declareProtected(Permissions.ModifyPortalContent, 'diverge')
    def diverge(self, applied_rule):
      """
        -> new status -> diverged

        This basically sets the rule to "diverged"
        and blocks expansion process
      """

    # Solvers
    security.declareProtected(Permissions.View, 'isDivergent')
    def isDivergent(self, applied_rule):
      """
        Returns 1 if divergent rule
      """

    security.declareProtected(Permissions.View, 'getDivergenceList')
    def getDivergenceList(self, applied_rule):
      """
        Returns a list Divergence descriptors
      """

    security.declareProtected(Permissions.View, 'getSolverList')
    def getSolverList(self, applied_rule):
      """
        Returns a list Divergence solvers
      """
    # Deliverability / orderability
    def isDeliverable(self, m):
      return 1
    def isOrderable(self, m):
      return 0

from Products.ERP5Type.Utils import monkeyPatch
monkeyPatch(TransformationSourcingRuleMixin, TransformationRule)
