# Copyright 2022-2023, IT Cell, Directorate of Treasuries & Accounts, Nagaland. All rights reserved.
from django.shortcuts import render


# Create your views here.
def home(request):
    context = {"url": "home"}
    template = 'pages/home.html'

    return render(request, template, context)


def about(request):
    context = {"url": "about"}
    template = 'pages/about.html'

    return render(request, template, context)
 