## Script (Python) "object_action_list"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=selection_name='', max_nb=0
##title=
##
# Retourne une liste d'objet correspondant � un selection
# si appel� sur un ERP5 Folder
# Retourne une liste � un seul objet (context)
# si appel� sur autre chose
# utile pour effectuer des actions (impression,...)
# que l'on souhaite appeler depuis une liste ou depuis un formulaire d�taill�

object_list = []
request = context.REQUEST
if context.getMetaType() == 'ERP5 Folder' :
  selection = context.portal_selections.getSelectionFor(selection_name,REQUEST=context.REQUEST)
  object_list = map((lambda x:x.getObject()),selection(context=context))
else :
  object_list.append(context)

# limitation du nombre d'objets en sortie
if max_nb <> 0 :
  if len(object_list) > max_nb :
    object_list = modele_list[0:max_nb]

return object_list
