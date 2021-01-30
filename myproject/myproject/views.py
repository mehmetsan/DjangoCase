from django.shortcuts import render

from urllib.request import urlopen
from bs4 import BeautifulSoup, element
import selenium

from xml.sax.handler import ContentHandler
from xml.sax import make_parser

from lxml import etree

import xml.etree.ElementTree as ET

def check_syntax(elements):
    try:
        parser = make_parser( )
        parser.setContentHandler(ContentHandler(  ))
        parser.parse(elements)
        print ("{} is well-formed".format("Your doc is ") )
    except Exception as e:
        print ("{} is NOT well-formed! {}".format("Your doc is ", e))

def home(request):

    if request.method == "POST":
        link = request.POST['link-url']
        print(link)

        req = urlopen(link)

        soup = BeautifulSoup(req, 'lxml')

        '''       
        f = open("sample.xml", "w")
        f.write(soup.prettify())
        f.close()
        '''

        file = open('sample.xml',mode='r')
        xslt_content  = file.read()


        #tree = ET.parse('sample.xml')

        #print(type(tree))

        link = "https://www.w3schools.com/xml/plant_catalog.xml"
        check_syntax(link)


        elements = soup.find_all()

        content = soup.prettify()

    #        content.decode('utf-8').encode('ascii')
     #   doc = etree.fromstring(content)



        return render( request, 'home.html', {'data':content})
    return render( request, 'home.html', {})
    