from nrc_adams_py.constants import NRC_BASE_URL, CONTENT_SEARCH, ADVANCED_SEARCH, library_types, count_exceeded_str, document_properties,DOC_URL_BASE
import nrc_adams_py.constants
import requests
from xml.etree import ElementTree
import xmljson, xmltodict
import re
import copy

class AdamsSearch(object):
    '''A single search to the NRC ADAMS API.

    Args:
        q (str | q object): ADAMS q parameter either as string or q helper object.  CHR format.  

        qn (str): Name of the query.

        s (str): Property name by which the result set will be sorted.

        so (str): Sort order. `ASC`|`DESC`

        base_url (str): ADAMS base url, imported from constants.py.

        auto_expand_search (int): 1000 < n < (high limit not enforced for now) Number of search results to return. Automatically expand the search result beyond the NRC imposed limit of 1000 entries.

    Attributes:
        response (string): String response from the http request. 

        url (string): Formatted search URL for HTTP GET request.

        response_documents (dict): Dict of the Response documents where k:v = AccessionNumber:OrderedDictDoct Object where keys are field names.  Documents are only those of PDF type.

        hit_count (int): Number of documents returned.

        doc_url_list (list): List of lists consisting of retrieved document title and the direct document URL.
    '''

    def __init__(self, q, qn = 'New', s = 'DocumentDate', so = 'DESC', auto_expand_search = 1000):
        self._q_og = copy.deepcopy(q)
        if isinstance(q, str):
            self._q = q.replace(" ","")
            if 'single_content_search' in q and tab != 'content-search-pars':
                raise ValueError('Can only content search with defaulted tab value (content-search-pars).')
        else:
            self._q = str(q)
        
        #date descending to expand search
        if auto_expand_search <= 1000:
            self._so = so 
            self._aes = 1000
            self._s = s
        else:
            self._so = 'DESC'
            self._aes = auto_expand_search
            self._s = 'DocumentDate'
        self._tab = q._tab
        self._qn = qn
        self._request = None
        self.base_url = NRC_BASE_URL
        self._response_xml_tree = None
        self._response_dict = None
        self._hit_count = None
        self._url = None
        self._doc_url_list = None
        self._full_response_dict = None
        
    def __repr__(self):
        return str(self.response)

    def _get_response(self):
        ''' Gets a response from ADAMS and builds an ordered dict with them,  search expanding if requested, by sorting results by document date, and repeatedly iterating, starting with the oldest date.
        '''
        self._request = requests.get(self.base_url, {'q': self._q,
                                                    'tab': self._tab,
                                                    'qn': self._qn,
                                                    's' : self._s,
                                                    'so' : self._so },
                                                    timeout=10)

        if not self._request.ok:
            raise SystemError("ADAMS response code was not status 200.")
        
        self._response_xml_tree = ElementTree.fromstring(self._request.content)
        
        #warn on incomplete result set if not expected
        if self._response_xml_tree.find('matches').text == "LocalizedMessage{key='search.documents.limit.exceed.message', params=[1000]}" and self._aes == 1000:
            Warning("Search exeeded ADAMS max count allowed limit (1000).  Result set is incomplete. Consider auto_expand_search > 1000.")

        self._full_response_dict = xmltodict.parse(self._request.content)

        self._response_dict = self._full_response_dict['search']['resultset']['result']

        self._temp_count = int(self._full_response_dict['search']['count'])
        
        #continue expansion if count < 1000 
        if self._aes > 1000 and self._temp_count >= 1000:  
            num_docs = 1000
            remaining_docs = self._aes - num_docs
            oldest_date = next(reversed(self._response_dict))[self._s]

            #if still under requested amount and there are remaining docs keep looping

            #get last added element from inital ordered dict
            
            while num_docs < self._aes and remaining_docs > 0: 
                #raise NotImplementedError

                #reint q with old values and modified properties search types
                self._q_og._properties_search_type_all =[[str(self._s),'lt',"'" + oldest_date + "'"]]

                q_new = q(properties_search_type_any = self._q_og._properties_search_type_any, properties_search_type_all = self._q_og._properties_search_type_all, options = self._q_og._options, tab=self._q_og._tab)
                
                init_req = requests.get(self.base_url, {'q': q_new,
                                'tab': self._tab,
                                'qn': self._qn,
                                's' : self._s,
                                'so' : 'DESC'},
                                timeout=100)
                
                if init_req.ok:
                    #combine next set with original result set dict
                    remaining_docs = int(ElementTree.fromstring(init_req.content).find('count').text)

                    new_dict = xmltodict.parse(init_req.content)['search']['resultset']['result'] 

                    self._response_dict.extend(new_dict)
                    
                    oldest_date = next(reversed(new_dict))[self._s]
                    
                    num_docs += remaining_docs
            
                else: 
                    raise ValueError("Request not successful")
        
        temp_dict = {}

        for doc in self._response_dict:
            if doc['MimeType'] == 'application/pdf':
                # hotlinking to pdf documents by accession number appears to work
                # https://adamswebsearch2.nrc.gov/webSearch2/main.jsp?AccessionNumber=ML19009A487
                doc['URL'] = DOC_URL_BASE + doc['AccessionNumber']    
            temp_dict[doc['AccessionNumber']] = doc
        self._response_dict = temp_dict

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
    def response_documents(self):
        '''Dict, k:v = AccessionNumber:response ordered dict. Modified to make the URL field actually work by using the Accession Number.  The default URI appears to link to some non-accessible NRC internal system.
        '''
        if self._response_dict is None:
            self._get_response()
            return self._response_dict
        else:
            return self._response_dict
    
    @property
    def hit_count(self):
        if self._hit_count is None:
            self._hit_count = len(self.response_documents.keys())
            return self._hit_count
        else:
            return self._hit_count
    
    @property
    def doc_url_list(self):
        if self._doc_url_list is None:
            self._doc_url_list = [[doc['DocumentTitle'], doc['URL']] for doc in self.response_documents.values()]
        else:
            self._doc_url_list

class q(object):
    ''' Get data parameters in the form ADAMS needs.

    Args:
        filters[string]: 'public' or 'legacy'.  Dict keys to constants.library_keys.  Search library.  Legacy is pre-2000.
        
        options[Options]: Options class instance.

        properties_search_type_any[list]: Search match any of the provided criteria.  List of lists where inner list is 3 elements. eg [[<property>, <operator>, <value>], ...].  The type/operator combinations are documented under nrc_adams_py.constants.document_properties.  

        properties_search_type_all[list]: Search match all of the provided criteria. List of lists where inner list is 3 elements. eg [[<property>, <operator>, <value>], ...].  The type/operator combinations are documented under nrc_adams_py.constants.document_properties

        single_content_search [str]: Search terms matched to document content.

        tab [str]: Type of search to perform, either `content-search-pars` or `advanced-search-pars`.  Content search is defaulted, and is used to search for matches inside of library documents, which is via the `single_content_search` sub-parameter in the q parameter.  Else the advanced search will be used.

    Example:
        >>>q=q(properties_search_type= 'properties_search_any', properties_search_any=[['DocumentType', 'starts', "'inspection+report'"],['DocketNumber', 'starts', "'05000'"],
        ['DocumentDate', 'range', "(left:'04/01/2013',right:'05/01/2013')"]], options = Options())

    '''

    def __init__(self, properties_search_type_any = None, properties_search_type_all = None, single_content_search = None, options = None, filters = 'public', tab = 'content-search-pars'):

        #store originals for later reconstruction of q parameter
        self._properties_search_type_any = properties_search_type_any
        self._properties_search_type_all = properties_search_type_all
        self._single_content_search = single_content_search
        self._options = options
        self._filters = filters
        self._tab = tab
        
        self._value = '(mode:sections,sections:('
        if filters is not None:
            if filters in library_types.keys():
                self._filters = 'filters:(' + library_types[filters] + '),'
                self._value += self._filters

        if options is None:
            raise Warning('Options needs to be an instance of Options if an advanced search is being performed. Content search will support a null options field')
        else:
            self._value += str(options)

        #validate one of the search types was passed 
        if (properties_search_type_any is None and properties_search_type_all is None):
            raise ValueError("One of the properties search types needs to be passed.")

        comma_flag = False
        for search_type, search_type_parameter_list in zip(['properties_search_all:!(', 'properties_search_any:!('],[properties_search_type_all, properties_search_type_any]):
            if search_type_parameter_list is not None:
                if comma_flag == True: #seperate the two types 
                    self._value += ','        
                self._value += search_type 
                self._value += build_properties_search_string(search_type_parameter_list, self._tab) + ")"
                comma_flag = True

                
        if single_content_search is not None:
            self._value += ",single_content_search:'" + re.sub(' ','+',single_content_search)

        #close the mode section parens and the q parens
        self._value += ')' + ')'

    def __repr__(self):
        return self._value

    #value = '''(mode:sections,sections:(filters:(public-library:!t),properties_search:!(!('$title',infolder,'Browns+Ferry','')),properties_search_any:!(!(DocumentType,ends,NUREG,''),!(DocumentType,ends,'NUREG+REPORTS','')),single_content_search:'steam+generator'))'''

def build_properties_search_string(properties_search_list, tab):
    ''' Assemble the properties portion of the data parameters search string.

    Args:
        properties_search_list (list): List of the document search properties.  See docs for q class.

        tab (string): Search type parameter.  See docs for q class.
    '''
    ss = ''
    
    for i, inner  in enumerate(properties_search_list):
        temp_value = ''
        if inner[0] not in document_properties.keys():
            raise ValueError("document property must be one of the specified document properties in document_properties list")

        #check search operator against document properties/seach op dict
        if inner[1] not in document_properties[inner[0]][tab]:
            raise ValueError("Search operator must be one of the specified search operators.")
        #dont add trailing comma at end of list
        if i + 1 == len(properties_search_list):
            temp_value += build_property_string(inner) 
        else:
            temp_value += build_property_string(inner) + ","

        ss += temp_value

    return(ss)

def build_property_string(prop_list):
    '''Assemble the lower level data parameter properties string from a single list entry.

    Args:
        prop_list (list): List of document search properties. See Example for q class.
    '''
    return '!(' + ','.join(prop_list) + ",'')"

class Options(object):
    '''Options parameter in ADAMS form.
    
    Provide an options_list OR the remainder of the arguments to define a set of options. 

    Object instance call returns a string of the requested options in ADAMS format.

    Args:
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

class ADAMSDoc(object):
    '''Not Utilized. Representation of a document returned from ADAMS.

    Args:
        adams_doc_dict(dict): Dict where keys are ADAMS XML field tags, and value is the field data.
    
    Attributes:
        MimeType (string): Document MimeType.  Example: application/pdf
        EstimagedPageCount (int): Estimated Document Page Count
        Keyword (string): Keywords seperated by comma
        PackageNumber (int): Package Number
        Publish Date PARS (date): Date added in WBA
        DocumentTitle (string): Doc title
        DocumentType (string): The document type.
        CompountDocumentState (bool): if true, this is a compound document.
        Web Address (string): URI for document.  This does not appear to be a user accessible field.
        Comment (string): Comment property for the document.
        RelatedDate (date): Related Date
    '''
    def __init__(self, adams_doc_dict):
        self.MimeType = adams_doc_dict['MimeType']
        self.EstimatedPageCount = adams_doc_dict['EstimatedPageCount']
        self.CaseReferenceNumber = adams_doc_dict['CaseReferenceNumber']
        self.ContentSize = adams_doc_dict['ContentSize']
        self.AuthorAffiliation = adams_doc_dict['AuthorAffiliation']
        self.Keyword = adams_doc_dict['Keyword']
        self.DocumentDate = adams_doc_dict['DocumentDate']
        self.LicenseNumber = adams_doc_dict['LicenseNumber']
        self.DocketNumber = adams_doc_dict['DocketNumber']
        self.AccessionNumber = adams_doc_dict['AccessionNumber']
        self.PackageNumber = adams_doc_dict['PackageNumber']
        self.PublishDatePARS = adams_doc_dict['PublishDatePARS']
        self.DocumentTitle = adams_doc_dict['DocumentTitle']
        self.DocumentReportNumber = adams_doc_dict['DocumentReportNumber']
        self.DocumentType = adams_doc_dict['DocumentType']
        self.AuthorName = adams_doc_dict['AuthorName']
        self.CompoundDocumentState = adams_doc_dict['CompoundDocumentState']
        self.AddresseeAffilliation = adams_doc_dict['AddresseeAffiliation']
        self.WebAddress = adams_doc_dict['URI'] # this does not appear to exist in returned searches
        self.MicroformAddresses = adams_doc_dict['MicroformAddresses']
        self.Comment = adams_doc_dict['Comment']
        self.RelatedDate  = adams_doc_dict['RelatedDate']
        self.AddresseeName = adams_doc_dict['AddresseeName']
        self.URI_internal = adams_doc_dict['URI']
        self.URL_document = adams_doc_dict[DOC_URL_BASE + self.AccessionNumber]
    
    def __repr__(self):
        print('Accession:' + self.AccessionNumber + ' ,' + self.DocumentTitle)

if __name__ == '__main__':
    print("Usage Example")
    
    a = Options()

    b = q(properties_search_type_any=[
    ['AddresseeAffiliation', 'eq', "'Arizona Public Service Co, (Formerly Arizona Nuclear)'"],
    ['AddresseeAffiliation', 'eq', "'Arizona Public Service Co'"],
    ['AddresseeAffiliation', 'eq', "'Arizona Public Service Co, (Formerly Arizona Nuclear)'"]
    ], options = a, tab='advanced-search-pars')
    
    x = AdamsSearch(b, auto_expand_search = 2000)
    
    print(x.url)
    print(len(x.response_documents))
    print(x.response_documents.keys())
