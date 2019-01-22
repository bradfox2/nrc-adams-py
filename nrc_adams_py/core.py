from nrc_adams_py.constants import NRC_BASE_URL, CONTENT_SEARCH, ADVANCED_SEARCH, library_types, count_exceeded_str, document_properties
import nrc_adams_py.constants
import requests
from xml.etree import ElementTree
import xmljson, xmltodict
import re

class AdamsSearch(object):
    '''A single search to the NRC ADAMS API.

    Attributes:
        q (str | q object): ADAMS q parameter either as string or q helper object.  CHR format.  
        
        tab (str): Type of search to perform, either `content-search-pars` or `advanced-search-pars`.  Content search is defaulted, and is used to search for matches inside of library documents, which is via the `single_content_search` sub-parameter in the q parameter.  Else the advanced search will be used.

        qn (str): Name of the query.

        s (str): Property name by which the result set will be sorted.

        so (str): Sort order. `ASC`|`DESC`

        base_url (str): ADAMS base url, imported from constants.py.

    '''

    def __init__(self, q, tab='content-search-pars', qn = None, s = None, so = None):
        if isinstance(q, str):
            self._q = q.replace(" ","")
            if 'single_content_search' in q and tab != 'content-search-pars':
                raise ValueError('Can only content search with defaulted tab value (content-search-pars).')
        else:
            self._q = str(q)

        self._tab = tab
        self._qn = qn
        self._s = s
        self._so = so
        self._request = None
        self.base_url = NRC_BASE_URL
        self.response_xml_tree = None
        self._response_dict = None

    def __repr__(self):
        return str(self.response)

    def _get_response(self):
        self._request = requests.get(self.base_url, {'q': self._q,
                        'tab': self._tab,
                        'qn': self._qn,
                        's' : self._s,
                        'so' : self._so },
                        timeout=10)
        if self._request.status_code != 200:
            raise SystemError("API response code was not 200-OK")
        
        self.response_xml_tree = ElementTree.fromstring(self._request.content)
        
        #warn on incomplete result set
        if self.response_xml_tree.find('matches').text == count_exceeded_str:
            Warning("Search exeeded ADAMS max count allowed limit (1000).  Result set is incomplete.")

    @property
    def response(self):
        if self._request is not None:
            return self._request.content
        else:
            self._get_response()
            return self._request.content
    
    @property
    def url(self):
        if self._request is None:
            self.response
            return self._request.url
        else:
            return self._request.url

    @property
    def response_dict(self):
        '''Dict of the Responses, modified to make the URI field actually work by using the Accession Number.  The default URI appears to link to some non-accessible NRC internal system.
        '''
        
        if self._response_dict is None:
            self._response_dict = xmltodict.parse(self.response)
            for doc in self._response_dict['search']['resultset']['result']:
                if doc['MimeType'] == 'application/pdf':
                    # hotlinking to pdf documents by accession number appears to work
                    # https://adamswebsearch2.nrc.gov/webSearch2/main.jsp?AccessionNumber=ML19009A487
                    doc['URL'] = 'https://adamswebsearch2.nrc.gov/webSearch2/main.jsp?AccessionNumber=' + doc['AccessionNumber']
            return self._response_dict
        else:
            return self._response_dict
    
    @property
    def response_documents(self):
        '''List of dicts, where each dict is a document in the response.
        '''
        return self.response_dict['search']['resultset']['result']

class q(object):
    ''' Get data parameters in the form ADAMS needs.

    Attributes:
        filters[string]: 'public' or 'legacy'.  Dict keys to constants.library_keys.  Search library.  Legacy is pre-2000.
        
        options[Options]: Options class instance.

        properties_search_type[string]: 'properties_search_all' or 'properties_search_any'.  All performs AND search, any performs OR search.

        properties_search[list]: List of lists where inner list is 3 elements. eg [[<property>, <operator>, <value>], ...].  The type/operator combinations are documented under nrc_adams_py.constants.document_properties

        single_content_search [str]: Search terms matched to document content.

        tab [str]: Repeat parameter from AdamsSearch. Type of search to perform, either `content-search-pars` or `advanced-search-pars`.  Content search is defaulted, and is used to search for matches inside of library documents, which is via the `single_content_search` sub-parameter in the q parameter.  Else the advanced search will be used.

    Example:
        >>>q=q(properties_search_type= 'properties_search_any', properties_search=[['DocumentType', 'starts', "'inspection+report'"],
        ['DocketNumber', 'starts', "'05000'"],
        ['DocumentDate', 'range', "(left:'04/01/2013',right:'05/01/2013')"]], options = Options())

    '''
    
    def __init__(self, properties_search_type, properties_search, single_content_search = None, options = None, filters = 'public', tab = 'content-search-pars'):
        
        self._value = '(mode:sections,sections:('
        if filters is not None:
            if filters in library_types.keys():
                self._filters = 'filters:(' + library_types[filters] + '),'
                self._value += self._filters

        if options is None:
            raise Warning('Options needs to be an instance of Options if an advanced search is being performed. Content search will support a null options field')
        else:
            self._value += str(options)
        
        if properties_search_type is None:
            raise ValueError("This arg needs to be passed.")
        else:
             self._value += properties_search_type + ':!(' 

        if properties_search is None or len(properties_search) == 0:
            raise  ValueError('Pass some search properties.')
        else:
            temp_value = ''
            for i, inner  in enumerate(properties_search):
                if inner[0] not in document_properties.keys():
                    raise ValueError("document property must be one of the specified document properties in document_properties list")

                #check search operator against document properties/seach op dict
                if inner[1] not in document_properties[inner[0]][tab]:
                    raise ValueError("search operator must be one of the specified search operators.")
                #dont add trailing comma at end of list
                if i + 1 == len(properties_search):
                    temp_value += '!(' + ','.join(inner) + ",'')" 
                else:
                    temp_value += '!(' + ','.join(inner) + ",''),"

            self._value += temp_value
        
        #close the properties search parens and the mode section parens
        self._value += ')' 

        if single_content_search is not None:
            self._value += ",single_content_search:'" + re.sub(' ','+',single_content_search)
        
        #close the mode section parens and the q parens
        self._value += ')' + ')'
        
    def __repr__(self):
        return self._value

    #value = '''(mode:sections,sections:(filters:(public-library:!t),properties_search:!(!('$title',infolder,'Browns+Ferry','')),properties_search_any:!(!(DocumentType,ends,NUREG,''),!(DocumentType,ends,'NUREG+REPORTS','')),single_content_search:'steam+generator'))'''

class Options(object):
    '''Options parameter in ADAMS form.
    
    Provide an options_list OR the remainder of the arguments to define a set of options. 

    Object instance call returns a string of the requested options in ADAMS format.

    Attributes:
        Options List: list of options in string format.  

        OR 
        
        Choose one of:
        added_this_month [bool]
        added_this_day [bool]

        AND 

        subfolder_path [string]: Absolute reference to the folder path in the document library.  See NRC guide for more detail. 
    '''
    def __init__(self, options_list = [], added_this_month = False, added_this_day = False, subfolder_path = None):
        
        self._options = None
        
        #pass list back as options string
        if options_list and len(options_list) > 1:
            ol_str = ','.join(options_list)
            self._options = 'options:(' + ol_str + '),'
        
        #process remainder of params into a list, and then join to options string
        self.options_list = []
        
        if added_this_month & added_this_day:
            raise ValueError('Only added_this_month or added_this_day can be true.')
        else:
            if added_this_day:
                self.options_list.append('added-this-day')
            if added_this_month:
                self.options_list.append('added-this-month')

        if subfolder_path is not None:
            self._subfolder_path = "within-folder:(enable:!t,insubfolder:!t,path:'" + subfolder_path + "')"
            self.options_list.append(self._subfolder_path)
        else:
            self._subfolder_path = "within-folder:(enable:!f,insubfolder:!f,path:'')"
            self.options_list.append(self._subfolder_path)

        ol_str = ','.join(self.options_list)
        self._options = self._options = 'options:(' + ol_str + '),'
    
    def __repr__(self):
        return self._options


if __name__ == '__main__':
    print("small tests")
    print(NRC_BASE_URL)
    a = Options()
    a

    b = q(properties_search_type= 'properties_search_any', properties_search=[['DocumentType', 'starts', "'inspection+report'"],
    ['DocketNumber', 'starts', "'05000'"],
    ['DocumentDate', 'range', "(left:'04/01/2013',right:'05/01/2013')"]], options = a)
    b

    x = AdamsSearch(b, 'advanced-search-pars')
    #print(x.response)
    print(x.url)
    print(x.response_documents[0])
