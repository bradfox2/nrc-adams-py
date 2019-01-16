from constants import NRC_BASE_URL, CONTENT_SEARCH
import requests
from xml.etree import ElementTree

class Payload(object):
    '''A group of General Parameters that will make up a payload for GET request.'''
    def __init__(self, q, tab, qn = None, s = None, so = None):
        self._q = q
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


q = '''(mode:sections,sections:( filters:(public-library:!t),),properties_search_any:!(!(DocumentType,ends,'Enforcement+Action','')),single_content_search:'Gamma+Knife’))'''

tab = 'content-search-pars'

qn = 'New'

s = 'PublishDatePARS'

so = 'ASC'

p = Payload(q, tab, qn, s, so)

load = p.generate_payload()

#working
#https://adams.nrc.gov/wba/services/search/advanced/nrc?q=(mode:sections,sections:(filters:(public-library:!t),properties_search_any:!(!(DocumentType,ends,%27Enforcement+Action%27,%27%27)),single_content_search:%27Gamma+Knife%27))&qn=New&tab=content-search-pars&s=PublishDatePARS&so=ASC

#not
#https://adams.nrc.gov/wba/services/search/advanced/nrc?q=%28mode%3Asections%2Csections%3A%28+filters%3A%28public-library%3A%21t%29%2C%29%2Cproperties_search_any%3A%21%28%21%28DocumentType%2Cends%2C%27Enforcement%2BAction%27%2C%27%27%29%29%2Csingle_content_search%3A%27Gamma%2BKnife%C3%A2%E2%82%AC%E2%84%A2%29%29&tab=content-search-pars&qn=New&s=PublishDatePARS&so=ASC

#http://adams.nrc.gov/wba/services/search/advanced/nrc?q=( mode:sections,sections:( filters:( public-library:!t), ),properties_search_any:!( !(DocumentType,ends,'Enforcement+Action','') ),single_content_search:'Gamma+Knife’ ) )&qn=New&tab=content-search-pars&s=DocumentDate&so=DESC


#requests is stripping parens
r  = requests.get(NRC_BASE_URL, params = load)

url = r.url

print(r.url)

print(r.content)

tree = ElementTree.fromstring(r.content)
