# Copyright 2022-2023, IT Cell, Directorate of Treasuries & Accounts, Nagaland. All rights reserved.

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('who', views.who, name='who'),
    path('news-events', views.news, name='news-events'),
    path('photo-gallery', views.photogallery, name='photo-gallery'),
    path('video-gallery', views.videogallery, name='video-gallery'),
    path('apar', views.apar, name='apar'),
    path('rti', views.rti, name='rti'),
    path('gpf', views.gpf, name='gpf'),
    path('pension', views.pension, name='pension'),
    path('contact', views.contact, name='contact'),
    path('grievance', views.grievance, name='grievance'),
    path('site-map', views.site_map, name='site-map'),
    path('screen-reader', views.screen_reader, name='screen-reader'),
]
