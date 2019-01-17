from constants import NRC_BASE_URL, CONTENT_SEARCH
import requests
from xml.etree import ElementTree

class Payload(object):
    '''A group of General Parameters that will make up a payload for GET request.'''
    def __init__(self, q, tab, qn = None, s = None, so = None):
        self._q = q.replace(" ","")
        self._tab = tab
        self._qn = qn
        self._s = s
        self._so = so

    def generate_payload(self):
        return {'q': self._q,
                'tab': self._tab,
                'qn': self._qn,
                's' : self._s,
                'so' : self._so }

#class GeneralParameter(object):
#    '''General  parameters that define the scope and sorting criteria for the result set'''
    ## q, tab, qn, s, so
#    def __init__(self, name, value):
#        self._name = name,
#        self._value = value

## q, tab, qn, s, so

q = '''(mode:sections,sections:(filters:(public-library:!t),properties_search:!(!('$title',infolder,'Palo+Verde',''))))'''

#print(q)

tab = 'content-search-pars'

qn = 'New'

s = 'PublishDatePARS'

so = 'ASC'

p = Payload(q, tab, qn, s, so)

load = p.generate_payload()

r = requests.get(NRC_BASE_URL, params = load)

print(r.url)
print(r.content)

tree = ElementTree.fromstring(r.content)

ElementTree.dump(tree)
