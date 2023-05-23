from django.shortcuts import render


def home(request):

    template = 'home.html'
    context = {}

    return render(request, template, context)


def post(request):

    template = 'post.html'
    context = {}

    return render(request, template, context)


def contact(request):

    template = 'contact.html'
    context = {}

    return render(request, template, context)
