from django.shortcuts import render
from urllib.request import urlopen
from bs4 import BeautifulSoup
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from entries.models import Entry
import threading


from django.core.mail import send_mail

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


def processUrl(request):
    content = ""
    link = request.POST['link-url']
    user_email = request.POST['email']
    errors = check_syntax(link)

    if errors:
        ## SEND EMAIL
        send_mail(
            "Your XML Input Failed",
            str(errors),
            "mehmettest@gmail.com",
            [user_email],
        )
        return False
        
    else:
        # SAVE THE FILE
        req = urlopen(link)
        soup = BeautifulSoup(req, 'lxml')

        content = soup.prettify()
    
        f = open("sample.xml", "w")
        f.write(content)
        f.close()

        Entry.objects.create(user=request.user, entry_xml=content, entry_link=link)
        return True 



def home(request):
    
    if request.method == "POST":
        t = threading.Thread(target=processUrl,
                            args=(request,)
                            )
        t.setDaemon(True)
        t.start()


        return render( request, 'home.html', {})
    return render( request, 'home.html', {})
    