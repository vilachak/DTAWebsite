# Copyright 2022-2023, IT Cell, Directorate of Treasuries & Accounts, Nagaland. All rights reserved.
from django.shortcuts import render
from datetime import datetime
from administrator.forms import CaptchaForm
from administrator.models import Contact, CustomUser, Department, District, Download, DownloadCategory, Grievance, \
    GrievanceCategory, NewsEvent, PhotoGallery, SliderImage, Treasury, VideoGallery, Advertisement, PressRelease


def home(request):
    page_title = "DTA, Nagaland | Home"
    news_events = NewsEvent.objects.filter(is_deleted=False).order_by('-id')[:3]
    notification_list = PressRelease.objects.filter(is_deleted=False).order_by('-id')[:5]
    advertisement_list = Advertisement.objects.filter(is_deleted=False).order_by('-id')[:5]
    download_list = Download.objects.filter(is_deleted=False).order_by('-id')[:5]
    download_type = download_list.first()
    slider_list = SliderImage.objects.filter(is_deleted=False).order_by('slide_no')
    context = {
        "home": "active",
        "page_title": page_title,
        "news_events": news_events,
        'notification': notification_list,
        'advertisement': advertisement_list,
        'download': download_list,
        'slider_list':slider_list,
        'download_type': download_type.download_category.name
        }
    template = 'pages/home.html'
    return render(request, template, context)


def about(request):
    page_title = "DTA, Nagaland | About"
    context = {"about": "active", "page_title": page_title}
    template = 'pages/about.html'
    return render(request, template, context)


def who(request):
    page_title = "DTA, Nagaland | Who's Who"
    context = {
        "who_who": "active",
        "page_title": page_title,
        "contact_list": Contact.objects.filter(is_deleted=False).order_by('designation')
        }
    template = 'pages/who.html'
    return render(request, template, context)


def news(request):
    page_title = "DTA, Nagaland | News & Events"
    news_events = NewsEvent.objects.filter(is_deleted=False).order_by('-id')[:15]
    try:
        news_id = request.GET["id"]
    except:
        news_id = '0'
    if news_id == '0':
        single_news_events = NewsEvent.objects.filter(is_deleted=False).order_by('-id')[:1].first()
    else:
        single_news_events = NewsEvent.objects.filter(id=news_id).first()
    context = {
        "news_events": "active",
        "page_title": page_title,
        "single_news_events": single_news_events,
        "news_events": news_events
        }
    template = 'pages/news_events.html'
    return render(request, template, context)


def photogallery(request):
    page_title = "DTA, Nagaland | Photo Gallery"
    context = {
        "gallery": "active",
        "page_title": page_title,
        "photo_gallery": "active",
        "photo_data": PhotoGallery.objects.filter(is_deleted=False)
        }
    template = 'pages/photo_gallery.html'
    return render(request, template, context)


def videogallery(request):
    page_title = "DTA, Nagaland | Video Gallery"
    context = {
        "gallery": "active",
        "page_title": page_title,
        "video_gallery": "active",
        "video_gallery_data": VideoGallery.objects.filter(is_deleted=False)
        }
    template = 'pages/video_gallery.html'
    return render(request, template, context)


def contact(request):
    page_title = "DTA, Nagaland | Contact"
    context = {
        "contact": "active",
        "page_title": page_title}
    template = 'pages/contact.html'
    return render(request, template, context)


def download(request):
    page_title = "DTA, Nagaland | Download"
    download_category = DownloadCategory.objects.filter(is_deleted=False)
    try:
        file_type = request.GET["type"]
    except:
        file_type = 'NA'
    download_id = 0
    if download_cat := DownloadCategory.objects.filter(name=file_type).first():
        download_id = download_cat.id
    download_list = Download.objects.filter(is_deleted=False, download_category_id=download_id)
    context = {"download": "active", "page_title": page_title, 'file_type': file_type, 'download_list': download_list, 'download_category': download_category}
    template = 'pages/download.html'

    return render(request, template, context)


def advertisement(request):
    page_title = "DTA, Nagaland | Advertisement"
    advertisement_list = Advertisement.objects.filter(is_deleted=False).order_by('-id')[:20]
    context = {"advertisement": "active", "page_title": page_title, 'advertisement_list': advertisement_list}
    template = 'pages/advertisement.html'

    return render(request, template, context)


def notification(request):
    page_title = "DTA, Nagaland | Notification"
    notification_list = PressRelease.objects.filter(is_deleted=False).order_by('-id')[:20]
    context = {"notification": "active", "page_title": page_title, 'notification_list': notification_list}
    template = 'pages/notification.html'

    return render(request, template, context)


def grievance(request):
    page_title = "DTA, Nagaland | Grievance"
    template = 'pages/grievance.html'
    district_list = District.objects.filter(is_deleted=False)
    department_list = Department.objects.filter(is_deleted=False)
    treasury_list = Treasury.objects.filter(is_deleted=False)
    grievance_category_list = GrievanceCategory.objects.filter(is_deleted=False)
    context = {
        "grievance": "active",
        'page_title': page_title,
        'district_list': district_list,
        'department_list': department_list,
        'treasury_list': treasury_list,
        'grievance_category_list': grievance_category_list,
        'CaptchaForms': CaptchaForm()
    }
    
    if request.method == "POST":
        if "submit" in request.POST:
            # Get treasury user from Id
            if treasury_user := CustomUser.objects.filter(is_active=True, treasury_id=request.POST.get("treasury")).order_by('-id').first():
                recipient_id = treasury_user.id
            else:
                treasury_user = CustomUser.objects.filter(is_active=True, user_type="ADMIN").order_by('-id').first()
                recipient_id = treasury_user.id
            grievance_kwargs = {
                'date_filing': datetime.now(),
                'applicant_name': request.POST.get("applicant_name"),
                'contact_no': request.POST.get("contact_no"),
                'ppo_no': request.POST.get("ppo_no"),
                'description': request.POST.get("description"),
                'grievance_action': request.POST.get("grievance_action"),
                'status': "Pending",
                'district_id': request.POST.get("district"),
                'department_id': request.POST.get("department"),
                'grievance_category_id': request.POST.get("grievance_category"),
                'treasury_id': request.POST.get("treasury"),
                'recipient_id': recipient_id
            }
            CaptchaForms = CaptchaForm(request.POST)
            if CaptchaForms.is_valid():
                Grievance.objects.create(**grievance_kwargs)
                context['success'] = "Successfully submitted."
            else:
                context['grievance_data'] = grievance_kwargs
                context['errorCap'] = "Invalid CAPTCHA"

        elif "search" in request.POST:
            contact_no = request.POST.get("contact_no")
            if g_data := Grievance.objects.filter(is_deleted=False, contact_no=contact_no).first():
                context['grievance_detail'] = g_data
            else:
                context['not_found'] = "Data not found!"
            context['contact_no'] = contact_no
                
    return render(request, template, context)


def site_map(request):
    page_title = "DTA, Nagaland | Site Map"
    context = {"site_map": "active", "page_title": page_title}
    template = 'pages/site_map.html'
    return render(request, template, context)


def screen_reader(request):
    page_title = "DTA, Nagaland | Screen Reader"
    context = {"screen_reader": "active", "page_title": page_title}
    template = 'pages/screen_reader.html'
    return render(request, template, context)
