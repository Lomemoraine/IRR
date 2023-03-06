# from django.http  import HttpResponse
from typing import Any, List, Union
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *
from .signals import *


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
            property_item = property_form.instance

            # Create interest rate options and corresponding rate per year
            interest_rate = InterestRates.objects.create(type='Interest & capital', average_interest_rate=0,
                                                         term=0, property=property_item)
            [PeriodRate.objects.create(year=year, rate=0, interest_rate=interest_rate) for year in range(1, 31)]

            # Create inflation rate and corresponding rates per year
            inflation_rate = InflationRates.objects.create(average_interest_rate=0, property=property_item)
            [PeriodRate.objects.create(year=year, rate=0, inflation_rate=inflation_rate) for year in range(1, 31)]

            # Depreciation rate
            Depreciation.objects.create(description='Description', type='Straight', value=0, rate=0, years=0,
                                        property=property_item)

            # Capital growth rate and corresponding rates per year
            capital_growth = CapitalGrowthRates.objects.create(average_capital_growth_rate=0, property=property_item)
            [PeriodRate.objects.create(year=year, rate=0, capital_growth=capital_growth) for year in range(1, 31)]

            # Monthly expense
            MonthlyExpense.objects.create(description='', value=0, property=property_item)

            # Own renovations for 30 years
            [OwnRenovations.objects.create(year=year, amount=0, income_per_year=0, property=property_item) for year in
             range(1, 31)]

            # Loan renovations for 30 years
            [LoanRenovations.objects.create(year=year, amount=0, income_per_year=0, property=property_item) for year in
             range(1, 31)]

            # Repair and maintenance for 30 years
            [RepairsMaintenance.objects.create(year=year, amount=0, property=property_item) for year in range(1, 31)]

            # Special expenses for 30 years
            [SpecialExpenses.objects.create(year=year, amount=0, property=property_item) for year in range(1, 31)]

            # Tax options
            tax_options = TaxOptions.objects.create(taxation_capacity='Personal', method='Marginal', tax_rate=0,
                                                    annual_taxable_income=0, maximum_tax_rate=0, property=property_item)
            [TaxOptionsIncome.objects.create(income=0, rate=0, tax_options=tax_options) for i in range(1, 6)]

            # Management expenses
            ManagementExpenses.objects.create(vacancy_rate=0, management_fee=0, management_fee_per_year=0,
                                              property=property_item)

            # Additional loan payments
            [AdditionalLoanPayments.objects.create(year=year, amount=0) for year in range(1, 31)]

            # Capital Income
            [CapitalIncome.objects.create(year=year, amount=0) for year in range(1, 31)]

            # Rental income and 30 year fields
            rental_income = RentalIncome.objects.create(rental_increase_type='capital', average_rental_income_per_month=0,
                                                        property=property_item)
            [PeriodRate.objects.create(year=year, amount=0, rental_income=rental_income) for year in range(1, 31)]

            # Comparison
            Comparison.objects.create(description='', rate=0, property=property_item)

        return redirect('interestrates', pk=property_item.id)

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
            return redirect('propertyitem', id=pk)
        # fix the redirect.
    else:
        form = EditpropertyForm(instance=property)
    return render(request, 'users/editproperty.html', {'form': form})


# @login_required(login_url='login')
# def interestview(request, pk):
#     interest_rate = get_object_or_404(InterestRates, pk=pk)
#     if request.method == 'POST':
#         form = InterestRateForm(request.POST, instance=interest_rate)
#         period_rate = PeriodRateFormSet(request.POST, instance=interest_rate)
#         if form.is_valid() and period_rate.is_valid():
#             form.save(pk=pk)
#             period_rate.save(pk=pk)
#             return redirect('inflationrates', id=pk)
#     else:
#         form = InterestRateForm(instance=interest_rate)
#         period_rate = PeriodRateFormSet(instance=interest_rate)
#     return render(request, 'users/interestrates.html', {'form': form, 'period_rate': period_rate})

@login_required(login_url='login')
def interestview(request, pk):
    interest_rate = get_object_or_404(InterestRates, pk=pk)
    if request.method == 'POST':
        form = InterestRateForm(request.POST, instance=interest_rate)
        formset = PeriodRateFormSet(request.POST, instance=interest_rate)
        if form.is_valid() and formset.is_valid():
            form.save(pk=pk)
            formset.save(pk=pk)
            return redirect('inflationrates', pk=pk)
    else:
        form = InterestRateForm(instance=interest_rate)
        formset = PeriodRateFormSet(instance=interest_rate)

    context = {
        'form': form,
        'formset': formset,
        'formset_errors': formset.errors,
    }
    return render(request, 'users/interestrates.html', context)


@login_required(login_url='login')
def addimages(request, pk):
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        property = Property.objects.get(id=pk)
        for image in images:
            images = Images.objects.create(
                property=property,
                image=image
            )
            return redirect('propertyitem', id=pk)

    context = {}

    return render(request, 'users/addimages.html', context=context)


@login_required(login_url='login')
def view_one_property(request, id):
    property_obj = Property.objects.get(id=id)
    # Loop to create column headers-> Very bad code
    column_name = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                   28, 29, 30]

    additional_loan_payments = AdditionalLoanPayments.objects.all()
    renovations_own = OwnRenovations.objects.all()
    renovations_loan = LoanRenovations.objects.all()
    repair_maintenance = RepairsMaintenance.objects.all()
    special_expense = SpecialExpenses.objects.all()
    property_value = calc_property_value(property_id=id)
    outstanding_loan = calc_outstanding_loan(property_id=id)
    equity = calc_equity(property_id=id)
    gross_rental_income = calc_gross_rental_income(property_id=id)
    loan_interest = calc_loan_interest(property_id=id)
    loan_principal = calc_loan_principal(property_id=id)
    total_loan_payment = calc_total_loan_payment(property_id=id)
    property_expense_per_year = calc_property_expenses_per_year(property_id=id)
    total_property_expenses_per_year = calc_total_property_expenses_per_year(property_id=id)
    pre_tax_before_cash_flow = calc_pre_tax_cash_flow(property_id=id)
    initial_capital_outflow = calc_initial_capital_outflow(property_id=id)
    taxable_deduction = calc_taxable_deductions(property_id=id)
    tax_cash_on_cash = calc_pre_tax_cash_on_cash(property_id=id)
    depreciation = calc_depreciation(property_id=id)
    taxable_amount = calc_taxable_amount(property_id=id)
    tax_credit = calc_tax_credits(property_id=id)
    after_tax_cashflow = calc_after_tax_cashflow(property_id=id)
    after_tax_cash_on_cash = calc_after_tax_cash_on_cash(property_id=id)
    income_per_month = calc_income_per_month(property_id=id)
    irr = calc_irr(property_id=id)

    context = {
        'property_obj': property_obj, 'column_name': column_name,
        'additional_loan_payments': additional_loan_payments,
        'renovations_own': renovations_own, 'renovations_loan': renovations_loan,
        'repair_maintenance': repair_maintenance, 'special_expense': special_expense,
        'property_value': property_value, 'outstanding_loan': outstanding_loan,
        'equity': equity, 'gross_rental_income': gross_rental_income, 'loan_interest': loan_interest,
        'loan_principal': loan_principal, 'total_loan_payment': total_loan_payment,
        'property_expense_per_year': property_expense_per_year,
        'total_property_expenses_per_year': total_property_expenses_per_year,
        'pre_tax_before_cash_flow': pre_tax_before_cash_flow,
        'initial_capital_outflow': initial_capital_outflow,
        'taxable_deduction': taxable_deduction, 'tax_cash_on_cash': tax_cash_on_cash,
        'depreciation': depreciation, 'taxable_amount': taxable_amount, 'tax_credit': tax_credit,
        'after_tax_cashflow': after_tax_cashflow, 'after_tax_cash_on_cash': after_tax_cash_on_cash,
        'income_per_month': income_per_month, 'irr': irr
    }
    return render(request, 'users/propertypage.html', context=context)


# Calculations for properties


def calc_property_value(property_id, years=30):
    try:
        cgr = CapitalGrowthRates.objects.get(property=property_id).average_capital_growth_rate
        prop = Property.objects.get(id=property_id)
        property_value_list = []
        for year in range(1, years + 1):
            property_value = prop.purchase_price * ((float(1) + cgr / 100)) ** year
            property_value_list.append(round(property_value, 2))
        return property_value_list
    except:
        None


def calc_outstanding_loan(property_id):
    try:
        rate = InterestRates.objects.get(property=property_id).average_interest_rate
        interest_rate = rate/100
        total_loan = calc_total_loan_payment(property_id=property_id)
        term = InterestRates.objects.get(property_id=property_id).term
        outstanding_loan_per_year: List[Union[int, Any]] = []
        for total_loan, t in zip(total_loan, range(1, term+1)):
            outstanding_loan = (total_loan / 12 * (1 - (1 + interest_rate / 12) ** (-(term - t) * 12))) / (interest_rate / 12)
            outstanding_loan_per_year.append(round(outstanding_loan, 2))
        return outstanding_loan_per_year
    except:
        None


def calc_equity(property_id):
    try:
        prop_value_year = calc_property_value(property_id=property_id)
        outstanding_loan = calc_outstanding_loan(property_id=property_id)
        equity_per_year = []
        if prop_value_year and outstanding_loan:
            for prop_value, out_loan in zip(prop_value_year, outstanding_loan):
                equity = prop_value - out_loan
                equity_per_year.append(round(equity, 2))
            return equity_per_year
    except:
        None


def calc_gross_rental_income(property_id, years=30):
    try:
        rental_income = RentalIncome.objects.get(property=property_id).amount * 30
        mgmnt_expenses = ManagementExpenses.objects.get(property=property_id).management_fee * 30
        list_income = []
        for year in range(1, years + 1):
            income = rental_income - mgmnt_expenses
            list_income.append(round(income))
        return list_income
    except:
        None


def calc_loan_interest(property_id):
    # loan amount - principal
    try:
        loan_principal = calc_loan_principal(property_id=property_id)
        loan_amount = calc_total_loan_payment(property_id=property_id)
        loan_interest_amt = []
        for principal, loan in zip(loan_principal, loan_amount):
            interest = loan - principal
            loan_interest_amt.append(round(interest, 2))
        return loan_interest_amt
    except:
        None


def calc_loan_principal(property_id):
    # Year1 -> Bond value - loan amount
    # Others -> loan amount[0] - loan amount [1]
    try:
        bond_value = Property.objects.get(id=property_id).bond_value
        term = InterestRates.objects.get(property_id=property_id).term
        outstanding_loan = calc_outstanding_loan(property_id=property_id)
        outstanding_loan.insert(0, bond_value)
        loan_principal = []
        for year in range(1, term+1):
            principal = outstanding_loan[year - 1] - outstanding_loan[year]
            loan_principal.append(round(principal, 2))
        return loan_principal
    except:
        None


def calc_total_loan_payment(property_id, interest_change=None, new_interest_rate=None):
    try:
        bond_price = Property.objects.get(id=property_id).bond_value
        avg_interest_rate_id = InterestRates.objects.get(property_id=property_id).id
        term = InterestRates.objects.get(property_id=property_id).term
        interest_rate = InterestRates.objects.get(property_id=property_id).average_interest_rate
        # interest_rates = [rate.rate / 100 for rate in PeriodRate.objects.filter(interest_rate_id=avg_interest_rate_id)]
        total_loan_payment = []
        for i in range(term):
            if i > term:
                total_loan_payment.append(0)
            else:
                if interest_change is None or new_interest_rate is None:
                    x = (interest_rate / 100)/12
                    y = term*12
                    z = 1+x
                    a = x*(z)**y
                    b = z**y - 1
                    c = a / b
                    d = bond_price * c
                    payment = d * 12
                    # payment = (bond_price * x*z**y / z**y-1)
                    for i in range(term):
                        total_loan_payment.append(round(payment, 2))
                    # print(total_loan_payment)
                    # bond_price -= payment
                else:
                    if interest_change > term:
                        raise ValueError("Interest change year cannot be greater than loan term.")
                    if i == interest_change - 1:
                        interest_rate = new_interest_rate / 100
                        payment = bond_price * (interest_rate / 12 * ((1 + interest_rate / 12) ** (term - i * 12)) / (
                            ((1 + interest_rate / 12) ** (term - i * 12)) - 1)) * 12
                        total_loan_payment.append(round(payment, 2))
                        bond_price -= payment
        return total_loan_payment
    except:
        None


def calc_property_expenses_per_year(property_id, years=30):
    try:
        monthly_expense = MonthlyExpense.objects.get(property_id=property_id).value
        property_expenses_per_year = []
        for year in range(1, years + 1):
            expenses = monthly_expense * 12
            property_expenses_per_year.append(round(expenses, 2))
        return property_expenses_per_year
    except:
        None


def calc_total_property_expenses_per_year(property_id, years=30):
    try:
        property_expenses_per_year = calc_property_expenses_per_year(property_id=property_id, years=years)
        special_expenses = list(SpecialExpenses.objects.filter(property_id=property_id))
        own_renovations = list(OwnRenovations.objects.filter(property_id=property_id))
        loan_renovations = list(LoanRenovations.objects.filter(property_id=property_id))
        repairs_maintenance = list(RepairsMaintenance.objects.filter(property_id=property_id))
        max_len = max(len(special_expenses), len(own_renovations), len(loan_renovations), len(repairs_maintenance))
        if max_len < years:
            years = max_len
        total_property_expenses_per_year = []
        for year in range(1, years + 1):
            expenses = 0
            expenses += special_expenses[year - 1].amount if year <= len(special_expenses) else 0
            expenses += property_expenses_per_year[year - 1]
            expenses += loan_renovations[year - 1].amount if year <= len(loan_renovations) else 0
            expenses += own_renovations[year - 1].amount if year <= len(own_renovations) else 0
            expenses += repairs_maintenance[year - 1].amount if year <= len(repairs_maintenance) else 0
            total_property_expenses_per_year.append(round(expenses, 2))
        return total_property_expenses_per_year
    except:
        None


def calc_pre_tax_cash_flow(property_id, years=30):
    try:
        gross_rental_income = RentalIncome.objects.get(property_id=property_id).amount * 12
        total_expenses = calc_total_property_expenses_per_year(property_id=property_id, years=years)
        pre_tax_cash_flow_per_year = []
        for year in range(1, years + 1):
            cash_flow = 0
            cash_flow += gross_rental_income
            cash_flow += total_expenses[year - 1] if year <= len(total_expenses) else 0
            pre_tax_cash_flow_per_year.append(round(cash_flow, 2))
        return pre_tax_cash_flow_per_year
    except:
        None


def calc_initial_capital_outflow(property_id, years=30):
    try:
        deposit = Property.objects.get(id=property_id).deposit
        other_costs = Property.objects.get(id=property_id).other_cost.amount
        initial_capital_outflow_per_year = []
        for year in range(1, years + 1):
            outflow = deposit + other_costs
            initial_capital_outflow_per_year.append(round(outflow, 2))
        return initial_capital_outflow_per_year
    except:
        None


def calc_pre_tax_cash_on_cash(property_id, years=30):
    try:
        pre_tax_cash_flow_per_year = calc_pre_tax_cash_flow(property_id=property_id)
        initial_capital_outflow_per_year = calc_initial_capital_outflow(property_id=property_id)
        pre_tax_cashoncash = []
        for year in range(1, years + 1):
            cash_on_cash = (pre_tax_cash_flow_per_year[year - 1] / initial_capital_outflow_per_year[year - 1]) * 100
            pre_tax_cashoncash.append(round(cash_on_cash, 2))
        return pre_tax_cashoncash
    except:
        None


def calc_taxable_deductions(property_id, years=30):
    try:
        loan_interest = calc_loan_interest(property_id=property_id)
        total_property_expenses = calc_total_property_expenses_per_year(property_id=property_id)
        taxable_deductions = []
        if loan_interest:
            for year in range(1, years + 1):
                deductions = 0
                deductions += loan_interest[year - 1] if year <= len(loan_interest) else 0
                deductions += total_property_expenses[year - 1] if year <= len(total_property_expenses) else 0
                taxable_deductions.append(round(deductions, 2))
        return taxable_deductions
    except:
        None


def calc_depreciation(property_id):
    try:
        rate = Depreciation.objects.get(property_id=property_id).rate
        years = Depreciation.objects.get(property_id=property_id).years
        purchase_date = Property.objects.get(id=property_id).purchase_date
        purchase_price = Property.objects.get(id=property_id).purchase_price
        depreciation_type = Depreciation.objects.get(property_id=property_id).type

        if depreciation_type == 'straight':
            annual_depreciation = purchase_price * (rate/100)
            total_depreciation = annual_depreciation * years
            remaining_value = purchase_price - total_depreciation

            depreciation_schedule = []
            for year in range(1, years + 1):
                depreciation = (purchase_price-remaining_value)/years
                depreciation_schedule.append(depreciation)
            return depreciation_schedule
        else:
            depreciation_schedule = []
            book_value = purchase_price
            for year in range(1, years + 1):
                depreciation = (book_value * rate) / 100
                book_value = book_value-depreciation
                depreciation_schedule.append(depreciation)
            return depreciation_schedule
    except:
        None


def calc_taxable_amount(property_id, years=30):
    try:
        gross_rental_income = calc_gross_rental_income(property_id)
        taxable_deductions = calc_taxable_deductions(property_id)
        taxable_amount = []
        for year in range(1, years + 1):
            amount = gross_rental_income[year - 1] - taxable_deductions[year - 1]
            taxable_amount.append(round(amount, 2))
        return taxable_amount
    except:
        None


def calc_tax_credits(property_id, years=30):
    try:
        taxable_deductions = calc_taxable_deductions(property_id=property_id)
        tax_credits = []
        for year in range(1, years + 1):
            credit = taxable_deductions[year - 1] * 0.3
            tax_credits.append(round(credit, 2))
        return tax_credits
    except:
        None


def calc_after_tax_cashflow(property_id, years=30):
    try:
        pre_tax_cashflow = calc_pre_tax_cash_flow(property_id=property_id)
        tax_credits = calc_tax_credits(property_id=property_id)
        after_tax_cashflow = []
        for year in range(1, years + 1):
            cashflow = pre_tax_cashflow[year - 1] - tax_credits[year - 1]
            after_tax_cashflow.append(round(cashflow, 2))
        return after_tax_cashflow
    except:
        None


def calc_income_per_month(property_id, years=30):
    try:
        after_tax_cashflow = calc_after_tax_cashflow(property_id=property_id)
        income_per_month = []
        for year in range(1, years + 1):
            income = after_tax_cashflow[year - 1] / 12
            income_per_month.append(round(income, 2))
        return income_per_month
    except:
        None


def calc_after_tax_cash_on_cash(property_id, years=30):
    try:
        after_tax_cashflow = calc_after_tax_cashflow(property_id=property_id)
        initial_cash_outflow = calc_initial_capital_outflow(property_id=property_id)
        after_tax_cash_on_cash = []
        for year in range(1, years + 1):
            cash_on_cash = (after_tax_cashflow[year - 1] / initial_cash_outflow[year - 1]) * 100
            after_tax_cash_on_cash.append(round(cash_on_cash, 2))
        return after_tax_cash_on_cash
    except:
        None


import pandas as pd
import numpy_financial as np


def calc_irr(property_id, years=30):
    try:
        after_tax_cashflow = calc_pre_tax_cash_flow(property_id=property_id)
        initial_investment = Property.objects.get(id=property_id).purchase_price
        if after_tax_cashflow:
            after_tax_cashflow.insert(0, -initial_investment)
        irr_list = []
        for year in range(years):
            sliced_cashflow = after_tax_cashflow[:year+1]
            irr = round(np.irr(sliced_cashflow)*100, 2)
            irr_list.append(irr)
        return irr_list
    except:
        None


def inflationview(request, pk):
    exist_check = Property.objects.get(id=pk)
    messages.error(request, 'Inflation rate already exists') if exist_check else messages.success(request, 'Successful')
    if request.method == 'POST':
        myform = InflationRateForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = InflationRateForm()
    return render(request, 'users/inflationrates.html', {'myform': myform})


def depreciationview(request, pk):
    if request.method == 'POST':
        myform = DepreciationForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = DepreciationForm()
    return render(request, 'users/depreciation.html', {'myform': myform})


def CapitalGrowthview(request, pk):
    exist_check = Property.objects.get(id=pk)
    messages.error(request, 'Average Capital Growth Rate already exists') if exist_check else messages.success(request,
                                                                                                               'Successful')
    if request.method == 'POST':
        myform = CapitalGrowthRatesForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = CapitalGrowthRatesForm()
    return render(request, 'users/capitalgrowth.html', {'myform': myform})


def MonthlyExpenseview(request, pk):
    if request.method == 'POST':
        myform = MonthlyExpenseForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = MonthlyExpenseForm()
    return render(request, 'users/MonthlyExpense.html', {'myform': myform})


def OwnRenovationsview(request, pk):
    if request.method == 'POST':
        myform = OwnRenovationsForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = OwnRenovationsForm()
    return render(request, 'users/ownrenovations.html', {'myform': myform})


def LoanRenovationsview(request, pk):
    if request.method == 'POST':
        myform = LoanRenovationsForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = LoanRenovationsForm()
    return render(request, 'users/loanrenovations.html', {'myform': myform})


def repairs_maintenanceview(request, pk):
    if request.method == 'POST':
        myform = repairs_maintenanceForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = repairs_maintenanceForm()
    return render(request, 'users/repairs_maintenance.html', {'myform': myform})


def specialexpensesview(request, pk):
    if request.method == 'POST':
        myform = specialexpensesForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = specialexpensesForm()
    return render(request, 'users/specialexpenses.html', {'myform': myform})


def taxoptionsview(request, pk):
    if request.method == 'POST':
        myform = taxoptionsForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = taxoptionsForm()
    return render(request, 'users/taxoptions.html', {'myform': myform})


def managementexpensesview(request, pk):
    if request.method == 'POST':
        myform = managementexpensesForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = managementexpensesForm()
    return render(request, 'users/managementexpenses.html', {'myform': myform})


def Additionalloanpaymentsview(request, pk):
    if request.method == 'POST':
        myform = AdditionalloanpaymentsForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = AdditionalloanpaymentsForm()
    return render(request, 'users/Additionalloanpayments.html', {'myform': myform})


def Capitalincomeview(request, pk):
    if request.method == 'POST':
        myform = CapitalincomeForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = CapitalincomeForm()
    return render(request, 'users/Capitalincome.html', {'myform': myform})


def RentalIncomeview(request, pk):
    exist_check = Property.objects.get(id=pk)
    messages.error(request, 'Inflation rate already exists') if exist_check else messages.success(request, 'Successful')
    if request.method == 'POST':
        myform = RentalIncomeForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = RentalIncomeForm()
    return render(request, 'users/RentalIncome.html', {'myform': myform})


def comparisonview(request, pk):
    if request.method == 'POST':
        myform = comparisonForm(request.POST)
        if myform.is_valid():
            myform.save(pk=pk)
            return redirect('propertyitem', id=pk)
    else:
        myform = comparisonForm()
    return render(request, 'users/comparison.html', {'myform': myform})
