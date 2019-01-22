#Constants from https://www.nrc.gov/site-help/developers/wba-api-developer-guide.pdf

NRC_BASE_URL = 'https://adams.nrc.gov/wba/services/search/advanced/nrc'

#Content Search
#http://adams.nrc.gov/wba/services/search/advanced/nrc?q=<data_parameters>&qn=<query_name>&tab=content-search-pars&s=<sort_property>&so=ASC|DESC

DATA_PARAMETERS = '?q='
QUERY_NAME = '&qn='
CONTENT_SEARCH = '&tab=content-search-pars'
SORT_PROPERTY = '&s='
SORT_ORDER = '&so=' # 'ASC' or 'DESC'

CONTENT_SEARCH_URL = NRC_BASE_URL + DATA_PARAMETERS + QUERY_NAME + CONTENT_SEARCH + SORT_PROPERTY + SORT_ORDER

#Advanced Search
#http://adams.nrc.gov/wba/services/search/advanced/nrc?q=<data_parameters>&qn=<query_name>&tab=advanced-search-pars&s=<sort_property>&so=ASC|DESC

ADVANCED_SEARCH = '&tab=advanced-search-pars'

CONTENT_SEARCH_URL = NRC_BASE_URL + DATA_PARAMETERS + QUERY_NAME + ADVANCED_SEARCH + SORT_PROPERTY + SORT_ORDER

#Part 21 Search
#Use either the Content Search or Advanced Search, but with !(DocumentType,eq,'Part+21+Correspondence','')in the query <data_parameters>

DATA_PARAMETERS = DATA_PARAMETERS + '''!(DocumentType,eq,'Part+21+Correspondence,'')'''

#Operating Reactor Inspection Report Search
#Use either the Content Search or Advanced Search, but with !(DocumentType,[infolder|starts],'inspection+report',''),!(DocketNumber,[infolder|starts],'05000','')in the query <data_parameters>

DATA_PARAMETERS = DATA_PARAMETERS + '''!(DocumentType,[infolder|starts],'inspection+report',''),!(DocketNumber,[infolder|starts],'05000','')'''

#Library Types (search libraries)
library_types = {'public' : 'public-library:!t',
                 'legacy' : 'legacy-library:!t'}

#API Count exceeded warning message
count_exceeded_str = "LocalizedMessage{key='search.documents.limit.exceed.message', params=[1000]}"

#search fields and operators by property
document_properties = {
    'AccessionNumber':\
        {'content-search-pars':\
            ['eq','not','infolder','ends'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'eq', 'not', 'infolder','ends']
        },
    'AddresseeAffiliation':\
        {'content-search-pars':\
            ['eq','not','infolder','ends'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'eq', 'not', 'infolder','ends']
        },
    'AddresseeName':\
        {'content-search-pars':\
            ['eq','not','infolder','ends'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'eq', 'not', 'infolder','ends']
        },
    'AuthorAffiliation':\
        {'content-search-pars':\
            ['eq','not','infolder','ends'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'eq', 'not', 'infolder','ends']
        },
    'AuthorName':\
        {'content-search-pars':\
            ['eq','not','infolder','ends'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'eq', 'not', 'infolder','ends']
        },
    'CaseReferenceNumber':\
        {'content-search-pars':\
            ['eq','not','starts','ends', 'not_starts'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'contains', 'not_contains', 'eq','not']
        },
    'DocketNumber':\
        {'content-search-pars':\
            ['eq','not','infolder','ends'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'eq', 'not', 'infolder','ends']
        },
    'DocumentDateDate':\
        {'content-search-pars':\
            ['eq','gt','lt','range'], 
        'advanced-search-pars':\
            ['eq', 'not', 'gt', 'ge', 'lt','le','range']
        },
    'DocumentType':\
        {'content-search-pars':\
            ['eq','not','infolder','ends'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'eq', 'not', 'infolder','ends']
        },
    'Keyword':\
        {'content-search-pars':\
            ['eq','not','infolder','ends'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'eq', 'not', 'infolder','ends']
        },
    'LicenseNumber':\
        {'content-search-pars':\
            ['eq','not','infolder','ends'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'eq', 'not', 'infolder','ends']
        },
    'PackageNumber':\
        {'content-search-pars':\
            ['eq','not','infolder','ends'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'eq', 'not', 'infolder','ends']
        },
    'PackageNumber':\
        {'content-search-pars':\
            ['eq','not','infolder','ends'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'eq', 'not', 'infolder','ends']
        },
    'PublishDatePARS':\
         {'content-search-pars':\
            ['eq','gt','lt','range'], 
        'advanced-search-pars':\
            ['eq', 'not', 'gt', 'ge', 'lt','le','range']
        },
     '$title':\
        {'content-search-pars':\
            ['eq','not','starts','ends', 'not_starts'], 
        'advanced-search-pars':\
            ['starts', 'not_starts', 'contains', 'not_contains', 'eq','not']
        },
    }
