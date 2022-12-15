# from django.http  import HttpResponse
from typing import Any

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *


# Create your views here.
# Homepage
def welcome(request):
    all_property = Property.objects.all()

    context = {
        'all_property': all_property
    }
    return render(request, 'home.html', context=context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('administrator')
        else:
            messages.info(request, "Username or Password is incorrect")

    context = {}
    return render(request, 'users/login.html', context=context)


@login_required
def log_out_user(request):
    logout(request)
    return render(request, 'users/home.html')


# Add property
@login_required()
def add_property(request):
    property_form = PropertyForm()
    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        if property_form.is_valid():
            new_property = property_form.save()
            Property.objects.create(
                name=new_property.name,
                property_type=new_property.property_type,
                purchase_price=new_property.purchase_price,
                deposit=new_property.deposit,
                location=new_property.location,
                other_cost=new_property.other_cost,
                bond_value=new_property.bond_value,
                notes=new_property.notes
            )

            return redirect('addimages')

    context = {
        'property_form': property_form
    }
    return render(request, 'users/addproperty.html', context=context)


@login_required()
def addimages(request):
    property = Property.objects.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        if data['property'] != 'none':
            property = Property.objects.get(id=data['property'])
        print(images, property)

        for image in images:
            images = Images.objects.create(
                property=property,
                image=image
            )
            return redirect('home')

    context = {'property': property}

    return render(request, 'users/addimages.html', context=context)


@login_required()
def view_one_property(request, id):
    property_obj = Property.objects.get(id=id)
    image = Images.objects.filter(property=property_obj)

    context = {
        'property_obj': property_obj,
        'image': image
    }
    return render(request, 'users/propertypage.html', context=context)
