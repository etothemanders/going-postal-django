from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import Shipment, Location


def index(request):
    return render(request, 'goingpostal_app/index.html')


def shipments(request):
    shipments = Shipment.objects.filter(user=request.user.id)
    undelivered_shipments = filter(lambda s: s.last_activity.status_description.upper() != 'DELIVERED', shipments)
    if undelivered_shipments:
        map(lambda u: u.check_for_new_activity(), undelivered_shipments)
        shipments = Shipment.objects.filter(user=request.user.id)
    context = {
        'shipments': shipments,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'goingpostal_app/shipments.html', context=context)


def add_shipment(request):
    if request.method == 'POST':
        data = request.POST
        tracking_number = data.get('tracking-number').upper()
        if not Shipment.objects.filter(tracking_no=tracking_number, user=request.user):
            s = Shipment(tracking_no=tracking_number, user=request.user)
            s.save()
            activities = s.track_activities()
            map(lambda activity_dict: Location.create(activity_dict=activity_dict, shipment=s).geocode().save(), activities)
    return redirect('shipments')


def delete_shipment(request):
    if request.method == 'POST':
        data = request.POST.get('tracking-number-delete')
        s = Shipment.objects.filter(user=request.user.id).filter(tracking_no=data)
        s.delete()

    return redirect('shipments')


def load_geojson(request):
    if request.user:
        shipments = Shipment.objects.filter(user=request.user.id)
        if shipments:
            geo_json = {
                "type": "FeatureCollection",
                "features": map(lambda s: s.create_geojson_feature(), shipments)
            }
            return JsonResponse(geo_json)


@login_required
def user_settings(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('auth_password_reset_complete')
    else:
        form = SetPasswordForm(request.user)

    context = {
        'change_password_form': form
    }
    return render(request, 'goingpostal_app/settings.html', context=context)


@login_required
def delete_user(request):
    if request.method == 'POST':
        user = User.objects.filter(id=request.user.id)
        user.delete()
    return redirect('index')
