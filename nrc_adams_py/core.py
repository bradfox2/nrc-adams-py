from constants import NRC_BASE_URL, CONTENT_SEARCH, ADVANCED_SEARCH, library_types
import requests
from xml.etree import ElementTree

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

    import requests
    from . import NRC_BASE_URL, CONTENT_SEARCH, ADVANCED_SEARCH
    
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

    def __repr__(self):
        return str(self.response)

    @property
    def response(self):
        if self._request is not None:
            return self._request.content
        else:
            self._request = requests.get(self.base_url, {'q': self._q,
                'tab': self._tab,
                'qn': self._qn,
                's' : self._s,
                'so' : self._so },
                timeout=10)
            return self._request.content
    
    @property
    def url(self):
        if self._request is None:
            self.response
            return self._request.url
        else:
            return self._request.url


class q(object):
    ''' Get data parameters in the form ADAMS needs.

    Attributes:
        filters[string]: 'public' or 'legacy'.  Dict keys to constants.library_keys.  Search library.  Legacy is pre-2000.
        
        options[Options]: Options class instance.

        properties_search_type[string]: 'properties_search_all' or 'properties_search_any'.  All performs AND search, any performs OR search.

        properties_search[list]: List of lists where inner list is 3 elements. eg [[<property>, <operator>, <value>], ...]


    Example:
        q=( mode:sections,sections:( filters:( public-library:!t), options:( within-folder:(enable:!f,insubfolder:!f,path:'') ),properties_search_all:!( !(AuthorName,starts,Macfarlane,''), !(DocumentType,starts,Speech,'') ) ) )

    '''
    from constants import library_types

    def __init__(self, properties_search_type, properties_search, options = None, filters = 'public'):
        
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
                #dont add trailing comma at end of list
                if i + 1 == len(properties_search):
                    temp_value += '!(' + ','.join(inner) + ",'')" 
                else:
                    temp_value += '!(' + ','.join(inner) + ",''),"

            self._value += temp_value
        
        #close the properties search parens and the mode section parens
        self._value += ')' + ')' + ')'
        
    def __repr__(self):
        return self._value

    #value = '''(mode:sections,sections:(filters:(public-library:!t),properties_search:!(!('$title',infolder,'Browns+Ferry','')),properties_search_any:!(!(DocumentType,ends,NUREG,''),!(DocumentType,ends,'NUREG+REPORTS','')),single_content_search:'steam+generator'))'''

class Options(object):
    '''box spread yar yar yar.
    Provide an options_list OR the remainder of the arguments to define a set of options. 

    Object instance call returns a string of the requested options in ADAMS format.

    Attributes:
        Options List: list of options in string format.  

        OR 

        added_this_month [bool]
        added_this_day [bool]
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
    a = Options()
    a

    b = q(properties_search_type= 'properties_search_any', properties_search=[['AuthorName','starts','Macfarlane'], ['DocumentType', 'starts', 'Speech']], options = a)
    b

    x = AdamsSearch(b, 'advanced-search-pars')
    print(x.response)
    print(x.url)

