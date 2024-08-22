# Copyright 2022-2023, IT Cell, Directorate of Treasuries & Accounts, Nagaland. All rights reserved.
import logging
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from DTAWebsite.settings import EMAIL_HOST_USER
from utils.crypto import AesCrypto
from utils.enums import LOGIN_REDIRECT, UserTypeEnum
from utils.file_upload import handle_uploaded_file
from utils.validations import validate_password, validate_role
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import os

from django.db.models.query_utils import Q
from administrator.forms import CaptchaForm, PasswordResetRequestForm, SetPasswordForm
from administrator.models import CustomUser, Contact, Designation, District, NewsEvent, PressRelease, Download, SliderImage, \
    PhotoGallery, VideoGallery, Department, Treasury, GrievanceCategory, Grievance, GrievanceResponse, DownloadCategory

logger = logging.getLogger(__name__)
User = get_user_model()


def Login(request):
    page_title = "CEO Nagaland | Login"
    template = "users/login.html"
    CaptchaForms = CaptchaForm()
    context = {'page_title': page_title, 'CaptchaForm': CaptchaForms}
    if request.method == "POST" and "submitForm" in request.POST:
        CaptchaForms = CaptchaForm(request.POST)
        if CaptchaForms.is_valid():
            username = request.POST['newUsername']
            password = request.POST['newPassword']
            usernameLength = int(request.POST['ul'])
            passwordLength = int(request.POST['pl'])
            key = request.POST['key']
            iv = request.POST['iv']
            aes = AesCrypto(key, iv)
            decryptedUsername = aes.decrypt(username)
            decryptedPassword = aes.decrypt(password)
            decryptedUsername = decryptedUsername[:usernameLength]
            decryptedPassword = decryptedPassword[:passwordLength]
            if user := authenticate(request, username=decryptedUsername, password=decryptedPassword):
                if user.user_type == UserTypeEnum.ADMIN.value:
                    login(request, user)
                    return redirect('/dashboard')
                else:
                    login(request, user)

                if destination := LOGIN_REDIRECT.get(user.user_type):
                    return redirect(destination)

            else:
                msg = 'Invalid username or password!'
                logger.error(msg)
                context['errormessage'] = msg
        else:
            context['errorCap'] = CaptchaForms.errors
    return render(request, template, context)


class AdminManagement:

    def __init__(self, user_type):
        self.user_type = user_type

    @validate_role
    def dashboard(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Dashboard"
        template = 'pages/admin/dashboard.html'
        context = {"dashboard": "nav-active", 'page_title': page_title}
        return render(request, template, context)

    @validate_role
    def district(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | District"
        template = 'pages/admin/district.html'
        context = {"master_expand": "nav-expanded", "district": "nav-active", 'page_title': page_title}
        if request.method == "POST":
            if "submit" in request.POST:
                name = request.POST.get("name")
                District(name=name).save()
                context['success'] = "Successfully submitted."

            elif "update" in request.POST:
                name = request.POST.get("name")
                district_code = request.POST.get("district_code_id")
                District.objects.filter(id=district_code).update(
                    name=name
                )
                context['success'] = "Successfully updated."

            elif "delete" in request.POST:
                district_id = request.POST.get("district_id")
                District.objects.filter(id=district_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = District.objects.filter(is_deleted=False).order_by('-id')
        return render(request, template, context)

    @validate_role
    def department(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Department"
        template = 'pages/admin/department.html'
        context = {"master_expand": "nav-expanded", "department": "nav-active", 'page_title': page_title}

        if request.method == "POST":
            if "submit" in request.POST:
                name = request.POST.get("name")
                Department(
                    name=name
                ).save()
                context['success'] = "Successfully submitted."

            elif "update" in request.POST:
                name = request.POST.get("name")
                department_id = request.POST.get("department_code_id")
                Department.objects.filter(id=department_id).update(
                    name=name
                )
                context['success'] = "Successfully updated."

            elif "delete" in request.POST:
                department_id = request.POST.get("department_id")
                Department.objects.filter(id=department_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = Department.objects.filter(is_deleted=False).order_by('-id')
        return render(request, template, context)

    @validate_role
    def treasury(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Treasury"
        template = 'pages/admin/treasury.html'
        context = {"master_expand": "nav-expanded", "treasury": "nav-active", 'page_title': page_title}

        if request.method == "POST":
            if "submit" in request.POST:
                name = request.POST.get("name")
                Treasury(
                    name=name
                ).save()
                context['success'] = "Successfully submitted."

            elif "update" in request.POST:
                name = request.POST.get("name")
                treasury_id = request.POST.get("treasury_code_id")
                Treasury.objects.filter(id=treasury_id).update(
                    name=name
                )
                context['success'] = "Successfully updated."

            elif "delete" in request.POST:
                treasury_id = request.POST.get("treasury_id")
                Treasury.objects.filter(id=treasury_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = Treasury.objects.filter(is_deleted=False).order_by('-id')
        return render(request, template, context)

    @validate_role
    def grievanceCategory(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Grievance Category"
        template = 'pages/admin/grievance_category.html'
        context = {"master_expand": "nav-expanded", "grievance_category": "nav-active", 'page_title': page_title}

        if request.method == "POST":
            if "submit" in request.POST:
                name = request.POST.get("name")
                GrievanceCategory(
                    name=name
                ).save()
                context['success'] = "Successfully submitted."

            elif "update" in request.POST:
                name = request.POST.get("name")
                grievance_category_id = request.POST.get("grievance_category_code_id")
                GrievanceCategory.objects.filter(id=grievance_category_id).update(
                    name=name
                )
                context['success'] = "Successfully updated."

            elif "delete" in request.POST:
                grievance_category_id = request.POST.get("grievance_category_id")
                GrievanceCategory.objects.filter(id=grievance_category_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = GrievanceCategory.objects.filter(is_deleted=False).order_by('-id')
        return render(request, template, context)

    @validate_role
    def grievance(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Grievance"
        template = 'pages/admin/grievance.html'
        district_list = District.objects.filter(is_deleted=False)
        department_list = Department.objects.filter(is_deleted=False)
        treasury_list = Treasury.objects.filter(is_deleted=False)
        grievance_category_list = GrievanceCategory.objects.filter(is_deleted=False)
        context = {
            "grievance": "nav-active",
            'page_title': page_title,
            'district_list': district_list,
            'department_list': department_list,
            'treasury_list': treasury_list,
            'grievance_category_list': grievance_category_list
        }

        if request.method == "POST":
            if "submit" in request.POST:
                grievance_kwargs = {
                    'date_filing': request.POST.get("date_filing"),
                    'time_filing': request.POST.get("time_filing"),
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
                    'recipient_id': request.user.id
                }
                Grievance.objects.create(**grievance_kwargs)
                context['success'] = "Successfully submitted."

            elif "update" in request.POST:
                grievance_id = request.POST.get("grievance_code_id")
                grievances_kwargs = {
                    'applicant_name': request.POST.get("applicant_name"),
                    'contact_no': request.POST.get("contact_no"),
                    'ppo_no': request.POST.get("ppo_no"),
                    'description': request.POST.get("description"),
                    'grievance_action': request.POST.get("grievance_action"),
                    'status': "Pending",
                    'district_id': request.POST.get("district"),
                    'department_id': request.POST.get("department"),
                    'grievance_category_id': request.POST.get("grievance_category"),
                    'treasury_id': request.POST.get("treasury")
                }
                Grievance.objects.filter(id=grievance_id).update(**grievances_kwargs)
                context['success'] = "Successfully updated."

            elif "delete" in request.POST:
                grievance_id = request.POST.get("grievance_id")
                Grievance.objects.filter(id=grievance_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = Grievance.objects.filter(is_deleted=False).order_by('-date_filing')
        return render(request, template, context)

    @validate_role
    def pressRelease(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Press Release"
        template = 'pages/admin/press_release.html'
        context = {"press_release_notification": "nav-active", 'page_title': page_title}

        if request.method == "POST":
            if "submit" in request.POST:
                title = request.POST.get("title")
                description = request.POST.get("description")
                publish_date = request.POST.get("publish_date")
                file_path = request.FILES.get('file_path', False)
                if file_path:
                    if file_path.name.lower().endswith('.pdf'):
                        if file_path.name.count('.') == 1:
                            doc_file_url = handle_uploaded_file('press_release', file_path)
                            doc_file_path = os.path.basename(doc_file_url)
                            PressRelease(
                                title=title,
                                description=description,
                                file_path=doc_file_path,
                                publish_date=publish_date
                            ).save()
                            context['success'] = "Successfully submitted."
                        else:
                            context['error'] = 'Invalid document file format!'
                    else:
                        context['error'] = 'Invalid document file format!'
                else:
                    PressRelease(
                        title=title,
                        description=description,
                        publish_date=publish_date
                    ).save()
                    context['success'] = "Successfully submitted."
            elif "update" in request.POST:
                press_release_id = request.POST.get("press_release_id")
                title = request.POST.get("title")
                description = request.POST.get("description")
                publish_date = request.POST.get("publish_date")
                file_path = request.FILES.get('file_path', False)
                if file_path:
                    if file_path.name.lower().endswith('.pdf'):
                        if file_path.name.count('.') == 1:
                            doc_file_url = handle_uploaded_file('press_release', file_path)
                            doc_file_path = os.path.basename(doc_file_url)
                            PressRelease.objects.filter(id=press_release_id).update(
                                title=title,
                                description=description,
                                file_path=doc_file_path,
                                publish_date=publish_date
                            )
                            context['success'] = "Successfully updated."
                        else:
                            context['error'] = 'Invalid document file format!'
                    else:
                        context['error'] = 'Invalid document file format!'
                else:
                    PressRelease.objects.filter(id=press_release_id).update(
                        title=title,
                        description=description,
                        publish_date=publish_date
                    )
                    context['success'] = "Successfully updated."
            elif "delete" in request.POST:
                press_id = request.POST.get("press_id")
                PressRelease.objects.filter(id=press_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = PressRelease.objects.filter(is_deleted=False).order_by('-id')
        return render(request, template, context)

    @validate_role
    def newsEvent(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | News & Events"
        template = 'pages/admin/news_event.html'
        context = {"news_event": "nav-active", 'page_title': page_title}
        if request.method == "POST":
            if "submit" in request.POST:
                title = request.POST.get("title")
                description = request.POST.get("description")
                publish_date = request.POST.get("publish_date")
                file_path = request.FILES.get('file_path', False)
                if file_path:
                    if file_path.name.lower().endswith(('.png','.jpg','.jpeg')):
                        if file_path.name.count('.') == 1:
                            if len(file_path) > 2097152:
                                context['error'] = 'File size is too big. It must be less than or equal to 2 mb.'
                            else:
                                doc_file_url = handle_uploaded_file('news', file_path)
                                doc_file_path = os.path.basename(doc_file_url)
                                NewsEvent(
                                    title=title,
                                    description=description,
                                    file_path=doc_file_path,
                                    uploaded_date=publish_date
                                ).save()
                                context['success'] = "Successfully submitted."
                        else:
                            context['error'] = 'Invalid document file format!'
                    else:
                        context['error'] = 'Invalid document file format!'
                else:
                    NewsEvent(
                        title=title,
                        description=description,
                        uploaded_date=publish_date
                    ).save()
                    context['success'] = "Successfully submitted."
            elif "delete" in request.POST:
                news_id = request.POST.get("news_id")
                NewsEvent.objects.filter(id=news_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = NewsEvent.objects.filter(is_deleted=False).order_by('-id')
        return render(request, template, context)

    @validate_role
    def photoGallery(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Photo Gallery"
        template = 'pages/admin/photo_gallery.html'
        context = {"gallery_slider": "nav-expanded", "photo_gallery": "nav-active", 'page_title': page_title}
        if request.method == "POST":
            if "submit" in request.POST:
                title = request.POST.get("title")
                description = request.POST.get("description")
                image_file = request.FILES['image_file']
                if image_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    if image_file.name.count('.') == 1:
                        if len(image_file) > 2097152:
                            context['error'] = 'Image size is too big. It must be less than or equal to 2 mb.'
                        else:
                            image_file_url = handle_uploaded_file('photo_gallery', image_file)
                            image_file_path = os.path.basename(image_file_url)
                            PhotoGallery(
                                title=title,
                                description=description,
                                image_path=image_file_path
                            ).save()
                            context['success'] = "Successfully submitted."
                    else:
                        context['error'] = 'Invalid image file format!'
                else:
                    context['error'] = 'Invalid image file format!'

            elif "update" in request.POST:
                photo_gallery_id = request.POST.get("photo_gallery_id")
                title = request.POST.get("title")
                description = request.POST.get("description")
                image_file = request.FILES.get('image_file', False)
                if image_file:
                    if image_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        if image_file.name.count('.') == 1:
                            if len(image_file) > 2097152:
                                context['error'] = 'Image size is too big. It must be less than or equal to 2 mb.'
                            else:
                                image_file_url = handle_uploaded_file('photo_gallery', image_file)
                                image_file_path = os.path.basename(image_file_url)
                                PhotoGallery.objects.filter(id=photo_gallery_id).update(
                                    title=title,
                                    description=description,
                                    image_path=image_file_path
                                )
                                context['success'] = "Successfully updated."
                        else:
                            context['error'] = 'Invalid image file format!'
                    else:
                        context['error'] = 'Invalid image file format!'
                else:
                    PhotoGallery.objects.filter(id=photo_gallery_id).update(
                        title=title,
                        description=description
                    )
                    context['success'] = "Successfully updated."

            elif "delete" in request.POST:
                photo_id = request.POST.get("photo_id")
                PhotoGallery.objects.filter(id=photo_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = PhotoGallery.objects.filter(is_deleted=False).order_by('-id')
        return render(request, template, context)

    @validate_role
    def videoGallery(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Video gallery"
        template = 'pages/admin/video_gallery.html'
        context = {"gallery_slider": "nav-expanded", "video_gallery": "nav-active", 'page_title': page_title}
        if request.method == "POST":
            if "submit" in request.POST:
                title = request.POST.get("title")
                description = request.POST.get("description")
                video_path = request.POST.get("video_path")
                VideoGallery(
                    title=title,
                    description=description,
                    video_path=video_path
                ).save()
                context['success'] = "Successfully submitted."

            elif "update" in request.POST:
                video_gallery_id = request.POST.get("video_gallery_id")
                title = request.POST.get("title")
                description = request.POST.get("description")
                video_path = request.POST.get("video_path")
                VideoGallery.objects.filter(id=video_gallery_id).update(
                    title=title,
                    description=description,
                    video_path=video_path
                )
                context['success'] = "Successfully updated."

            elif "delete" in request.POST:
                video_id = request.POST.get("video_id")
                VideoGallery.objects.filter(id=video_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = VideoGallery.objects.filter(is_deleted=False).order_by('-id')
        return render(request, template, context)

    @validate_role
    def sliderImage(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Slider Image"
        template = 'pages/admin/slider_image.html'
        context = {"gallery_slider": "nav-expanded", "slider_image": "nav-active", 'page_title': page_title}
        if request.method == "POST":
            if "submit" in request.POST:
                title = request.POST.get("title")
                slider_no = request.POST.get("slider_no")
                image_file = request.FILES['image_file']
                if image_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    if image_file.name.count('.') == 1:
                        if len(image_file) > 2097152:
                            context['error'] = 'Image size is too big. It must be less than or equal to 2 mb.'
                        else:
                            if SliderImage.objects.filter(slide_no=slider_no, is_deleted=False).exists():
                                context[
                                    'error'] = 'Slide no ' + slider_no + ' is already taken. Select different slide no.'
                            else:
                                image_file_url = handle_uploaded_file('slider', image_file)
                                image_file_path = os.path.basename(image_file_url)
                                SliderImage(
                                    title=title,
                                    slide_no=slider_no,
                                    image_path=image_file_path
                                ).save()
                                context['success'] = "Successfully submitted."
                    else:
                        context['error'] = 'Invalid image file format!'
                else:
                    context['error'] = 'Invalid image file format!'

            elif "update" in request.POST:
                slider_no_id = request.POST.get("slider_no_id")
                title = request.POST.get("title")
                slider_no = request.POST.get("slider_no")
                image_file = request.FILES.get('image_file', False)
                if image_file:
                    if image_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        if image_file.name.count('.') == 1:
                            if len(image_file) > 2097152:
                                context['error'] = 'Image size is too big. It must be less than or equal to 2 mb.'
                            else:
                                if SliderImage.objects.filter(slide_no=slider_no, is_deleted=False).exclude(
                                        id=slider_no_id).exists():
                                    context[
                                        'error'] = 'Slide no ' + slider_no + ' is already taken. Select different slide no.'
                                else:
                                    image_file_url = handle_uploaded_file('slider', image_file)
                                    image_file_path = os.path.basename(image_file_url)
                                    SliderImage.objects.filter(id=slider_no_id).update(
                                        title=title,
                                        slide_no=slider_no,
                                        image_path=image_file_path
                                    )
                                    context['success'] = "Successfully updated."
                        else:
                            context['error'] = 'Invalid image file format!'
                    else:
                        context['error'] = 'Invalid image file format!'
                else:
                    if SliderImage.objects.filter(slide_no=slider_no, is_deleted=False).exclude(
                            id=slider_no_id).exists():
                        context['error'] = 'Slide no ' + slider_no + ' is already taken. Select different slide no.'
                    else:
                        SliderImage.objects.filter(id=slider_no_id).update(
                            title=title,
                            slide_no=slider_no
                        )
                        context['success'] = "Successfully updated."

            elif "delete" in request.POST:
                slide_id = request.POST.get("slider_id")
                SliderImage.objects.filter(id=slide_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = SliderImage.objects.filter(is_deleted=False).order_by('slide_no')
        return render(request, template, context)

    @validate_role
    def downloadCategory(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Download Category"
        template = 'pages/admin/download_category.html'
        context = {"master_expand": "nav-expanded", "download_category": "nav-active", 'page_title': page_title}

        if request.method == "POST":
            if "submit" in request.POST:
                name = request.POST.get("name")
                DownloadCategory(
                    name=name
                ).save()
                context['success'] = "Successfully submitted."

            elif "update" in request.POST:
                name = request.POST.get("name")
                download_category_id = request.POST.get("download_category_code_id")
                DownloadCategory.objects.filter(id=download_category_id).update(
                    name=name
                )
                context['success'] = "Successfully updated."

            elif "delete" in request.POST:
                download_category_id = request.POST.get("download_category_id")
                DownloadCategory.objects.filter(id=download_category_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = DownloadCategory.objects.filter(is_deleted=False).order_by('-id')
        return render(request, template, context)

    @validate_role
    def download(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Download"
        template = 'pages/admin/download.html'
        download_category = DownloadCategory.objects.filter(is_deleted=False)
        context = {"download_expand": "nav-expanded", "download": "nav-active", 'page_title': page_title, "download_category": download_category}
        if request.method == "POST":
            if "submit" in request.POST:
                title = request.POST.get("title")
                download_type = request.POST.get("type")
                file_path = request.FILES['file_path']
                if file_path.name.lower().endswith('.pdf'):
                    if file_path.name.count('.') == 1:
                        if len(file_path) > 5197152:
                            context['error'] = 'File size is too big. It must be less than or equal to 5 mb.'
                        else:
                            doc_file_url = handle_uploaded_file('download', file_path)
                            doc_file_path = os.path.basename(doc_file_url)
                            Download(
                                title=title,
                                download_category_id=download_type,
                                file_path=doc_file_path
                            ).save()
                            context['success'] = "Successfully submitted."
                    else:
                        context['error'] = 'Invalid document file format!'
                else:
                    context['error'] = 'Invalid document file format!'

            elif "update" in request.POST:
                download_id = request.POST.get("update_download_id")
                title = request.POST.get("title")
                download_type = request.POST.get("type")
                file_path = request.FILES.get('file_path', False)
                if file_path:
                    if file_path.name.lower().endswith('.pdf'):
                        if file_path.name.count('.') == 1:
                            if len(file_path) > 22197152:
                                context['error'] = 'File size is too big. It must be less than or equal to 20 mb.'
                            else:
                                doc_file_url = handle_uploaded_file('download', file_path)
                                doc_file_path = os.path.basename(doc_file_url)
                                Download.objects.filter(id=download_id).update(
                                    title=title,
                                    download_category_id=download_type,
                                    file_path=doc_file_path
                                )
                                context['success'] = "Successfully updated."
                        else:
                            context['error'] = 'Invalid document file format!'
                    else:
                        context['error'] = 'Invalid document file format!'
                else:
                    Download.objects.filter(id=download_id).update(
                        title=title
                    )
                    context['success'] = "Successfully updated."

            elif "delete" in request.POST:
                download_id = request.POST.get("download_id")
                Download.objects.filter(id=download_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = Download.objects.filter(is_deleted=False).order_by('-id')
        return render(request, template, context)

    @validate_role
    def designation(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Designation"
        template = 'pages/admin/designation.html'
        context = {"master_expand": "nav-expanded", "designation": "nav-active", 'page_title': page_title}

        if request.method == "POST":
            if "submit" in request.POST:
                name = request.POST.get("name")
                Designation(
                    name=name
                ).save()
                context['success'] = "Successfully submitted."

            elif "update" in request.POST:
                name = request.POST.get("name")
                designation_id = request.POST.get("designation_code_id")
                Designation.objects.filter(id=designation_id).update(
                    name=name
                )
                context['success'] = "Successfully updated."

            elif "delete" in request.POST:
                designation_id = request.POST.get("designation_id")
                Designation.objects.filter(id=designation_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = Designation.objects.filter(is_deleted=False).order_by('-id')
        return render(request, template, context)
    
    @validate_role
    def contactDetail(self, request):
        page_title = "Directorate of Treasuries & Accounts, Nagaland | Contact Details"
        template = 'pages/admin/contact.html'
        designation_list = Designation.objects.filter(is_deleted=False).order_by('id')
        context = {"who_who": "nav-active", 'page_title': page_title, 'designation_list': designation_list}
        if request.method == "POST":
            if "submit" in request.POST:
                name = request.POST.get("name")
                designation = request.POST.get("designation")
                contact_no = request.POST.get("contact_no")
                email = request.POST.get("email")

                Contact(
                    name=name,
                    designation_id=designation,
                    contact_no=contact_no,
                    email=email
                ).save()
                context['success'] = "Successfully submitted."

            elif "update" in request.POST:
                contact_id = request.POST.get("update_contact_id")
                name = request.POST.get("name")
                designation = request.POST.get("designation")
                contact_no = request.POST.get("contact_no")
                email = request.POST.get("email")

                Contact.objects.filter(id=contact_id).update(
                    name=name,
                    designation_id=designation,
                    contact_no=contact_no,
                    email=email
                )
                context['success'] = "Successfully updated."

            elif "delete" in request.POST:
                contact_id = request.POST.get("contact_id")
                Contact.objects.filter(id=contact_id).update(is_deleted=True)
                context['success'] = "Successfully Deleted."
        context['data'] = Contact.objects.filter(is_deleted=False).order_by('-id')
        return render(request, template, context)

    @validate_role
    def userManagement(self, request):
        template = 'users/user_management.html'
        page_title = 'Directorate of Treasuries & Accounts, Nagaland | User Management'
        district_list = District.objects.filter(is_deleted=False)
        treasury_list = Treasury.objects.filter(is_deleted=False)
        context = {'master_expand': 'nav-expanded', 'page_title': page_title,
                   'user_management': 'nav-active', 'district_list': district_list, 'treasury_list': treasury_list}
        if request.method == "POST":
            name = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            designation = request.POST.get('designation')
            mobile_no = request.POST.get('mobile_no')
            treasury_id = request.POST.get('treasury')
            district_id = request.POST.get('district')
            password = request.POST.get('password')
            confirm_password = request.POST.get('Confirm_password')

            if "create_user" in request.POST:
                user_type = request.POST.get('user_type')
                check_password = validate_password(password, confirm_password)
                if not check_password['status']:
                    context['error'] = check_password['message']
                else:
                    if CustomUser.objects.filter(username=name).exists():
                        context['error'] = 'Same username already exist!'
                    else:
                        CustomUser.objects.create_user(user_type=user_type, username=name, district_id=district_id, treasury_id=treasury_id,
                                                  password=password, is_staff=True, is_active=True, first_name=first_name, last_name=last_name, mobile_no=mobile_no, designation=designation).save()
                        context['success'] = 'Successfully Created.'

            elif "update_user" in request.POST:
                code = request.POST.get('code')
                if CustomUser.objects.filter(username=name).exclude(id=code).exists():
                    context['error'] = 'Same username already exist!'
                else:
                    get_data = CustomUser.objects.filter(id=code).first()
                    get_data.first_name = first_name
                    get_data.last_name = last_name
                    get_data.designation = designation
                    get_data.mobile_no = mobile_no
                    get_data.save()
                    context['success'] = 'Successfully Updated.'

            elif "delete" in request.POST:
                code = request.POST.get('code')
                get_data = CustomUser.objects.filter(id=code).first()
                get_data.is_active = False
                get_data.save()
                context['success'] = 'Successfully Deleted.'

        context['user_list'] = CustomUser.objects.filter(is_active=True).all().order_by('id')
        return render(request, template, context)


def userProfile(request):
    template = 'users/user_profile.html'
    page_title = 'DTA Nagaland | User Profile'
    form = PasswordChangeForm(request.user)
    context = {'master_expand': 'nav-expanded', 'page_title': page_title, 'user_management': 'nav-active', 'form': form}
    if request.method == "POST":

        new_password = request.POST.get('new_password1')
        new_password1 = request.POST.get('new_password1')
        check_password = validate_password(new_password, new_password1)
        if not check_password['status']:
            context['msg'] = check_password['message']
            context['error_status'] = check_password['status']
        else:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                context['msg'] = 'Successfully Updated.'
            else:
                context['errormsg'] = form
    return render(request, template, context)


class ResetPasswordRequestView(FormView):
    template_name = "users/forgot_password_template.html"
    success_url = '/reset_password/'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        # This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        # A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_or_username"]

        if self.validate_email_address(data) is True:
            # If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.

            associated_users = User.objects.filter(Q(email=data) | Q(username=data))
        else:
            # If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.

            associated_users = User.objects.filter(username=data)
        if associated_users.exists():
            subject_template_name = 'users/password_reset_subject.txt'
            email_template_name = 'users/password_reset_email.html'
            for user in associated_users:
                c = {
                    'email': user.email,
                    'domain': request.META['HTTP_HOST'],
                    'site_name': 'CEO',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                subject = loader.render_to_string(subject_template_name, c)
                # Email subject *must not* contain newlines
                subject = ''.join(subject.splitlines())
                email = loader.render_to_string(email_template_name, c)
                send_mail(subject, email, EMAIL_HOST_USER, [user.email], fail_silently=False)
            result = self.form_valid(form)
            messages.success(request, 'Your password reset is in progress, please check your email for further details')
            return result
        result = self.form_invalid(form)
        messages.error(request, 'Your password reset is in progress, please check your email for further details')
        return result


class PasswordResetConfirmView(FormView):
    template_name = "users/reset_password.html"
    success_url = '/login/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        # View that checks the hash in a password reset link and presents a
        # form for entering a new password.
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been successful.')
                return self.form_invalid(form)
        else:
            messages.error(request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)


def Logout(request):
    logout(request)
    return redirect('login')
