from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def info(request):
    return render(request, 'info.html')

def about(request):
    return render(request, 'about.html')

def project(request):
    return render(request, 'project.html')

def launch_schedule(request):
    return render(request, 'launch_schedule.html')

def contact(request):
    return render(request, 'contact.html')
