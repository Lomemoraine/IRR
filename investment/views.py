# from django.http  import HttpResponse
from typing import Any
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *


# Create your views here.
# Homepage
@login_required(login_url='login')
def welcome(request):
    all_property = Property.objects.all()

    context = {
        'all_property': all_property
    }
    return render(request, 'home.html', context=context)


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def log_in(request):
    error = False

    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                error = True
    else:
        form = LogInForm()

    return render(request, 'users/login.html', {'form': form, 'error': error})


# def login_user(request):
#     if request.method == 'POST':
#         form = loginForm(request.POST)
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('administrator')
#         else:
#             messages.info(request, "Username or Password is incorrect")

#     context = {}
#     return render(request, 'users/login.html', context=context)


@login_required(login_url='login')
def log_out(request):
    logout(request)
    return redirect(reverse('login'))


# Add property
@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def view_one_property(request, id):
    property_obj = Property.objects.get(id=id)
    image = Images.objects.filter(property=property_obj)

    context = {
        'property_obj': property_obj,
        'image': image
    }
    return render(request, 'users/propertypage.html', context=context)
