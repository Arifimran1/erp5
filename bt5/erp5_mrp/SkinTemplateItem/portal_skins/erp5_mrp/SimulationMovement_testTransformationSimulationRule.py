specialise_list = context.getSpecialiseValueList(portal_type="Transformation")
if  (len(specialise_list) == 1 and
     context.getResource() == specialise_list[0].getResource()):
  parent = context.getParentValue()
  parent_specialise_portal_type = parent.getSpecialiseValue().getPortalType()
  # Case Manufacturing Order at the root producing a Manufacturing Execution
  if (parent_specialise_portal_type == "Order Root Simulation Rule" \
        and parent.getCausalityValue().getPortalType() == "Manufacturing Order"):
    return True
  # Case Manufacturing Order is generated by Simulation
  if parent_specialise_portal_type == "Production Simulation Rule":
    movement = context.getDeliveryValue()
    return movement is not None and movement.getPortalType() in (
      "Manufacturing Order Line", "Manufacturing Order Cell")
return False
