# from django.http  import HttpResponse
from typing import Any
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
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
            property_form.save()
            # Property.objects.create(
            #     name=new_property.name,
            #     property_type=new_property.property_type,
            #     purchase_price=new_property.purchase_price,
            #     deposit=new_property.deposit,
            #     City=new_property.City,
            #     other_cost=new_property.other_cost,
            #     bond_value=new_property.bond_value,
            #     notes=new_property.notes
            # )

        return redirect('addimages' )

    context = {
        'property_form': property_form
    }
    return render(request, 'users/addproperty.html', context=context)
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = EditpropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('propertyitem',id=pk)
        # fix the redirect.
    else:
        form = EditpropertyForm(instance=property)
    return render(request, 'users/editproperty.html', {'form': form})
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
            return redirect('interestrates')

    context = {'property': property}

    return render(request, 'users/addimages.html', context=context)


@login_required(login_url='login')
def view_one_property(request, id):
    property_obj = Property.objects.get(id=id)
    image = Images.objects.filter(property=property_obj)
    property_value_list = property_obj.determine_property_value()
    outstanding_loan_per_year = property_obj.determine_outstanding_loan_per_year()
    equity_per_year = property_obj.determine_equity_per_year()
    gross_rental_income = property_obj.determine_gross_rental_income()
    loan_interest = property_obj.determine_loan_interest()
    loan_principal = property_obj.determine_loan_principal()
    total_loan_payment = property_obj.determine_total_loan_payment_per_year()
    additionalloans = property_obj.Additionalloanpayments
    ownrenovations = property_obj.OwnRenovations
    loanrenovations = property_obj.LoanRenovations
    repairs_maintenance = property_obj.repairs_maintenance
    special_expenses = property_obj.specialexpenses
    property_expenses = property_obj.determine_property_expenses_per_year()
    total_property_expenses = property_obj.determine_total_property_expenses_per_year()
    capital_received = property_obj.Capitalincome
    pre_tax_cash_flow = property_obj.determine_pre_tax_cash_flow_per_year()
    initial_outflows = property_obj.determine_initial_capital_outflow_per_year()
    pre_tax_cash_on_cash = property_obj.determine_pre_tax_cash_on_cash()
    total_taxable_deductions = property_obj.determine_taxable_deductions(years=30)
    depreciationlist = property_obj.calculate_depreciation()
    taxable_amounts = property_obj.calculate_taxable_amount()
    tax_credits = property_obj.determine_tax_credits()
    after_tax_cashflows = property_obj.determine_after_tax_cashflow()
    after_tax_cash_on_cash = property_obj.determine_after_tax_cash_on_cash()
    income_per_month = property_obj.determine_income_per_month()
    
    
    context = {
        'property_obj': property_obj,
        'image': image,
        'property_value_list': property_value_list,
        'outstanding_loan_per_year': outstanding_loan_per_year,
        'equity_per_year': equity_per_year,
        'loan_interest': loan_interest,
        'loan_principal': loan_principal,
        'gross_rental_income': gross_rental_income,
        'total_loan_payment': total_loan_payment,
        'additionalloans': additionalloans,
        'ownrenovations': ownrenovations,
        'loanrenovations': loanrenovations,
        'repairs_maintenance': repairs_maintenance,
        'special_expenses': special_expenses,
        'property_expenses': property_expenses,
        'total_property_expenses': total_property_expenses,
        'capital_received': capital_received,
        'pre_tax_cash_flow': pre_tax_cash_flow,
        'initial_outflows': initial_outflows,
        'pre_tax_cash_on_cash': pre_tax_cash_on_cash,
        'total_taxable_deductions': total_taxable_deductions,
        'depreciationlist': depreciationlist,
        'taxable_amounts': taxable_amounts,
        'tax_credits': tax_credits,
        'after_tax_cashflows': after_tax_cashflows,
        'after_tax_cash_on_cash': after_tax_cash_on_cash,
        'income_per_month': income_per_month
        
        
    }
    return render(request, 'users/propertypage.html', context=context)
#continue Thursday
def interestview(request):
    if request.method == 'POST':
        form = InterestRateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inflationrates')
    else:
        form = InterestRateForm()
    return render(request, 'users/interestrates.html', {'form': form})
def inflationview(request):
    if request.method == 'POST':
        myform = InflationRateForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('depreciation')
    else:
        myform = InflationRateForm()
    return render(request, 'users/inflationrates.html', {'myform': myform})
def depreciationview(request):
    if request.method == 'POST':
        myform = DepreciationForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('capitalgrowth')
    else:
        myform = DepreciationForm()
    return render(request, 'users/depreciation.html', {'myform': myform})
def CapitalGrowthview(request):
    if request.method == 'POST':
        myform = CapitalGrowthRatesForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('monthlyexpense')
    else:
        myform = CapitalGrowthRatesForm()
    return render(request, 'users/capitalgrowth.html', {'myform': myform})
def MonthlyExpenseview(request):
    if request.method == 'POST':
        myform = MonthlyExpenseForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('ownrenovations')
    else:
        myform = MonthlyExpenseForm()
    return render(request, 'users/MonthlyExpense.html', {'myform': myform})
def OwnRenovationsview(request):
    if request.method == 'POST':
        myform = OwnRenovationsForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('loanrenovations')
    else:
        myform = OwnRenovationsForm()
    return render(request, 'users/ownrenovations.html', {'myform': myform})
def LoanRenovationsview(request):
    if request.method == 'POST':
        myform = LoanRenovationsForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('repairs_maintenance')
    else:
        myform = LoanRenovationsForm()
    return render(request, 'users/loanrenovations.html', {'myform': myform})
def repairs_maintenanceview(request):
    if request.method == 'POST':
        myform = repairs_maintenanceForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('specialexpenses')
    else:
        myform = repairs_maintenanceForm()
    return render(request, 'users/repairs_maintenance.html', {'myform': myform})
def specialexpensesview(request):
    if request.method == 'POST':
        myform = specialexpensesForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('taxoptions')
    else:
        myform = specialexpensesForm()
    return render(request, 'users/specialexpenses.html', {'myform': myform})
def taxoptionsview(request):
    if request.method == 'POST':
        myform = taxoptionsForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('managementexpenses')
    else:
        myform = taxoptionsForm()
    return render(request, 'users/taxoptions.html', {'myform': myform})
def managementexpensesview(request):
    if request.method == 'POST':
        myform = managementexpensesForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('Additionalloanpayments')
    else:
        myform = managementexpensesForm()
    return render(request, 'users/managementexpenses.html', {'myform': myform})

def Additionalloanpaymentsview(request):
    if request.method == 'POST':
        myform = AdditionalloanpaymentsForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('Capitalincome')
    else:
        myform = AdditionalloanpaymentsForm()
    return render(request, 'users/Additionalloanpayments.html', {'myform': myform})
def Capitalincomeview(request):
    if request.method == 'POST':
        myform = CapitalincomeForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('RentalIncome')
    else:
        myform = CapitalincomeForm()
    return render(request, 'users/Capitalincome.html', {'myform': myform})
def RentalIncomeview(request):
    if request.method == 'POST':
        myform = RentalIncomeForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('comparison')
    else:
        myform = RentalIncomeForm()
    return render(request, 'users/RentalIncome.html', {'myform': myform})
def comparisonview(request,pk):
    if request.method == 'POST':
        myform = comparisonForm(request.POST)
        if myform.is_valid():
            myform.save()
            return redirect('propertyitem',id=pk)
    else:
        myform = comparisonForm()
    return render(request, 'users/comparison.html', {'myform': myform})

# def interestview(request):
#     property = Property.objects.all()

#     if request.method == 'POST':
#         data = request.POST
    
#             return redirect('home')

#     context = {'property': property}

#     return render(request, 'users/interestrates.html', context=context)