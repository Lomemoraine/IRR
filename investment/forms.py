from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.forms import fields, widgets


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class LogInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['prof_pic', 'f_name', 'l_name', 'phone', 'bio']


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'property_type', 'purchase_price', 'deposit', 'city',
                  'bond_value', 'notes']
        widgets = {
            'name': widgets.Input(attrs={
                'class': 'form-control',
                'placeholder': 'Five bedroom townhouse',
                'id': 'name'
            }),
            'property_type': widgets.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select type',
                'id': 'property_type'
            }),
            'purchase_price': widgets.Input(attrs={
                'class': 'form-control',
                'placeholder': '4000000',
                'id': 'purchase_price'
            }),
            'deposit': widgets.Input(attrs={
                'class': 'form-control',
                'placeholder': '300000',
                'id': 'deposit'
            }),
            'City': widgets.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select Location',
                'id': 'City'
            }),
            'bond_value': widgets.Input(attrs={
                'class': 'form-control',
                'placeholder': '-----',
                'id': 'bond_value'
            }),
            'notes': widgets.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any Other Information',
                'id': 'notes'
            }),
        }


class InterestRateForm(forms.ModelForm):
    class Meta:
        model = InterestRates
        fields = ['type', 'average_interest_rate']


class EditpropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'property_type', 'purchase_price', 'deposit', 'city',
                  'bond_value', 'notes']


#

class InflationRateForm(forms.ModelForm):
    class Meta:
        model = InflationRates
        fields = ['average_interest_rate']


class DepreciationForm(forms.ModelForm):
    class Meta:
        model = Depreciation
        fields = ['description', 'type', 'value', 'rate', 'years']


class CapitalGrowthRatesForm(forms.ModelForm):
    class Meta:
        model = CapitalGrowthRates
        fields = ['average_capital_growth_rate']


class MonthlyExpenseForm(forms.ModelForm):
    # should give a user freedom to add rows as they wish using javascript or django formset
    class Meta:
        model = MonthlyExpense
        fields = ['description', 'value']


class OwnRenovationsForm(forms.ModelForm):
    class Meta:
        model = OwnRenovations
        fields = ['year', 'amount', 'income_per_year']


class LoanRenovationsForm(forms.ModelForm):
    class Meta:
        model = LoanRenovations
        fields = ['year', 'amount', 'income_per_year']


class repairs_maintenanceForm(forms.ModelForm):
    class Meta:
        model = RepairsMaintenance
        fields = ['year', 'amount']


class specialexpensesForm(forms.ModelForm):
    class Meta:
        model = SpecialExpenses
        fields = ['year', 'amount']


class taxoptionsForm(forms.ModelForm):
    class Meta:
        model = TaxOptions
        fields = ['taxation_capacity', 'method', 'tax_rate',
                  'annual_taxable_income', 'maximum_tax_rate', 'income', 'rate']


class managementexpensesForm(forms.ModelForm):
    class Meta:
        model = ManagementExpenses
        fields = ['vacancy_rate', 'management_fee', 'management_fee_per_year']


class AdditionalloanpaymentsForm(forms.ModelForm):
    class Meta:
        model = AdditionalLoanPayments
        fields = ['amount']


class CapitalincomeForm(forms.ModelForm):
    class Meta:
        model = CapitalIncome
        fields = ['year', 'amount']


class RentalIncomeForm(forms.ModelForm):
    class Meta:
        model = RentalIncome
        fields = ['rental_increase_type', 'increase_percentage', 'average_rental_income_per_month']


class comparisonForm(forms.ModelForm):
    class Meta:
        model = Comparison
        fields = ['description', 'rate']
