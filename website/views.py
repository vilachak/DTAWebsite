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
