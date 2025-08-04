from django.http import HttpResponse
from django.shortcuts import render

def aboutus(request):
    return HttpResponse("This is the about us page.")

def home(request):
    data = {
        'title':'Home',
        'bdata':'Welcome to the world of Django!!!'
    }
    return render(request, "index.html",data)  # Render the index.html template

def course(request):
    return HttpResponse("<b>This is Course page..</b>")

def course_detail(request, course_id):
    return HttpResponse(f"<b>This is Course Detail page for course {course_id}..</b>")