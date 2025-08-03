from django.http import HttpResponse

def aboutus(request):
    return HttpResponse("This is the about us page.")

def home(request):
    return HttpResponse("<b>This is Home page..</b>")