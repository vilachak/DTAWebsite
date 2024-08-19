# Copyright 2022-2023, IT Cell, Directorate of Treasuries & Accounts, Nagaland. All rights reserved.
from django.shortcuts import render


# Create your views here.
def home(request):
    page_title = "DTA, Nagaland | Home"
    context = {"home": "active","page_title":page_title}
    template = 'pages/home.html'
    return render(request, template, context)


def about(request):
    page_title = "DTA, Nagaland | About"
    context = {"about": "active","page_title":page_title}
    template = 'pages/about.html'
    return render(request, template, context)
 
def who(request):
    page_title = "DTA, Nagaland | Who's Who"
    context = {"who_who": "active","page_title":page_title}
    template = 'pages/who.html'
    return render(request, template, context)

def news(request):
    page_title = "DTA, Nagaland | News & Events"
    context = {"news_events": "active","page_title":page_title}
    template = 'pages/news_events.html'
    return render(request, template, context)

def photogallery(request):
    page_title = "DTA, Nagaland | Photo Galleery"
    context = {"gallery": "active","page_title":page_title}
    template = 'pages/photo_gallery.html'
    return render(request, template, context)

def videogallery(request):
    page_title = "DTA, Nagaland | Video Galleery"
    context = {"gallery": "active","page_title":page_title}
    template = 'pages/video_gallery.html'
    return render(request, template, context)

def contact(request):
    page_title = "DTA, Nagaland | Contact"
    context = {"contact": "active","page_title":page_title}
    template = 'pages/contact.html'
    return render(request, template, context)

def apar(request):
    page_title = "DTA, Nagaland | APAR"
    context = {"download": "active","page_title":page_title}
    template = 'pages/apar.html'
    return render(request, template, context)

def rti(request):
    page_title = "DTA, Nagaland | RTI"
    context = {"download": "active","page_title":page_title}
    template = 'pages/rti.html'
    return render(request, template, context)

def gpf(request):
    page_title = "DTA, Nagaland | GPF"
    context = {"download": "active","page_title":page_title}
    template = 'pages/gpf.html'
    return render(request, template, context)

def pension(request):
    page_title = "DTA, Nagaland | Pensionm"
    context = {"download": "active","page_title":page_title}
    template = 'pages/pension.html'
    return render(request, template, context)

def grievance(request):
    page_title = "DTA, Nagaland | Grievance"
    context = {"grievance": "active","page_title":page_title}
    template = 'pages/grievance.html'
    return render(request, template, context)

def site_map(request):
    page_title = "DTA, Nagaland | Site Map"
    context = {"site_map": "active","page_title":page_title}
    template = 'pages/site_map.html'
    return render(request, template, context)

def screen_reader(request):
    page_title = "DTA, Nagaland | Screen Reader"
    context = {"screen_reader": "active","page_title":page_title}
    template = 'pages/screen_reader.html'
    return render(request, template, context)