# Copyright 2022-2023, IT Cell, Directorate of Treasuries & Accounts, Nagaland. All rights reserved.
from django.urls import path, include

urlpatterns = [
    path('', include('website.urls')),
    path('', include('administrator.urls'))
]
