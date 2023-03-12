from typing import Any, List, Union
import numpy_financial as np
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
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
            [Depreciation.objects.create(description='Description', type='Straight', value=0, rate=0, years=0,
                                         property=property_item) for x in range(1, 5)]

            # Capital growth rate and corresponding rates per year
            capital_growth = CapitalGrowthRates.objects.create(average_capital_growth_rate=0, property=property_item)
            [PeriodRate.objects.create(year=year, rate=0, capital_growth=capital_growth) for year in range(1, 31)]

            # Monthly expense
            [MonthlyExpense.objects.create(description='', value=0, property=property_item) for x in range(1, 3)]

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
            [AdditionalLoanPayments.objects.create(year=year, amount=0, property=property_item)
             for year in range(1, 31)]

            # Capital Income
            [CapitalIncome.objects.create(year=year, amount=0, property=property_item) for year in range(1, 31)]

            # Rental income and 30 year fields
            rental_income = RentalIncome.objects.create(rental_increase_type='capital',
                                                        average_rental_income_per_month=0,
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


@login_required(login_url='login')
def interest_view(request, pk):
    interest_rate = get_object_or_404(InterestRates, pk=pk)
    PeriodRateFormSet = inlineformset_factory(
        InterestRates, PeriodRate, form=PeriodRateForm, extra=0, can_delete=False
    )
    if request.method == 'POST':
        form = InterestRateForm(request.POST, instance=interest_rate)
        formset = PeriodRateFormSet(request.POST, instance=interest_rate)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('inflationrates', pk=pk)
        else:
            print(formset.errors)
    else:
        form = InterestRateForm(instance=interest_rate)
        formset = PeriodRateFormSet(instance=interest_rate)

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'users/interestrates.html', context)


@login_required(login_url='login')
def add_images(request, pk):
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
    # outstanding_loan = calc_outstanding_loan(property_id=id)
    # equity = calc_equity(property_id=id)
    # gross_rental_income = calc_gross_rental_income(property_id=id)
    # loan_interest = calc_loan_interest(property_id=id)
    # loan_principal = calc_loan_principal(property_id=id)
    total_loan_payment = calc_total_loan_payment(property_id=id)
    # property_expense_per_year = calc_property_expenses_per_year(property_id=id)
    # total_property_expenses_per_year = calc_total_property_expenses_per_year(property_id=id)
    # pre_tax_before_cash_flow = calc_pre_tax_cash_flow(property_id=id)
    # initial_capital_outflow = calc_initial_capital_outflow(property_id=id)
    # taxable_deduction = calc_taxable_deductions(property_id=id)
    # tax_cash_on_cash = calc_pre_tax_cash_on_cash(property_id=id)
    # depreciation = calc_depreciation(property_id=id)
    # taxable_amount = calc_taxable_amount(property_id=id)
    # tax_credit = calc_tax_credits(property_id=id)
    # after_tax_cashflow = calc_after_tax_cashflow(property_id=id)
    # after_tax_cash_on_cash = calc_after_tax_cash_on_cash(property_id=id)
    # income_per_month = calc_income_per_month(property_id=id)
    # irr = calc_irr(property_id=id)

    context = {
        'property_obj': property_obj, 'column_name': column_name,
        'additional_loan_payments': additional_loan_payments,
        'renovations_own': renovations_own, 'renovations_loan': renovations_loan,
        'repair_maintenance': repair_maintenance, 'special_expense': special_expense,
        'property_value': property_value,
        # 'outstanding_loan': outstanding_loan,
        # 'equity': equity, 'gross_rental_income': gross_rental_income, 'loan_interest': loan_interest,
        # 'loan_principal': loan_principal,
        'total_loan_payment': total_loan_payment,
        # 'property_expense_per_year': property_expense_per_year,
        # 'total_property_expenses_per_year': total_property_expenses_per_year,
        # 'pre_tax_before_cash_flow': pre_tax_before_cash_flow,
        # 'initial_capital_outflow': initial_capital_outflow,
        # 'taxable_deduction': taxable_deduction, 'tax_cash_on_cash': tax_cash_on_cash,
        # 'depreciation': depreciation, 'taxable_amount': taxable_amount, 'tax_credit': tax_credit,
        # 'after_tax_cashflow': after_tax_cashflow, 'after_tax_cash_on_cash': after_tax_cash_on_cash,
        # 'income_per_month': income_per_month, 'irr': irr
    }
    return render(request, 'users/propertypage.html', context=context)


# Calculations for properties

def calc_property_value(property_id, years=30):
    try:
        cgr = CapitalGrowthRates.objects.get(property=property_id).average_capital_growth_rate
        prop = Property.objects.get(id=property_id)
        property_value_list = []
        for year in range(1, years + 1):
            property_value = prop.purchase_price * (float(1) + cgr / 100) ** year
            property_value_list.append(round(property_value, 2))
        return property_value_list
    except(CapitalGrowthRates.DoesNotExist, Property.DoesNotExist) as e:
        print(f"Error: {e}")
        return None


# def calc_outstanding_loan(property_id):
#     try:
#         rate = InterestRates.objects.get(property=property_id).average_interest_rate
#         other_rates = PeriodRate.objects.filter(interest_rate=rate).order_by('year')
#         interest_rate = [rate / 100 for rate in other_rates]
#         total_loan = calc_total_loan_payment(property_id=property_id)
#         term = InterestRates.objects.get(property_id=property_id).term
#         outstanding_loan_per_year: List[Union[int, Any]] = []
#         for total_loan, t in zip(total_loan, range(1, term + 1)):
#             # outstanding_loan = (total_loan / 12 * (1 - (1 + interest_rate[0] / 12) ** (-(term - t) * 12))) / (
#             #         interest_rate[0] / 12)
#             outstanding_loan = 0
#             outstanding_loan_per_year.append(round(outstanding_loan, 2))
#
#         return outstanding_loan_per_year
#     except(InterestRates.DoesNotExist, Property.DoesNotExist) as e:
#         print(f"Error: {e}")
#         return None


# def calc_equity(property_id):
#     try:
#         prop_value_year = calc_property_value(property_id=property_id)
#         outstanding_loan = calc_outstanding_loan(property_id=property_id)
#         equity_per_year = []
#         if prop_value_year and outstanding_loan:
#             for prop_value, out_loan in zip(prop_value_year, outstanding_loan):
#                 equity = prop_value - out_loan
#                 equity_per_year.append(round(equity, 2))
#             return equity_per_year
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None


# def calc_gross_rental_income(property_id, years=30):
#     try:
#         rental_income = RentalIncome.objects.get(property=property_id).amount * 30
#         mgmnt_expenses = ManagementExpenses.objects.get(property=property_id).management_fee * 30
#         list_income = []
#         for year in range(1, years + 1):
#             income = rental_income - mgmnt_expenses
#             list_income.append(round(income))
#         return list_income
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None


# def calc_loan_interest(property_id):
#     # loan amount - principal
#     try:
#         loan_principal = calc_loan_principal(property_id=property_id)
#         loan_amount = calc_total_loan_payment(property_id=property_id)
#         loan_interest_amt = []
#         for principal, loan in zip(loan_principal, loan_amount):
#             interest = loan - principal
#             loan_interest_amt.append(round(interest, 2))
#         return loan_interest_amt
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None


# def calc_loan_principal(property_id):
#     try:
#         bond_value = Property.objects.get(id=property_id).bond_value
#         term = InterestRates.objects.get(property_id=property_id).term
#         outstanding_loan = calc_outstanding_loan(property_id=property_id)
#         outstanding_loan.insert(0, bond_value)
#         loan_principal = []
#         for year in range(1, term + 1):
#             principal = outstanding_loan[year - 1] - outstanding_loan[year]
#             loan_principal.append(round(principal, 2))
#         return loan_principal
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
def calc_total_loan_payment(property_id):
    try:
        avg_interest_rate_id = InterestRates.objects.get(property_id=property_id).id
        term = InterestRates.objects.get(property_id=property_id).term
        bond_price = Property.objects.get(id=property_id).bond_value

        interest_rates = []
        for rate in PeriodRate.objects.filter(interest_rate_id=avg_interest_rate_id):
            if rate.rate != 0:
                interest_rates.append({rate.year: rate.rate})

        total_loan_payment = []
        interest_change = None
        print(interest_rates)

        for i in range(1, len(interest_rates)):
            current_rate = list(interest_rates[i].values())[0]
            previous_rate = list(interest_rates[i - 1].values())[0]
            if current_rate != previous_rate:
                interest_change = True

        if interest_change is True:
            for y in range(1, len(interest_rates)):
                interest_rate = list(interest_rates[0].values())[0]
                current_rate = list(interest_rates[y - 1].values())[0]
                if interest_rate == current_rate:
                    rate = ((interest_rate / 100) / 12)
                    a = (1 + rate) ** (term * 12)
                    b = bond_price * ((rate * a) / (a - 1))
                    c = 1 - ((1 + rate) ** -((term - y) * 12))
                    payment = b * (c / rate)
                    total_loan_payment.append(round(payment, 2))
                else:
                    bond_price = payment
                    interest_rate = current_rate
                    rate = ((interest_rate / 100) / 12)
                    x = (term - y + 1) * 12
                    a = (1 + rate) ** x
                    b = bond_price * ((rate * a) / (a - 1))
                    c = 1 - ((1 + rate) ** -((term - y) * 12))
                    payment = b * (c / rate)
                    total_loan_payment.append(round(payment, 2))
        else:
            x = (list(interest_rates[0].values())[0] / 100) / 12
            y = term * 12
            z = 1 + x
            a = x * z ** y
            b = z ** y - 1
            c = a / b
            d = bond_price * c
            payment = d * 12
            for y in range(term):
                total_loan_payment.append(round(payment, 2))
        print(total_loan_payment)
        return total_loan_payment
    except (TypeError, AttributeError) as e:
        print(f"Error: {e}")
        return None


#
#
# def calc_property_expenses_per_year(property_id, years=30):
#     try:
#         monthly_expense = MonthlyExpense.objects.filter(property_id=property_id).value
#         property_expenses_per_year = []
#         for year in range(1, years + 1):
#             expenses = monthly_expense * 12
#             property_expenses_per_year.append(round(expenses, 2))
#         return property_expenses_per_year
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
# def calc_total_property_expenses_per_year(property_id, years=30):
#     try:
#         property_expenses_per_year = calc_property_expenses_per_year(property_id=property_id, years=years)
#         special_expenses = list(SpecialExpenses.objects.filter(property_id=property_id))
#         own_renovations = list(OwnRenovations.objects.filter(property_id=property_id))
#         loan_renovations = list(LoanRenovations.objects.filter(property_id=property_id))
#         repairs_maintenance = list(RepairsMaintenance.objects.filter(property_id=property_id))
#         max_len = max(len(special_expenses), len(own_renovations), len(loan_renovations), len(repairs_maintenance))
#         if max_len < years:
#             years = max_len
#         total_property_expenses_per_year = []
#         for year in range(1, years + 1):
#             expenses = 0
#             expenses += special_expenses[year - 1].amount if year <= len(special_expenses) else 0
#             expenses += property_expenses_per_year[year - 1]
#             expenses += loan_renovations[year - 1].amount if year <= len(loan_renovations) else 0
#             expenses += own_renovations[year - 1].amount if year <= len(own_renovations) else 0
#             expenses += repairs_maintenance[year - 1].amount if year <= len(repairs_maintenance) else 0
#             total_property_expenses_per_year.append(round(expenses, 2))
#         return total_property_expenses_per_year
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
# def calc_pre_tax_cash_flow(property_id, years=30):
#     try:
#         gross_rental_income = RentalIncome.objects.get(property_id=property_id).amount * 12
#         total_expenses = calc_total_property_expenses_per_year(property_id=property_id, years=years)
#         pre_tax_cash_flow_per_year = []
#         for year in range(1, years + 1):
#             cash_flow = 0
#             cash_flow += gross_rental_income
#             cash_flow += total_expenses[year - 1] if year <= len(total_expenses) else 0
#             pre_tax_cash_flow_per_year.append(round(cash_flow, 2))
#         return pre_tax_cash_flow_per_year
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
# def calc_initial_capital_outflow(property_id, years=30):
#     try:
#         deposit = Property.objects.get(id=property_id).deposit
#         other_costs = Property.objects.get(id=property_id).other_cost.amount
#         initial_capital_outflow_per_year = []
#         for year in range(1, years + 1):
#             outflow = deposit + other_costs
#             initial_capital_outflow_per_year.append(round(outflow, 2))
#         return initial_capital_outflow_per_year
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
# def calc_pre_tax_cash_on_cash(property_id, years=30):
#     try:
#         pre_tax_cash_flow_per_year = calc_pre_tax_cash_flow(property_id=property_id)
#         initial_capital_outflow_per_year = calc_initial_capital_outflow(property_id=property_id)
#         pre_tax_cashoncash = []
#         for year in range(1, years + 1):
#             cash_on_cash = (pre_tax_cash_flow_per_year[year - 1] / initial_capital_outflow_per_year[year - 1]) * 100
#             pre_tax_cashoncash.append(round(cash_on_cash, 2))
#         return pre_tax_cashoncash
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
# def calc_taxable_deductions(property_id, years=30):
#     try:
#         loan_interest = calc_loan_interest(property_id=property_id)
#         total_property_expenses = calc_total_property_expenses_per_year(property_id=property_id)
#         taxable_deductions = []
#         if loan_interest:
#             for year in range(1, years + 1):
#                 deductions = 0
#                 deductions += loan_interest[year - 1] if year <= len(loan_interest) else 0
#                 deductions += total_property_expenses[year - 1] if year <= len(total_property_expenses) else 0
#                 taxable_deductions.append(round(deductions, 2))
#         return taxable_deductions
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
# def calc_depreciation(property_id):
#     try:
#         rate = Depreciation.objects.filter(property_id=property_id).rate
#         years = Depreciation.objects.filter(property_id=property_id).years
#         purchase_date = Property.objects.filter(id=property_id).purchase_date
#         purchase_price = Property.objects.filter(id=property_id).purchase_price
#         depreciation_type = Depreciation.objects.filter(property_id=property_id).type
#
#         if depreciation_type == 'straight':
#             annual_depreciation = purchase_price * (rate / 100)
#             total_depreciation = annual_depreciation * years
#             remaining_value = purchase_price - total_depreciation
#
#             depreciation_schedule = []
#             for year in range(1, years + 1):
#                 depreciation = (purchase_price - remaining_value) / years
#                 depreciation_schedule.append(depreciation)
#             return depreciation_schedule
#         else:
#             depreciation_schedule = []
#             book_value = purchase_price
#             for year in range(1, years + 1):
#                 depreciation = (book_value * rate) / 100
#                 book_value = book_value - depreciation
#                 depreciation_schedule.append(depreciation)
#             return depreciation_schedule
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
# def calc_taxable_amount(property_id, years=30):
#     try:
#         gross_rental_income = calc_gross_rental_income(property_id)
#         taxable_deductions = calc_taxable_deductions(property_id)
#         taxable_amount = []
#         for year in range(1, years + 1):
#             amount = gross_rental_income[year - 1] - taxable_deductions[year - 1]
#             taxable_amount.append(round(amount, 2))
#         return taxable_amount
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
# def calc_tax_credits(property_id, years=30):
#     try:
#         taxable_deductions = calc_taxable_deductions(property_id=property_id)
#         tax_credits = []
#         for year in range(1, years + 1):
#             credit = taxable_deductions[year - 1] * 0.3
#             tax_credits.append(round(credit, 2))
#         return tax_credits
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
# def calc_after_tax_cashflow(property_id, years=30):
#     try:
#         pre_tax_cashflow = calc_pre_tax_cash_flow(property_id=property_id)
#         tax_credits = calc_tax_credits(property_id=property_id)
#         after_ta
#         x_cashflow = []
#         for year in range(1, years + 1):
#             cashflow = pre_tax_cashflow[year - 1] - tax_credits[year - 1]
#             after_tax_cashflow.append(round(cashflow, 2))
#         return after_tax_cashflow
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
# def calc_income_per_month(property_id, years=30):
#     try:
#         after_tax_cashflow = calc_after_tax_cashflow(property_id=property_id)
#         income_per_month = []
#         for year in range(1, years + 1):
#             income = after_tax_cashflow[year - 1] / 12
#             income_per_month.append(round(income, 2))
#         return income_per_month
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
# def calc_after_tax_cash_on_cash(property_id, years=30):
#     try:
#         after_tax_cashflow = calc_after_tax_cashflow(property_id=property_id)
#         initial_cash_outflow = calc_initial_capital_outflow(property_id=property_id)
#         after_tax_cash_on_cash = []
#         for year in range(1, years + 1):
#             cash_on_cash = (after_tax_cashflow[year - 1] / initial_cash_outflow[year - 1]) * 100
#             after_tax_cash_on_cash.append(round(cash_on_cash, 2))
#         return after_tax_cash_on_cash
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#
#
# def calc_irr(property_id, years=30):
#     try:
#         after_tax_cashflow = calc_pre_tax_cash_flow(property_id=property_id)
#         initial_investment = Property.objects.get(id=property_id).purchase_price
#         if after_tax_cashflow:
#             after_tax_cashflow.insert(0, -initial_investment)
#         irr_list = []
#         for year in range(years):
#             sliced_cashflow = after_tax_cashflow[:year + 1]
#             irr = round(np.irr(sliced_cashflow) * 100, 2)
#             irr_list.append(irr)
#         return irr_list
#     except (TypeError, AttributeError) as e:
#         print(f"Error: {e}")
#         return None
#


def inflation_view(request, pk):
    inflation_rate = get_object_or_404(InflationRates, pk=pk)
    PeriodRateInflationFormSet = inlineformset_factory(
        InflationRates, PeriodRate, form=PeriodRateForm, extra=0, can_delete=False, )
    if request.method == 'POST':
        inflation_form = InflationRateForm(request.POST, instance=inflation_rate)
        inflation_formset = PeriodRateInflationFormSet(request.POST, instance=inflation_rate)
        if inflation_form.is_valid():
            inflation_form.save()
        if inflation_formset.is_valid():
            inflation_formset.save()
            return redirect('depreciation', pk=pk)
        print(inflation_formset.errors, 'formset not saved')
    inflation_form = InflationRateForm(instance=inflation_rate)
    inflation_formset = PeriodRateInflationFormSet(instance=inflation_rate)

    context = {
        'inflation_form': inflation_form,
        'inflation_formset': inflation_formset
    }
    return render(request, 'users/inflationrates.html', context)


def depreciation_view(request, pk):
    property_item = Property.objects.get(pk=pk)
    depreciation_formset = inlineformset_factory(Property, Depreciation, form=DepreciationForm, extra=0,
                                                 can_delete=False)
    if request.method == 'POST':
        formset = depreciation_formset(request.POST, instance=property_item)
        if formset.is_valid():
            formset.save()
            return redirect('capitalgrowth', pk=pk)
        print(formset.errors)
    formset = depreciation_formset(instance=property_item)

    context = {
        'depreciation_formset': formset,
    }
    return render(request, 'users/depreciation.html', context)


def capital_growth_view(request, pk):
    capital_growth = get_object_or_404(CapitalGrowthRates, pk=pk)
    PeriodRateCGR = inlineformset_factory(CapitalGrowthRates, PeriodRate, form=PeriodRateForm, extra=0,
                                          can_delete=False)
    if request.method == 'POST':
        cgr_form = CapitalGrowthRatesForm(request.POST, instance=capital_growth)
        cgr_formset = PeriodRateCGR(request.POST, instance=capital_growth)
        if cgr_form.is_valid():
            cgr_form.save()
        if cgr_formset.is_valid():
            cgr_formset.save()
            return redirect('monthlyexpense', pk=pk)
        print(cgr_formset.errors)
    cgr_form = CapitalGrowthRatesForm(instance=capital_growth)
    cgr_formset = PeriodRateCGR(instance=capital_growth)

    context = {
        'cgr_form': cgr_form,
        'cgr_formset': cgr_formset
    }
    return render(request, 'users/capitalgrowth.html', context)


def monthly_expense_view(request, pk):
    property_item = Property.objects.get(pk=pk)
    expense_formset = inlineformset_factory(Property, MonthlyExpense, form=MonthlyExpenseForm, extra=2,
                                            can_delete=False)
    if request.method == 'POST':
        formset = expense_formset(request.POST, instance=property_item)
        if formset.is_valid():
            formset.save()
            return redirect('ownrenovations', pk=pk)
        print(formset.errors)
    formset = expense_formset(instance=property_item)

    context = {'expense_formset': formset}
    return render(request, 'users/MonthlyExpense.html', context)


def own_renovations_view(request, pk):
    property_item = Property.objects.get(pk=pk)
    own_renovations_formset = inlineformset_factory(Property, OwnRenovations, form=OwnRenovationsForm,
                                                    can_delete=False, extra=1)
    if request.method == 'POST':
        formset = own_renovations_formset(request.POST, instance=property_item)
        if formset.is_valid():
            formset.save()
            return redirect('loanrenovations', pk=pk)
        print(formset.errors)
    formset = own_renovations_formset(instance=property_item)

    context = {'own_renovations_formset': formset}
    return render(request, 'users/ownrenovations.html', context)


def loan_renovations_view(request, pk):
    property_item = Property.objects.get(pk=pk)
    loan_renovations_formset = inlineformset_factory(Property, LoanRenovations, form=LoanRenovationsForm,
                                                     extra=0, can_delete=False)
    if request.method == 'POST':
        formset = loan_renovations_formset(request.POST, instance=property_item)
        if formset.is_valid():
            formset.save()
            return redirect('repairs_maintenance', pk=pk)
        print(formset.errors)
    formset = loan_renovations_formset(instance=property_item)

    context = {'loan_renovations_formset': formset}
    return render(request, 'users/loanrenovations.html', context)


def repairs_maintenance_view(request, pk):
    property_item = Property.objects.get(pk=pk)
    repairs_formset = inlineformset_factory(Property, RepairsMaintenance, form=repairs_maintenanceForm, extra=0,
                                            can_delete=False)
    if request.method == 'POST':
        formset = repairs_formset(request.POST, instance=property_item)
        if formset.is_valid():
            formset.save()
            return redirect('specialexpenses', pk=pk)
        print(formset.errors)
    formset = repairs_formset(instance=property_item)

    context = {'repairs_formset': formset}
    return render(request, 'users/repairs_maintenance.html', context)


def special_expenses_view(request, pk):
    property_item = Property.objects.get(pk=pk)
    special_expenses_formset = inlineformset_factory(Property, SpecialExpenses, form=specialexpensesForm, extra=0,
                                                     can_delete=False)
    if request.method == 'POST':
        formset = special_expenses_formset(request.POST, instance=property_item)
        if formset.is_valid():
            formset.save()
            return redirect('taxoptions', pk=pk)
        print(formset.errors)
    formset = special_expenses_formset(instance=property_item)

    context = {'special_expenses_formset': formset}
    return render(request, 'users/specialexpenses.html', context)


def tax_options_view(request, pk):  # Todo incomplete
    tax_options = get_object_or_404(TaxOptions, pk=pk)
    tax_options_income_formset = inlineformset_factory(TaxOptions, TaxOptionsIncome, form=TaxOptionsIncomeForm,
                                                       extra=2, can_delete=False)
    if request.method == 'POST':
        tax_form = taxoptionsForm(request.POST, instance=tax_options)
        tax_formset = tax_options_income_formset(request.POST, instance=tax_options)
        if tax_formset.is_valid() and tax_form.is_valid():
            tax_form.save()
            tax_formset.save()
            return redirect('propertyitem', id=pk)
        print(tax_formset.errors)
    tax_form = taxoptionsForm(instance=tax_options)
    tax_formset = tax_options_income_formset(instance=tax_options)

    context = {
        'tax_form': tax_form,
        'tax_formset': tax_formset
    }
    return render(request, 'users/taxoptions.html', context)


def management_expenses_view(request, pk):
    property_item = Property.objects.get(pk=pk)
    management_expenses_formset = inlineformset_factory(Property, ManagementExpenses, form=managementexpensesForm,
                                                        extra=0, can_delete=False)
    if request.method == 'POST':
        formset = management_expenses_formset(request.POST, instance=property_item)
        if formset.is_valid():
            formset.save()
            return redirect('Additionalloanpayments', pk=pk)
        print(formset.errors)
    formset = management_expenses_formset(instance=property_item)

    context = {'management_expenses_formset': formset}
    return render(request, 'users/managementexpenses.html', context)


def additional_loan_payments_view(request, pk):  # todo not doen
    property_item = Property.objects.get(pk=pk)
    add_loans_formset = inlineformset_factory(Property, AdditionalLoanPayments, form=AdditionalloanpaymentsForm,
                                              extra=0, can_delete=False)
    if request.method == 'POST':
        formset = add_loans_formset(request.POST, instance=property_item)
        print(formset)
        if formset.is_valid():
            formset.save()
            return redirect('Capitalincome', pk=pk)
        print(formset.errors)
    formset = add_loans_formset(instance=property_item)
    print(formset)

    context = {
        'formset': formset,
        'property': property_item
    }
    return render(request, 'users/Additionalloanpayments.html', context)


def capital_income_view(request, pk):
    property_item = Property.objects.get(pk=pk)
    capital_income_formset = inlineformset_factory(Property, CapitalIncome, form=CapitalincomeForm, extra=0,
                                                   can_delete=False)
    if request.method == 'POST':
        formset = capital_income_formset(request.POST, instance=property_item)
        if formset.is_valid():
            formset.save()
            return redirect('RentalIncome', pk=pk)
        print(formset.errors)
    formset = capital_income_formset(instance=property_item)

    context = {'capital_income_formset': formset}
    return render(request, 'users/Capitalincome.html', context)


def rental_income_view(request, pk):
    rental_income = get_object_or_404(RentalIncome, pk=pk)
    rental_income_formset = inlineformset_factory(RentalIncome, PeriodRate, fields=['year', 'amount'], extra=0,
                                                  can_delete=False)
    if request.method == 'POST':
        rental_form = RentalIncomeForm(request.POST, instance=rental_income)
        rental_formset = rental_income_formset(request.POST, instance=rental_income)
        if rental_form.is_valid() and rental_formset.is_valid():
            rental_form.save()
            rental_formset.save()
            return redirect('comparison', pk=pk)
        print(rental_formset.errors, rental_form.errors)
    rental_form = RentalIncomeForm(instance=rental_income)
    rental_formset = rental_income_formset(instance=rental_income)

    context = {'rental_form': rental_form, 'rental_formset': rental_formset}
    return render(request, 'users/RentalIncome.html', context)


def comparison_view(request, pk):
    property_item = Property.objects.get(pk=pk)
    comparison_formset = inlineformset_factory(Property, Comparison, form=comparisonForm, extra=0, can_delete=False)
    if request.method == 'POST':
        formset = comparison_formset(request.POST, instance=property_item)
        if formset.is_valid():
            formset.save()
            return redirect('propertyitem', id=pk)
        print(formset.errors)
    formset = comparison_formset(instance=property_item)

    return render(request, 'users/comparison.html', {'formset': formset})
