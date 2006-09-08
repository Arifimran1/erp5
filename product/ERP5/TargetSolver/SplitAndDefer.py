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

from CopyToTarget import CopyToTarget
from zLOG import LOG

class SplitAndDefer(CopyToTarget):
  """
    Split and defer simulation movement.

    Many 'deliverable movements' are created in the Simulation and
    may need to be delivered later. Solver accumulates such movements
    in the solving process and creates a new delivery

    This only works when some movements can not be delivered 
    (excessive qty is not covered)
  """

  def solve(self, simulation_movement):
    """
      Split a simulation movement and accumulate
    """
    movement_quantity = simulation_movement.getQuantity()
    delivery_quantity = simulation_movement.getDeliveryQuantity()
    new_movement_quantity = delivery_quantity * simulation_movement.getDeliveryRatio()

    if movement_quantity > new_movement_quantity:
      split_index = 0
      new_id = "%s_split_%s" % (simulation_movement.getId(), split_index)
      while getattr(simulation_movement.aq_parent, new_id, None) is not None:
        split_index += 1
        new_id = "%s_split_%s" % (simulation_movement.getId(), split_index)
      # Adopt different dates for defferred movements
      new_movement = simulation_movement.aq_parent.newContent(
                        portal_type="Simulation Movement",
                        id=new_id,
                        efficiency=simulation_movement.getEfficiency(),
                        start_date=self.start_date,
                        stop_date=self.stop_date,
                        order=simulation_movement.getOrder(),
                        deliverable=simulation_movement.isDeliverable(),
                        quantity=movement_quantity-new_movement_quantity,
                        price = simulation_movement.getPrice(),
                        source = simulation_movement.getSource(),
                        destination = simulation_movement.getDestination(),
                        source_section = simulation_movement.getSourceSection(),
                        resource = simulation_movement.getResource(),
                        destination_section = simulation_movement.getDestinationSection(),
                        activate_kw=self.activate_kw,
                        **self.additional_parameters
      )
      new_movement.activate(**self.additional_parameters).expand()
      # adopt new quantity on original simulation movement
      simulation_movement.edit(quantity=new_movement_quantity)
    simulation_movement._v_activate_kw = self.activate_kw
    simulation_movement.activate(**self.additional_parameters).expand()

    # SplitAndDefer solves the divergence at the current level, no need to
    # backtrack.
