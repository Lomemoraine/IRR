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


# class CapitalGrowthRatesForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year_rate = f'year_{i}_rate'
#
#             self.fields[year_rate] = forms.FloatField()
#
#
#     class Meta:
#         model = CapitalGrowthRates
#         fields = []
#
# class MonthlyExpenseForm(forms.ModelForm):
#     # should give a user freedom to add rows as they wish using javascript or django formset
#     class Meta:
#         model =   MonthlyExpense
#         fields = ['description','value']
# class OwnRenovationsForm(forms.ModelForm):
#     class Meta:
#         model =   OwnRenovations
#         fields = []
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year_rate = f'year_{i}_incomeperyear'
#             year_amount = f'year_{i}_amount'
#             self.fields[year_rate] = forms.FloatField()
#             self.fields[year_amount] = forms.FloatField()
# class LoanRenovationsForm(forms.ModelForm):
#     class Meta:
#         model =   LoanRenovations
#         fields = []
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year_rate = f'year_{i}_incomeperyear'
#             year_amount = f'year_{i}_amount'
#             self.fields[year_rate] = forms.FloatField()
#             self.fields[year_amount] = forms.FloatField
# class repairs_maintenanceForm(forms.ModelForm):
#     class Meta:
#         model =   repairs_maintenance
#         fields = []
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year = f'year_{i}_amount'
#             self.fields[year] = forms.FloatField()
#
# class specialexpensesForm(forms.ModelForm):
#     class Meta:
#         model = specialexpenses
#         fields = []
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year = f'year_{i}_amount'
#             self.fields[year] = forms.FloatField()
#
# class taxoptionsForm(forms.ModelForm):
#     class Meta:
#         model =  taxoptions
#         fields = ['taxationcapacity','method','taxrate','annualtaxableincome','maximumtaxrate','income','rate']
#
# class managementexpensesForm(forms.ModelForm):
#     class Meta:
#         model =  managementexpenses
#         fields = ['vacancyrate','managementfee','managementfeeperyear']
# class AdditionalloanpaymentsForm(forms.ModelForm):
#     class Meta:
#         model =  Additionalloanpayments
#         fields = ['amount']
# class CapitalincomeForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year = f'year_{i}_amount'
#             setattr(self, year, models.FloatField())
#     class Meta:
#         model =  Capitalincome
#         fields = []
#
#
#
# class RentalIncomeForm(forms.ModelForm):
#
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year = f'year_{i}_amount'
#             self.fields[year] = forms.FloatField()
#     class Meta:
#         model = RentalIncome
#         fields = ['rentalincreasetype','increasepercentage','averagerentalincomepermonth']
#
# class comparisonForm(forms.ModelForm):
#     class Meta:
#         model =  comparison
#         fields = ['description','rate']