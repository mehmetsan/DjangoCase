from django.shortcuts import render
from urllib.request import urlopen
from bs4 import BeautifulSoup
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from entries.models import Entry

def check_syntax(link):
    try:
        parser = make_parser( )
        parser.setContentHandler(ContentHandler(  ))
        parser.parse(link)
        print ("{} is well-formed".format("Your doc is ") )
        return False
    except Exception as e:
        print ("{} is NOT well-formed! {}".format("Your doc is ", e))
        return e

def home(request):
    content = ""

    if request.method == "POST":
        link = request.POST['link-url']
        errors = check_syntax(link)

        if errors:
            ## SEND EMAIL
            pass
        else:
            # SAVE THE FILE
            req = urlopen(link)
            soup = BeautifulSoup(req, 'lxml')

            content = soup.prettify()
       
            f = open("sample.xml", "w")
            f.write(content)
            f.close()

            Entry.objects.create(user=request.user, entry_xml=content, entry_link=link)
        

        return render( request, 'home.html', {'data':content})
    return render( request, 'home.html', {})
    