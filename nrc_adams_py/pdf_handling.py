import io
import multiprocessing as mp
import re
from io import StringIO

import en_core_web_sm
import pdfminer
import requests
import spacy
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(url):
    '''Convert PDF document to raw text.

    Args:
        url(string): URL of pdf document.

    Returns:
        string: Raw text of the pdf if successful, None if not. 
    '''

    pdf = requests.get(url)
    if pdf.ok:

        pdf_b = pdf.content    
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = io.BytesIO(pdf_b)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()

        for page in list(PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True)):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()

        if str(text) == '\x0c':
            return None
        else:
            return text

    else:
        Warning('Bad response from %s' % url)
        return None

def pdf_link_to_text(url_list, num_threads):
    '''Parallelized processing of a list of urls to pdf documents into raw text.
       
    Args:
        url_list (list): List of URLs that resolve to PDF documents.  Bad resolution will lead to None returned.

        num_threads (int): Number of cores to use to use in paralleization.

    Returns:
        list: Raw text of PDF document if successful, None if not.
    '''
    num_cores = mp.cpu_count()
    if num_cores < num_threads:
        raise ValueError("Too many threads")
    
    pool = mp.Pool(mp.cpu_count() - 1)
    results = pool.map(convert_pdf_to_txt, [url for url in url_list])
    pool.close()

    return results

if __name__ == "__main__":

    convert_pdf_to_txt('https://www.nrc.gov/site-help/developers/wba-api-developer-guide.pdf')
