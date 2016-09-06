production_order_line = state_change['object']
portal = production_order_line.getPortalObject()

transformation = production_order_line.getSpecialiseValue(
  portal_type=portal.getPortalTransformationTypeList())
if transformation is None:
  portal = production_order_line.getPortalObject()
  resource_uid = production_order_line.getResourceUid()
  if resource_uid:
    transformation_list = portal.portal_catalog(
      portal_type=portal.getPortalTransformationTypeList(),
      validation_state="!=invalidated",
      default_resource_uid=resource_uid)
    if len(transformation_list) >= 1:
      transformation = transformation_list[0].getRelativeUrl()
      production_order_line.setSpecialise(transformation)
