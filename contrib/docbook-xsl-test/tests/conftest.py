# -*- coding: UTF-8 -*-

from __future__ import print_function

import sys
import os
import os.path
import glob

import pytest
from lxml import etree
import platform
import commands

def getlocalpath(catalog, url):
   """Returns the local path from url found in file catalog
   """
   cmd="xmlcatalog {0} {1}".format(catalog, url)
   result=commands.getstatusoutput(cmd)
   if result[0]:
      raise OSError("Problem with xmlcatalog: {0}".format(result[1]))
   
   # Small trick which works in both cases, with and without file:// suffix
   return result[1].split("file://")[-1]


CANONICALURL='http://docbook.sourceforge.net/release/xsl/current/'
MAINXMLCATALOG={
   'Linux':    "/etc/xml/catalog",
   'Mac':      "/etc/xml/catalog",
   'Windows':  None,
   }
STYLESHEETS={
   'html-single':     'html/docbook.xsl',
   'html-chunk':      'html/chunk.xsl',
   'xhtml-single':    'xhtml/docbook.xsl',
   'xhtml-chunk':     'xhtml/chunk.xsl',
   'xhtml1.1-single': 'xhtml-1_1/docbook.xsl',
   'xhtml1.1-chunk':  'xhtml-1_1/chunk.xsl',
   'xhtml5-single':   'xhtml5/docbook.xsl',
   'xhtml5-chunk':    'xhtml5/chunk.xsl',
   'fo':              'fo/docbook.xsl',
   'profile':         'profiling/profile.xsl',
   'epub':            'epub/docbook.xsl',
   'epub3':           'epub3/chunk.xsl',
   }

SYSTEM=platform.system()
DIST=platform.linux_distribution()[0].strip()

if SYSTEM=="Linux":
   # Overwrite it
   MAINXMLCATALOG=MAINXMLCATALOG[SYSTEM]
   LOCALDBXSLPATH=getlocalpath(MAINXMLCATALOG, CANONICALURL)

else:
   raise OSError("Variable LOCALPATH in {0} for system '{1}' is unknown. " \
                 "Please set the correct path.".format(__file__, system))



#def pytest_runtest_setup(item):
   #"""called for running each test
   #"""
   #MYDIR=os.path.dirname(__file__)
   #if MYDIR not in sys.path:
      #sys.path.insert(0, MYDIR)


def pytest_report_header(config):
   """Present extra information
   http://pytest.org/latest/example/simple.html#adding-info-to-test-report-header
   """
   result=["",
           "Test cases for DocBook XSL Stylesheets",
           ""
          ]
   if config.option.verbose > 0:
      return result

# @pytest.fixture(scope="module")
def xmlparser(encoding=None, 
              attribute_defaults=False, 
              dtd_validation=False, 
              load_dtd=False, 
              no_network=True, 
              ns_clean=True, 
              recover=False, 
              # XMLSchema schema=None, 
              remove_blank_text=False, 
              resolve_entities=False, 
              remove_comments=False, 
              remove_pis=False, 
              strip_cdata=True, 
              target=None, 
              compact=True):
   """Pytest fixture: returns a XMLParser object
   """
   return etree.XMLParser(encoding=encoding,
                  attribute_defaults=attribute_defaults,
                  dtd_validation=dtd_validation,
                  load_dtd=load_dtd,
                  no_network=no_network,
                  ns_clean=ns_clean,
                  recover=recover,
                  remove_blank_text=remove_blank_text,
                  resolve_entities=resolve_entities,
                  remove_comments=remove_comments,
                  remove_pis=remove_pis,
                  strip_cdata=strip_cdata,
                  target=target,
                  compact=compact
                  )

@pytest.fixture
def xmlfile(request):
   """Pytest fixture: returns a list of files in the current directory
   """
   # print( ">>>#", request.fspath.dirname )
   path = os.path.join(request.fspath.dirname, "*.xml")
   return glob.glob(path)


@pytest.fixture(scope="module")
def namespaces():
   """Pytest fixture: returns a dictionary of common namespaces
   """
   return {'h':'http://www.w3.org/1999/xhtml'}


@pytest.fixture(scope="module")
def stylesheets():
   """Pytest fixture: returns a dictionary which maps formats to relative paths
   """
   return STYLESHEETS

# -------------------------

@pytest.fixture(scope="module")
def localdbxslpath():
   """Pytest fixture: returns the local path of the DocBook XSL stylesheets
   """
   return LOCALDBXSLPATH

# Taken from http://pytest.org/latest/example/simple.html#adding-info-to-test-report-header
def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item

def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" %previousfailed.name)


class XMLFile():
   def __init__(self, xmlfile,
               localdbxslpath=LOCALDBXSLPATH, 
               xmlparser=xmlparser(), 
               namespaces=namespaces()):
      self._xmlfile = xmlfile
      self._basexslt = localdbxslpath
      self._xmlparser = xmlparser
      self._ns = namespaces
      self._xslt = None
   
   def parse(self, xslt):
      self._xslt = os.path.join(self._basexslt, xslt)
      self._xmltree = etree.parse(self._xmlfile)
      self._xsltree = etree.parse(self._xslt)
      self._transform = etree.XSLT(self._xsltree)
   
   def transform(self, **kwargs):
      return self._transform(self._xmltree, **kwargs)
   
   @property
   def xml(self):
      return self._xmltree

   @property
   def xslt(self):
      return self._xslt
      
   @property
   def ns(self):
      return self._ns


@pytest.fixture()# scope="module"
def xmltestfile(request, xmlfile, localdbxslpath, xmlparser, namespaces):
   """Pytest fixture: return a XMLFile object which holds all the parsing and transformation logic
   """
   # print("****", request, xmlparser)
   return XMLFile(xmlfile[0], localdbxslpath, xmlparser, namespaces)


# EOF