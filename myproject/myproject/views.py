from django.shortcuts import render
from urllib.request import urlopen
from bs4 import BeautifulSoup
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from entries.models import Entry
import threading
import xml.etree.ElementTree as ET


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
    change_word = request.POST['change-word'].strip()
    change_to = request.POST['change-to'].strip()

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

        Entry.objects.create(user=request.user, entry_xml=content, entry_link=link)

        f = open("sample.xml", "w")
        f.write(content)
        f.close()

        tree = ET.parse('sample.xml')
        count = 0

        for child in tree.iter():
            if change_word in child.text:
                child.text = change_to
                count += 1

        tree.write("res.xml")

        # SEND CHANGE RESULT MAIL
        send_mail(
            "Your change result",
            "Due to your word change {} field(s) have been succesfully changed from {} to {} .".format(count, change_word, change_to),
            "mehmettest@gmail.com",
            [user_email],
        )
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
    