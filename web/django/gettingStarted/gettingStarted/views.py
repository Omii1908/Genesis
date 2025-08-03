from django.http import HttpResponse

def aboutus(request):
    return HttpResponse("This is the about us page.")

def home(request):
    return HttpResponse("<b>This is Home page..</b>")

def course(request):
    return HttpResponse("<b>This is Course page..</b>")

def course_detail(request, course_id):
    return HttpResponse(f"<b>This is Course Detail page for course {course_id}..</b>")