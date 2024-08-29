# Copyright 2022-2023, IT Cell, Directorate of Treasuries & Accounts, Nagaland. All rights reserved.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class TimeStamped(models.Model):
    created_at = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=False, null=True)

    class Meta:
        abstract = True


class District(TimeStamped):
    name = models.CharField(max_length=150, null=False)


class Department(TimeStamped):
    name = models.CharField(max_length=150, null=False)


class Treasury(TimeStamped):
    name = models.CharField(max_length=150, null=False)


class GrievanceCategory(TimeStamped):
    name = models.CharField(max_length=150, null=False)


class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, default="ADMIN")
    mobile_no = models.CharField(max_length=10, null=True)
    designation = models.CharField(max_length=150, null=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='custom_user', null=True)
    treasury = models.ForeignKey(Treasury, on_delete=models.PROTECT, related_name='custom_user', null=True)


class Grievance(TimeStamped):
    date_filing = models.DateField()
    time_filing = models.TimeField(auto_now=True)
    applicant_name = models.CharField(max_length=150)
    ppo_no = models.CharField(max_length=50, null=True)
    contact_no = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True)
    grievance_action = models.TextField(null=True)
    date_first = models.DateField(null=True)
    date_second = models.DateField(null=True)
    date_final = models.DateField(null=True)
    status = models.CharField(max_length=20, null=True)  # Pending, Completed, Ongoing

    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='grievance')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='grievance')
    grievance_category = models.ForeignKey(GrievanceCategory, on_delete=models.PROTECT, related_name='grievance')
    treasury = models.ForeignKey(Treasury, on_delete=models.PROTECT, related_name='grievance')
    recipient = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='grievance')


class GrievanceResponse(TimeStamped):
    action_taken = models.TextField(null=True)

    action_taken_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='grievance_response')
    grievance = models.ForeignKey(Grievance, on_delete=models.PROTECT, related_name='grievance_response')


class SliderImage(TimeStamped):
    slide_no = models.IntegerField(default=0)
    title = models.CharField(max_length=150, unique=True)
    image_path = models.CharField(max_length=150, unique=True)


class PressRelease(TimeStamped):
    title = models.CharField(max_length=150)
    description = models.TextField()
    file_path = models.CharField(max_length=150, null=True, blank=True)
    publish_date = models.DateField()


class Advertisement(TimeStamped):
    title = models.CharField(max_length=150)
    description = models.TextField()
    file_path = models.CharField(max_length=150, null=True, blank=True)
    publish_date = models.DateField()


class NewsEvent(TimeStamped):
    title = models.CharField(max_length=150, null=False)
    description = models.TextField(null=False)
    file_path = models.CharField(max_length=150, null=True, blank=True)
    uploaded_date = models.DateField(null=True)


class PhotoGallery(TimeStamped):
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    image_path = models.CharField(max_length=150, null=True, blank=True)


class VideoGallery(TimeStamped):
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    video_path = models.CharField(max_length=150, null=True, blank=True)


class DownloadCategory(TimeStamped):
    name = models.CharField(max_length=150, null=False)


class Download(TimeStamped):
    title = models.CharField(max_length=150)
    uploaded_date = models.DateField(null=True)
    file_path = models.CharField(max_length=150, null=True, blank=True)

    download_category = models.ForeignKey(DownloadCategory, on_delete=models.PROTECT, related_name='download')


class Designation(TimeStamped):
    name = models.CharField(max_length=150, null=False)


class Contact(TimeStamped):
    name = models.CharField(max_length=150, null=True, blank=True)
    contact_no = models.CharField(max_length=150, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)

    designation = models.ForeignKey(Designation, on_delete=models.PROTECT, related_name='contact')
