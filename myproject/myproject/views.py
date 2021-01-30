from django.shortcuts import render
from urllib.request import urlopen
from bs4 import BeautifulSoup
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from entries.models import Entry
import threading
import xml.etree.ElementTree as ET
from django.core.mail import send_mail

def check_changes():
    """
        A function to check every entry for any change when the app starts
        Updates the entry_xml if entry at the database differs from the link's content
    """
    all_entries = Entry.objects.all()

    for user_entry in all_entries:
        req = urlopen(user_entry.entry_link)
        soup = BeautifulSoup(req, 'lxml')
        content = soup.prettify()

        # IF THERE IS A CHANGE, UPDATE THE ENTRY
        if content != user_entry.entry_xml:
            the_entry = Entry.objects.get(id=user_entry.id)
            the_entry.entry_xml = content
            the_entry.save()
    return


def check_syntax(link):
    """
        A function to check the syntax of the xml file accessed in the link
        Returns False if there are no errors
        Returns Exception if there are errors
    """
    try:
        parser = make_parser( )
        parser.setContentHandler(ContentHandler(  ))
        parser.parse(link)
        return False
    except Exception as e:
        return e


def processUrl(request):
    """
        A function to process the xml file accessed in the link
        Sends failure email if there check_syntax() returns exception
        Creates Entry object, iterates,
        Changes the XML and sends email for a given word if  check_syntax() returns False
    """
    link = request.POST['link-url']
    user_email = request.POST['email']
    change_word = request.POST['change-word'].strip()
    change_to = request.POST['change-to'].strip()
    errors = check_syntax(link)

    if errors:
        ## SEND FAILURE EMAIL
        send_mail(
            "Your XML Input Failed",
            str(errors),
            "mehmettest@gmail.com",
            [user_email],
        )
        
    else:
        # GET XML CONTENT
        req = urlopen(link)
        soup = BeautifulSoup(req, 'lxml')
        content = soup.prettify()

        # CREATE AN ENTRY OBJECT FOR THE INPUT
        Entry.objects.create(user=request.user, entry_xml=content, entry_link=link)

        # SAVE XML CONTENT AND CONVERT TO A TREE
        f = open("sample.xml", "w")
        f.write(content)
        f.close()

        tree = ET.parse('sample.xml')
        count = 0

        # ITERATE OVER EACH ELEMENT IN THE TREE
        for child in tree.iter():
            if change_word in child.text:
                child.text = change_to
                count += 1

        tree.write("res.xml")

        # SEND CHANGE WORD RESULTS MAIL
        send_mail(
            "Your change result",
            "Due to your word change {} field(s) have been succesfully changed from {} to {} .".format(count, change_word, change_to),
            "mehmettest@gmail.com",
            [user_email],
        )

    return 


def home(request):
    '''
        The main home view for the django app
        Runs check_changes() when called for the first time
        Handles the submitted user input form
    '''
    th = threading.Thread(target=check_changes,
                        args=()
                        )
    th.setDaemon(True)
    th.start()
    
    if request.method == "POST":
        t = threading.Thread(target=processUrl,
                            args=(request,)
                            )
        t.setDaemon(True)
        t.start()

    return render( request, 'home.html', {})
    