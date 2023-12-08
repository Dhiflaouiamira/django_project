from django.shortcuts import render, redirect
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import *
from .forms import *


def vehicles_view(request):
    vehicles = Vehicle.objects.all() #filter(for_sale=True)
    return render(request, "vehicles.html", {"vehicles": vehicles, "user": request.user})

def vehicle_details(request, id):
    vehicle = Vehicle.objects.get(pk=id)
    print(vehicle.for_sale)
    return render(request, "vehicledetails.html", {"vehicle": vehicle, "user": request.user})

from django.urls import reverse

def addvehicle_view(request):
    message = ""
    form = AddVehicleForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            try:
                model = form.cleaned_data.get("model")
                vehicle = Vehicle(
                    owner=request.user,
                    fuel_type=form.cleaned_data.get("fuel_type"),
                    model=form.cleaned_data.get("model"),
                    for_sale=form.cleaned_data.get("for_sale"),
                    kilometers=form.cleaned_data.get("kilometers"),
                    price=form.cleaned_data.get("price"),
                    brand=form.cleaned_data.get("brand"),
                    photo=form.cleaned_data.get("photo")
                )
                vehicle.save()
                message = "{} saved successfully.".format(vehicle)
                # Redirect to the 'vehicles' page after successfully adding the vehicle
                return redirect('vehicles_path')  # Make sure to use the appropriate URL name
            except Exception as exp:
                message = exp
                print("Error from except")
        else:
            print(form.errors)
    return render(request, "addvehicle.html", {
        "form": form, 
        "user": request.user, 
        "message": message
    })



def delete_vehicle(request, vehicle_id):
    message = ""
    try:
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        vehicle.delete()
        message = "Deleted."
    except Exception as exp:
        print(exp)
        message = exp
    return redirect("vehicles_path")


def predictvehicle_view(request):
    message = ""
    form = PredictedVehicleForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                model = form.cleaned_data.get("model")
                vehicle = Vehicle(
                    fuel_type=form.cleaned_data.get("fuel_type"),
                    model=form.cleaned_data.get("model"),
                    kilometers=form.cleaned_data.get("kilometers"),
                    brand=form.cleaned_data.get("brand"),
                )
                print(vehicle)
                message = "Estimated price: {} TND".format(25000)
            except Exception as exp:
                message = exp
            
    return render(request, "predict.html", {
        "form": form, 
        "user": request.user, 
        "message": message}
    )
from django.shortcuts import render, redirect
from .forms import UpdateVehicleForm
from .models import Vehicle

def  updatevehicle_view(request, id):
    message = ""
    try:
        vehicle = Vehicle.objects.get(pk=id)
        if request.method == 'POST':
            form = UpdateVehicleForm(request.POST, request.FILES, instance=vehicle)
            if form.is_valid():
                form.save()
                message = "Vehicle updated successfully."
                return redirect('vehicle_details', id=id)  # Redirect to vehicle details page after update
        else:
            form = UpdateVehicleForm(instance=vehicle)
    except Vehicle.DoesNotExist:
        message = "Vehicle does not exist."
        form = None

    return render(request, "updatevehicle.html", {
        "form": form,
        "vehicle_id": id,
        "message": message
    })