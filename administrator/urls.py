# Copyright 2022-2023, IT Cell, Directorate of Treasuries & Accounts, Nagaland. All rights reserved.
from django.urls import include, path, re_path

from administrator.views import Login, Logout, PasswordResetConfirmView, ResetPasswordRequestView, AdminManagement, userProfile
from utils.enums import UserTypeEnum

urlpatterns = [
    path('dashboard', AdminManagement([UserTypeEnum.ADMIN]).dashboard, name='dashboard'),
    path('admin-district', AdminManagement([UserTypeEnum.ADMIN]).district, name='admin-district'),
    path('admin-department', AdminManagement([UserTypeEnum.ADMIN]).department, name='admin-department'),
    path('admin-treasury', AdminManagement([UserTypeEnum.ADMIN]).treasury, name='admin-treasury'),
    path('admin-grievance-category', AdminManagement([UserTypeEnum.ADMIN]).grievanceCategory, name='admin-grievance-category'),
    path('admin-grievance', AdminManagement([UserTypeEnum.ADMIN]).grievance, name='admin-grievance'),
    path('admin-press-release', AdminManagement([UserTypeEnum.ADMIN]).pressRelease,
         name='admin-press-release'),
    path('admin-news-event', AdminManagement([UserTypeEnum.ADMIN]).newsEvent, name='admin-news-event'),
    path('admin-photo-gallery', AdminManagement([UserTypeEnum.ADMIN]).photoGallery, name='admin-photo-gallery'),
    path('admin-video-gallery', AdminManagement([UserTypeEnum.ADMIN]).videoGallery, name='admin-video-gallery'),
    path('slider-image', AdminManagement([UserTypeEnum.ADMIN]).sliderImage, name='slider-image'),
    path('admin-download', AdminManagement([UserTypeEnum.ADMIN]).download, name='admin-download'),
    path('admin-contact', AdminManagement([UserTypeEnum.ADMIN]).contactDetail, name='admin-contact'),


    path('login', Login, name='login'),
    path('logout', Logout, name='logout'),
    path('user-management', AdminManagement([UserTypeEnum.ADMIN]).userManagement, name='user-management'),
    path('user-profile', userProfile, name='user-profile'),

    re_path('reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', PasswordResetConfirmView.as_view(),
            name='reset_password_confirm'),
    path('reset_password/', ResetPasswordRequestView.as_view(), name="reset_password"),

    re_path(r'^captcha/', include('captcha.urls')),
]

