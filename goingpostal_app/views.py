from django.shortcuts import render

from .models import Shipment


def index(request):
    return render(request, 'goingpostal_app/index.html')


def shipments(request):
    if request.method == 'POST':
        data = request.POST
        tracking_number = data.get('tracking-number')
        s = Shipment(tracking_no=tracking_number, user=request.user)
        s.save()

    import pdb; pdb.set_trace()
    shipments = Shipment.objects.filter(user=request.user.id)
    context = {
        'shipments': shipments
    }
    return render(request, 'goingpostal_app/shipments.html', context=context)
