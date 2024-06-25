# Copyright 2022-2023, IT Cell, Directorate of Treasuries & Accounts, Nagaland. All rights reserved.

from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
]
