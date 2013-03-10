

import urllib2
from bs4 import BeautifulSoup


def catch_url( url ):
  content = urllib2.urlopen( url )
  soup = BeautifulSoup( content )
  return soup