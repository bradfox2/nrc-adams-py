import nose
from nose import with_setup, raises

from nrc_adams_py import core
from nrc_adams_py.constants import NRC_BASE_URL
from nrc_adams_py.core import Options, AdamsSearch, q

import pdfminer
import io
import requests
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

import nrc_adams_py.pdf_handling
from nrc_adams_py.pdf_handling import convert_pdf_to_txt

def testPdfhandling():
    assert str(convert_pdf_to_txt('https://www.nrc.gov/site-help/developers/wba-api-developer-guide.pdf')[-10:]) == 'cement'

@raises(FileNotFoundError)
def testURLfailure():
    convert_pdf_to_txt('https://www.nrc.gov/site-help/developers/wba-api-developer-guidadsfasdfe.pdf')



