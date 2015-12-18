from django.shortcuts import render, redirect

from .models import Shipment


def index(request):
    return render(request, 'goingpostal_app/index.html')


def shipments(request):
    shipments = Shipment.objects.filter(user=request.user.id)
    context = {
        'shipments': shipments
    }
    return render(request, 'goingpostal_app/shipments.html', context=context)


def add_shipment(request):
    if request.method == 'POST':
        data = request.POST
        tracking_number = data.get('tracking-number')
        s = Shipment(tracking_no=tracking_number, user=request.user)
        s.save()

    return redirect('shipments')


def delete_shipment(request):
    if request.method == 'POST':
        data = request.POST.get('tracking-number-delete')
        s = Shipment.objects.filter(user=request.user.id).filter(tracking_no=data)
        s.delete()

    return redirect('shipments')
