import nose
from nose import with_setup

from nrc_adams_py import core
from nrc_adams_py.constants import NRC_BASE_URL
from nrc_adams_py.core import Options, AdamsSearch, q, build_properties_search_string, build_property_string

#print("small tests")
#print(NRC_BASE_URL)

def setup_func():
    pass

def teardown_func():
    pass

def test_build_property_string():
    x = str(build_property_string(['AddresseeAffiliation', 'eq', "Arizona Nuclear Power Project"]))

    assert x == "!(AddresseeAffiliation,eq,Arizona Nuclear Power Project,'')"

def test_build_properties_search_string():
    x = str(build_properties_search_string([
    ['AddresseeAffiliation', 'eq', "'Arizona Nuclear Power Project'"],
    ['AddresseeAffiliation', 'eq', "'Arizona Public Service Co'"],
    ['AddresseeAffiliation', 'eq', "'Arizona Public Service Co, (Formerly Arizona Nuclear)'"]], 'advanced-search-pars'))

    assert x == "!(AddresseeAffiliation,eq,'Arizona Nuclear Power Project',''),!(AddresseeAffiliation,eq,'Arizona Public Service Co',''),!(AddresseeAffiliation,eq,'Arizona Public Service Co, (FormerlyArizona Nuclear)','')"

def testOptions():
    a = Options(options_list=[])
    assert str(a) == "options:(within-folder:(enable:!f,insubfolder:!f,path:'')),"
@with_setup(setup_func, teardown_func)
def testQ():
    b = q(properties_search_type_any=[['DocumentType', 'starts', "'inspection+report'"],
    ['DocketNumber', 'starts', "'05000'"],
    ['DocumentDate', 'range', "(left:'04/01/2013',right:'05/01/2013')"]], options = Options(options_list=[]), tab='advanced-search-pars')
    
    assert str(b) == "(mode:sections,sections:(filters:(public-library:!t),options:(within-folder:(enable:!f,insubfolder:!f,path:'')),properties_search_any:!(!(DocumentType,starts,'inspection+report',''),!(DocketNumber,starts,'05000',''),!(DocumentDate,range,(left:'04/01/2013',right:'05/01/2013'),''))))"

def testAdamsSearch():
    b = q(properties_search_type_any=[['DocumentType', 'starts', "'inspection+report'"],['DocketNumber', 'starts', "'05000'"],['DocumentDate', 'range', "(left:'04/01/2013',right:'05/01/2013')"]], options = Options(options_list=[]),tab='advanced-search-pars')

    x = AdamsSearch(b)
    
    print(x.url)

    assert str(x.url) == "https://adams.nrc.gov/wba/services/search/advanced/nrc?q=%28mode%3Asections%2Csections%3A%28filters%3A%28public-library%3A%21t%29%2Coptions%3A%28within-folder%3A%28enable%3A%21f%2Cinsubfolder%3A%21f%2Cpath%3A%27%27%29%29%2Cproperties_search_any%3A%21%28%21%28DocumentType%2Cstarts%2C%27inspection%2Breport%27%2C%27%27%29%2C%21%28DocketNumber%2Cstarts%2C%2705000%27%2C%27%27%29%2C%21%28DocumentDate%2Crange%2C%28left%3A%2704%2F01%2F2013%27%2Cright%3A%2705%2F01%2F2013%27%29%2C%27%27%29%29%29%29&tab=advanced-search-pars&qn=New&s=DocumentDate&so=DESC"

    assert isinstance(x.response_documents, dict)

    assert list(x.response_documents)[0] == 'ML18342A014'

if __name__ == '__main__':
    
    b = q(properties_search_type_any=[['DocumentType', 'starts', "'inspection+report'"],['DocketNumber', 'starts', "'05000'"],['DocumentDate', 'range', "(left:'04/01/2013',right:'05/01/2013')"]], options = Options(options_list=[]), tab = 'advanced-search-pars')
        
    x = AdamsSearch(b,so= '$title')
    print(list(x.response_documents)[0])
