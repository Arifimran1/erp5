'''
RULES

Single arguments:
    - arg:value translates into arg='value' in query
    - quotes are cleared
    - if value contains spaces, punctuation or anything else it has to be put in quotes
    - file is source_reference (original file name)
    - language, version, reference

Multiple arguments:
    - arg:xxx works the same way
    - arg:(xxx,yyy) ORs both (do not put space after comma)
    - arg:all translates into empty tuple, which implies all available values
    - state (simulation_state), type (portal_type)

Everything else is treated as SearchableText
'''


import re

# parsing defined here
simulation_states=()
r=re.compile('(\w+:"[^"]+"|\w+:[\(\),\w/\-.]+)')
filetyper=lambda s:('source_reference','%%.%s' % s)
filestripper=lambda s: ('source_reference',s.replace('"',''))
#addarchived=lambda s: ('simulation_state',simulation_states+('archived',))
state=lambda s:('simulation_state',parsestates(s))
type=lambda s:('portal_type',parsestates(s))
paramsmap=dict(file=filestripper,type=type,reference='reference',filetype=filetyper,state=state,\
        language='language',version='version')

def parsestates(s):
    if s=='all':
        return ()
    if s[0]=='(' and s[-1]==')':
        return [i for i in s[1:-1].split(',') if i!='']
    return s.replace('"','').replace("'","")

def analyze(params):
    params['SearchableText']=''
    params['simulation_state']=simulation_states
    def cutter(s):
        ss=s.split(':')
        if len(ss)==1:
            params['SearchableText']+=ss[0]
        if len(ss)==2:
            try:
                ps=paramsmap.get(ss[0])(ss[1])
                params[ps[0]]=ps[1]
            except TypeError:
                if paramsmap.has_key(ss[0]):
                    params[paramsmap.get(ss[0])]=ss[1]
                else:
                    params[ss[0]]=ss[1]
    return cutter

def parseSearchString(searchstring):
    params={}
    l=r.split(searchstring)
    print l
    map(analyze(params),l)
    params['SearchableText']=params['SearchableText'].strip()
    return params

if __name__=='__main__':
    #searchstring='byle cisnie zego file:"ble ble.doc" filetype:doc type:Text poza tym reference:abc-def'
    searchstring='byle "cisnie zego" state:draft file:"ble ble.doc" type:"Web Site" poza tym reference:abc-def dupa:kwas/zbita'
    print parseSearchString(searchstring)
