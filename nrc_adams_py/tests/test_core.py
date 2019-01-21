from nrc_adams_py import core
from nrc_adams_py.constants import NRC_BASE_URL
from nrc_adams_py.core import Options, AdamsSearch, q

#print("small tests")
#print(NRC_BASE_URL)

def test_options():
    a = Options()
    assert str(a) == "options:(within-folder:(enable:!f,insubfolder:!f,path:'')),"

def test_q():
    b = q(properties_search_type= 'properties_search_any', properties_search=[['DocumentType', 'starts', "'inspection+report'"],
    ['DocketNumber', 'starts', "'05000'"],
    ['DocumentDate', 'range', "(left:'04/01/2013',right:'05/01/2013')"]], options = Options())
    
    assert str(b) == "(mode:sections,sections:(filters:(public-library:!t),options:(within-folder:(enable:!f,insubfolder:!f,path:'')),properties_search_any:!(!(DocumentType,starts,'inspection+report',''),!(DocketNumber,starts,'05000',''),!(DocumentDate,range,(left:'04/01/2013',right:'05/01/2013'),''))))"

def test_AdamsSearch():
    b = q(properties_search_type= 'properties_search_any', properties_search=[['DocumentType', 'starts', "'inspection+report'"],
    ['DocketNumber', 'starts', "'05000'"],
    ['DocumentDate', 'range', "(left:'04/01/2013',right:'05/01/2013')"]], options = Options())

    x = AdamsSearch(b, 'advanced-search-pars')

    assert str(x.url) == "https://adams.nrc.gov/wba/services/search/advanced/nrc?q=%28mode%3Asections%2Csections%3A%28filters%3A%28public-library%3A%21t%29%2Coptions%3A%28within-folder%3A%28enable%3A%21f%2Cinsubfolder%3A%21f%2Cpath%3A%27%27%29%29%2Cproperties_search_any%3A%21%28%21%28DocumentType%2Cstarts%2C%27inspection%2Breport%27%2C%27%27%29%2C%21%28DocketNumber%2Cstarts%2C%2705000%27%2C%27%27%29%2C%21%28DocumentDate%2Crange%2C%28left%3A%2704%2F01%2F2013%27%2Cright%3A%2705%2F01%2F2013%27%29%2C%27%27%29%29%29%29&tab=advanced-search-pars"

    assert isinstance(x.response_documents[0], dict)

    assert str(x.response_documents[0]) ==  """OrderedDict([('@number', '1'), ('AddresseeAffiliation', 'Tennessee Valley Authority'), ('AuthorName', 'Bonser B R'), ('Keyword', 'cxs7, nrpars, oarc20080515wjd1, rls1, SUNSI Review Complete, utsPARS'), ('MimeType', 'application/pdf'), ('LicenseNumber', 'CPPR-0092, NPF-090'), ('AuthorAffiliation', 'NRC/RGN-II/DRS/PSB2'), ('DocumentType', 'Inspection Report Correspondence, Letter'), ('DocketNumber', '05000390, 05000391'), ('AddresseeName', 'Campbell W R'), ('CompoundDocumentState', 'false'), ('EstimatedPageCount', '11'), ('ContentSize', '385,929'), ('DocumentTitle', 'IR 05000390-08-002 & 05000391-08-002, on 02/11-15/2008 & 02/25-29/2008, Watts Bar Baseline Occupational Radiation Safety Inspection.'), ('AccessionNumber', 'ML073400098'), ('PublishDatePARS', '12/13/2007 09:15 AM EST'), ('DocumentDate', '12/03/2007'), ('DocumentReportNumber', 'IR-08-002'), ('URI', 'http://adams.nrc.gov:9080/wba/view?action=view&actionId=view&ids=[{"documentId":%7B%22dataProviderId%22%3A%22ce_bp8os_repository%22%2C%22compound%22%3Afalse%2C%22properties%22%3A%7B%22%24os%22%3A%22ADAMSPublicOS%22%2C%22ce_object_id%22%3A%22%7B056710BA-02D0-495F-9B3E-00001F667656%7D%22%2C%22%24is_compound%22%3Afalse%7D%7D}]&mimeType=application/pdf&docTitle=IR 05000390-08-002 & 05000391-08-002, on 02/11-15/2008 & 02/25-29/2008, Watts Bar Baseline Occupational Radiation Safety Inspection.'), ('URL', 'https://adamswebsearch2.nrc.gov/webSearch2/main.jsp?AccessionNumber=ML073400098')])"""



