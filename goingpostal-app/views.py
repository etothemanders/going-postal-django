from django.shortcuts import render


def index(request):
    return render(request, 'goingpostal-app/index.html')


def shipments(request):
    return render(request, 'goingpostal-app/shipments.html')
