from django.shortcuts import render

def home(request):

    if request.method == "POST":
        link = request.POST['link-url']
        print(link)
    return render( request, 'home.html', {})