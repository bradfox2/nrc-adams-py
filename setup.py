from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nrc_adams_py",
    version="0.0.3",
    author="Brad Fox",
    author_email="bradley.fox@avfintellitech.com",
    description="Python Class connect to NRC ADAMS API",
    long_description="""Class for Python Interaction with NRC Adams API.

    https://www.nrc.gov/site-help/developers/wba-api-developer-guide.pdf

    Adams.nrc.gov contains hundreds of thousands of full-text documents that the NRC has released since November 1, 1999, and several hundred new documents are added each day.

    The following document libraries at adams.nrc.gov are available to the APIs:

    *Public Library. Contains all image and text documents that the NRC has made public since November 1, 1999—over 800,000 full-text documents, and over 60,000 packages (virtual containers of related documents). This collection includes publicly available regulatory guides, NUREG-series reports, inspection reports, Commission documents, correspondence, and other regulatory and technical documents written by NRC staff, contractors, and licensees. The Public Library is available through both the Content Search API and the Advanced Search API.

    *Legacy Public Library. Contains over 1.9 million bibliographic records (some with abstracts and full text) that the NRC made public before November 1999. The Legacy Public Library is available only through the Advanced Search API.

    Data will change over the co urse of the day as the NRC issues new documents. For this reason counts may vary and may age quickly, depending on site activity and time.

    Search result sets for all APIs in this guide are limited to 1,000 results. If more than 1,0000 documents match the search criteria, then the following will occur:

    *only the first 1,000 matches will be returned,

    *the . . . field in the result set will be set to LocalizedMessage{key='search.documents.limit.exceed.message', params=[1000]} and

    *the . . .field in the result set will be set to 1000.""",
    long_description_content_type="text/markdown",
    url="https://github.com/bradfox2/nrc-adams-py",
    packages=find_packages(),
    test_suite = 'nose.collector',
    test_require = ['nose'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)