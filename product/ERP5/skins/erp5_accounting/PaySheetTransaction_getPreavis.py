## Script (Python) "PaySheetTransaction_getPreavis"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# D�finition des pr�avis selon le temps dans l'entreprise (en jours)
seuils = [ { 'limite':30 , 'preavis':'1 jour' },    # 1er mois d'essai
           { 'limite':60 , 'preavis':'1 semaine' }, # 2e mois d'essai
           { 'limite':730, 'preavis':'1 mois' },    # 2 premi�res ann�es
           { 'limite':0,   'preavis':'2 mois' } ]   # Apr�s les 2 premi�res ann�es


paysheet        = context.getObject()
employee_object = paysheet.getDestinationSectionValue()


# R�cup�ration de l'entreprise actuelle
currentOrg = None
if hasattr(employee_object,"default_career"):
  currentOrg = employee_object["default_career"].getSubordinationValue()

if currentOrg == None:
  return '???'
  
# Calcul du temps total dans cette entreprise
totalTime = 0
steps = employee_object.contentValues()
for step in steps:
  if step.getPortalType() == "Career" and step.getId() != "default_career":
    if step.getSubordinationValue() == currentOrg:
      difference = step.getStopDate() - step.getStartDate()
      if difference > 0:
        totalTime = totalTime + difference

totalTime = int( totalTime + (DateTime() - employee_object["default_career"].getStartDate()) )


# D�termination du pr�avis
for i in range(len(seuils)):
  if i < len(seuils)-1:
    if seuils[i]['limite'] >= totalTime:
      return seuils[i]['preavis']
  else:
    return seuils[i]['preavis']
