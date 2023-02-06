from django.db import models
from datetime import date,timedelta
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField
import numpy_financial as npf
import math


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"  # make the user log in with the email
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    prof_pic = CloudinaryField('images',default='http://res.cloudinary.com/dim8pysls/image/upload/v1639001486'
                                       '/x3mgnqmbi73lten4ewzv.png')
    bio = models.TextField(blank=True, max_length=255, default='please update your bio')
    f_name = models.CharField(blank=True, max_length=255)
    l_name = models.CharField(blank=True, max_length=50)
    phone = PhoneNumberField(blank=True)

    def __str__(self):
        return self.f_name

    def save_profile(self):
        """Add Profile to database"""
        self.save()


class PropertyType(models.Model):
    name = models.CharField(max_length=252, null=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=252, null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=252, null=True)

    def __str__(self):
        return self.name


class OtherCosts(models.Model):
    CHOICES = (
        ('Property Taxes', 'Property Taxes'),
        ('Repairs & Utilities', 'Repairs & Utilities'),
        ('Mortgage Insurance', 'Mortgage Insurance'),
    )
    other_costs = models.CharField(max_length=255, null=True, choices=CHOICES)
    amount = models.IntegerField(null=True)

    def __str__(self):
        return self.other_costs


class Property(models.Model):
    name = models.CharField(max_length=252, null=True)
    property_type = models.ForeignKey(PropertyType, null=True, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True, null=True)
    purchase_price = models.FloatField(null=True)
    deposit = models.FloatField(null=True)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    other_cost = models.ForeignKey(OtherCosts, null=True, on_delete=models.CASCADE)
    bond_value = models.IntegerField(null=True)
    notes = models.TextField(max_length=1260, null=True)

    def __str__(self):
        return self.name

    def save_property(self):
        """Add property to database"""
        self.save()


class Images(models.Model):
    image = CloudinaryField('images',default='http://res.cloudinary.com/dim8pysls/image/upload/v1639001486'
                                    '/x3mgnqmbi73lten4ewzv.png')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)\


class InterestRates(models.Model):
    Choices = (
        ('Interest & capital', 'Interest & capital'),
        ('Interest only', 'Interest only')
    )
    type = models.CharField(max_length=255, null=True, choices=Choices)
    average_interest_rate = models.FloatField(blank=True, default=1)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, default=1)

    def add_year_rate(self, year, rate):
        PeriodRate.objects.create(interest_rate=self, year=year, rate=rate)


class InflationRates(models.Model):
    average_interest_rate = models.FloatField(blank=True, default=1)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)

    def add_year_rate(self, year, rate):
        PeriodRate.objects.create(interest_rate=self, year=year, rate=rate)


class Depreciation(models.Model):
    Choices = (
        ('Straight', 'Straight'),
        ('Diminishing', 'Diminishing')
    )
    description = models.CharField(blank=True, max_length=255)
    type = models.CharField(choices=Choices, max_length=255)
    value = models.FloatField(blank=True, default=1)
    rate = models.FloatField(blank=True, default=1)
    years = models.PositiveSmallIntegerField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)


class PeriodRate(models.Model):
    year = models.PositiveSmallIntegerField()
    rate = models.FloatField()
    interest_rate = models.ForeignKey(InterestRates, on_delete=models.CASCADE)

#
#
# class Depreciation(models.Model):
# #should allow the users to add as many fields as they want can either use js document.createElement() or django formset.
#     type = models.CharField(null=True,max_length=50,default='Interest & capital', choices=(
#         ('Straight', 'Straight'),
#         ('Diminishing', 'Diminishing'),
#
#     ))
#     description = models.CharField(null=True,max_length=255)
#     value = models.FloatField(null=True)
#     rate = models.IntegerField(('Rate (%)'),null=True,default=8)
#     years = models.IntegerField(null=True)
#     # property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):
#         return self.rate
# class CapitalGrowthRates(models.Model):
#
#     # rate = models.IntegerField(null=True,default=8)
#     averagecapitalGrowthrate = models.FloatField(('Average Capital Growth Rate (%)'),null=False,default=8)
#     # property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):
#         return str(self.averagecapitalGrowthrate)
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year_rate = f'year_{i}_rate'
#
#             setattr(self, year_rate, models.FloatField())
#
# class MonthlyExpense(models.Model):
#
#     description = models.CharField(max_length=255, null=True)
#     value = models.IntegerField(null=True)
#     # property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
#
#
#     def __str__(self):
#         return self.description
#
# class OwnRenovations(models.Model):
#
#     # incomeperyear = models.FloatField(('Income per year'), null=True,default=0)
#     # # amount = models.IntegerField(null=True,default=0)
#     # # property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
#
#
#     # def __str__(self):
#     #     return str(self.incomeperyear)
#     # def __init__(self, *args, **kwargs):
#     #     super().__init__(*args, **kwargs)
#     #     for i in range(1, 31):
#     #         year = f'year_{i}_amount'
#     #         setattr(self, year, models.FloatField())
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year_rate = f'year_{i}_incomeperyear'
#             year_amount = f'year_{i}_amount'
#             setattr(self, year_rate, models.FloatField())
#             setattr(self, year_amount, models.FloatField())
#
# class LoanRenovations(models.Model):
#
#     # incomeperyear = models.FloatField(('Income per year'), null=True,default=0)
#     # amount = models.IntegerField(null=True,default=0)
#     # property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
#
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year_rate = f'year_{i}_incomeperyear'
#             year_amount = f'year_{i}_amount'
#             setattr(self, year_rate, models.FloatField())
#             setattr(self, year_amount, models.FloatField())
# class repairs_maintenance(models.Model):
#     # amount = models.IntegerField(null=True,default=0)
#     # # property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
#
#
#     # def __str__(self):
#     #     return self.amount
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year = f'year_{i}_amount'
#             setattr(self, year, models.FloatField())
# class specialexpenses(models.Model):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year = f'year_{i}_amount'
#             setattr(self, year, models.FloatField())
# class taxoptions(models.Model):
#
#     taxationcapacity = models.CharField(null=True,max_length=50,default='Interest & capital', choices=(
#         ('Personal', 'Personal'),
#         ('close corporation', 'close corporation'),
#         ('private company', 'private company'),
#         ('trust', 'trust'),
#
#     ))
#     method = models.CharField(null=True,max_length=50,default='Interest & capital', choices=(
#         ('0%', '0%'),
#         ('Marginal', 'Marginal'),
#         ('Use Tax Table', 'Use Tax Table'),
#         ('Custom', 'Custom'),
#
#     ))
#
#     taxrate = models.FloatField(('Tax Rate(%)'),null=True)
#     annualtaxableincome = models.FloatField(('Annual Taxableincome(%)'),null=False)
#     maximumtaxrate = models.IntegerField(('Maximum Tax Rate (%)'),null=False)
#     income = models.IntegerField(null=True)
#     rate = models.IntegerField(null=True)
#     # property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):
#         return self.rate
# class managementexpenses(models.Model):
#
#     vacancyrate = models.IntegerField(('Vacancy Rate (%)'),null=True,default=0)
#     managementfee = models.IntegerField(('Management Fee (%)'),null=True,default=0)
#     managementfeeperyear = models.IntegerField(('Management Fee per Year '))
#     # property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
#
#
#     def __str__(self):
#         return self.vacancyrate
#
# class Additionalloanpayments(models.Model):
#
#     amount = models.IntegerField(null=True,default=0)
#     # property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
#
#
#
#     def __str__(self):
#         return self.amount
#     def save_additionalloanpaymens(self):
#         """Add loans to database"""
#         self.save()
#
#
# class Capitalincome(models.Model):
#
#     amount = models.IntegerField(null=True,default=0)
#     # property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):
#         return str(self.amount)
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year = f'year_{i}_amount'
#             setattr(self, year, models.FloatField())
#
# class RentalIncome(models.Model):
#
#     rentalincreasetype = models.CharField(('Type'),null=True,max_length=50,default='Interest & capital', choices=(
#         ('capital', 'capital'),
#         ('inflation', 'inflation'),
#         ('percent', 'percent'),
#
#     ))
#     increasepercentage = models.IntegerField(('Increase Percentage (%)'))
#     averagerentalincomepermonth = models.FloatField(('Average Rental Income Per Month'),null=True)
#     # amount = models.IntegerField(('Amount'),null=True)
#     # property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):
#         return self.rentalincreasetype
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for i in range(1, 31):
#             year = f'year_{i}_amount'
#             setattr(self, year, models.FloatField())
#
# class comparison(models.Model):
#     description = models.CharField(max_length=255, null=True)
#     rate = models.IntegerField(('Rate (%)'),null=True,default=0)
#     # property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
#
#
#
#     def __str__(self):
#         return self.description
# class Images(models.Model):
#     image = CloudinaryField('images',default='http://res.cloudinary.com/dim8pysls/image/upload/v1639001486'
#                                     '/x3mgnqmbi73lten4ewzv.png')
#
#
#     #determine the property value
#     def determine_property_value(self, years=30):
#         purchase_price = self.purchase_price
#         capital_growth_rate = getattr(self.CapitalGrowthRates,f'year_{year}_rate',0) / 100 if getattr(self.CapitalGrowthRates,f'year_{year}_rate',0) else 0
#         property_value_list = []
#         for year in range(1, years+1):
#             property_value = purchase_price * (1 + capital_growth_rate/100)**year
#             property_value_list.append(property_value)
#         return property_value_list
#     #property = Property.objects.get(id=1)
#     # property_value = property.determine_property_value(5)
#     # print(property_value)
#     #determine total loan amount
#     def determine_outstanding_loan_per_year(self):
#         if self.InterestRates:
#             interest_rate = getattr(self.InterestRates,f'year_{t}_rate'/100) if getattr(self.InterestRates,f'year_{t}_rate'/100) else 0
#             term = self.InterestRates.term if self.InterestRates.term else 0
#         else:
#             interest_rate = 0
#             term = 30
#         # interest_rate = self.InterestRates.averageinterestrate/100 if self.InterestRates.averageinterestrate else 0
#         total_loan =self.determine_total_loan_payment_per_year()/12
#         outstanding_loan_per_year = []
#         for t in range(1, term + 1):
#             if t > term:
#                 outstanding_loan_per_year.append(0)
#             else:
#
#                 outstanding_loan = (total_loan * (1-(1 + interest_rate/12)**(-(term - t) * 12))/(interest_rate/12))
#                 outstanding_loan_per_year.append(outstanding_loan)
#         return outstanding_loan_per_year
#     def determine_equity_per_year(self):
#         property_value_per_year = self.determine_property_value()
#         outstanding_loan_per_year = self.determine_outstanding_loan_per_year()
#         equity_per_year = []
#         for i in range(len(property_value_per_year)):
#             equity = property_value_per_year[i] - outstanding_loan_per_year[i]
#             equity_per_year.append(equity)
#             return equity_per_year
#     #determine loan interest
#     def determine_loan_interest(self):
#         if self.InterestRates:
#
#             term = self.InterestRates.term if self.InterestRates.term else 0
#         else:
#
#             term = 30
#         total_loan = self.determine_total_loan_payment_per_year()
#         loan_principal = self.determine_loan_interest()
#         loan_interest = []
#         for year in range(1, term + 1):
#             interest = total_loan[year-1] * loan_principal[year-1]
#             loan_interest.append(interest)
#         return loan_interest
#     #use total loan payment function instead of ousttanding loan
#     def determine_loan_principal(self):
#         if self.InterestRates:
#
#             term = self.InterestRates.term if self.InterestRates.term else 0
#         else:
#
#             term = 30
#         outstanding_loan_per_year = self.determine_outstanding_loan_per_year()
#
#         loan_principal = []
#         for year in range(1, term + 1):
#             principal = outstanding_loan_per_year[year-1] - outstanding_loan_per_year[year]
#             # total_loan_per_year[t-1] - total_loan_per_year[t]
#             loan_principal.append(principal)
#         return loan_principal
#     #function to calculate the total loan amount....revisit this formula
#     def determine_total_loan_payment_per_year(self, interest_change_year=None, new_interest_rate=None):
#         bond_price = self.bond_value
#         if self.InterestRates:
#             # current_year = 2 # let's say this is the current year you are calculating for
#             # year_amount_field = f'year_{current_year}_amount
#             interest_rate = getattr(self.InterestRates,f'year_{i}_rate'/100) if getattr(self.InterestRates,f'year_{i}_rate'/100) else 0
#
#             # interest_rate = getattr(self.InterestRates, year_amount_field) / 100 if getattr(self.InterestRates, year_amount_field) else 0
#             term = self.InterestRates.term if self.InterestRates.term else 0
#         else:
#             interest_rate = 0
#             term = 30
#
#         payments_per_year = []
#         for i in range(term):
#             if i > term:
#                 payments_per_year.append(0)
#             else:
#                 if interest_change_year is None or new_interest_rate is None:
#                     payment = bond_price * (interest_rate/12 * ((1 + interest_rate/12)**(term -i * 12)) / (((1 + interest_rate/12)**(term - i * 12)) - 1)) * 12
#                 else:
#                     if interest_change_year > term:
#                         raise ValueError("Interest change year cannot be greater than loan term.")
#                     if i == interest_change_year - 1:
#                         interest_rate = new_interest_rate / 100
#                     payment = bond_price * (interest_rate/12 * ((1 + interest_rate/12)**(term -i * 12)) / (((1 + interest_rate/12)**(term - i * 12)) - 1)) * 12
#                 payments_per_year.append(payment)
#                 bond_price -= payment#to get the remaining loan to be used for the next iteration
#         return payments_per_year
#     #code to determine property expenses.
#     #call this on an instance property_expenses = property_object.determine_property_expenses()
#     # def determine_gross_rental_income(self, years=30):
#     #     rental_income = self.RentalIncome.amount * 12
#     #     management_expenses = self.managementexpenses.expenses * 12
#     #     gross_rental_income = []
#     #     for year in range(1, years+1):
#     #         income = rental_income - management_expenses
#     #         gross_rental_income.append(income)
#     #     return gross_rental_income
#     def determine_property_expenses_per_year(self, years=30):
#         if self.MonthlyExpense:
#             monthly_expense = list(self.MonthlyExpense.value if self.MonthlyExpense.value else 0)
#
#         else:
#             monthly_expense = 0
#
#
#         property_expenses_per_year = []
#         for year in range(1, years+1):
#             expenses = monthly_expense * 12
#             property_expenses_per_year.append(expenses)
#         return property_expenses_per_year
#     #determine the total property expenses per year
#     def determine_total_property_expenses_per_year(self, years=30):
#         property_expenses_per_year = self.determine_property_expenses_per_year(years)
#         if self.MonthlyExpense:
#             special_expenses = list(getattr(self.specialexpenses, f'year_{year}_amount') if getattr(self.specialexpenses, f'year_{year}_amount') else 0)
#
#         else:
#             special_expenses = [0] * years
#
#
#         if self.OwnRenovations:
#             ownrenovations = list(getattr(self.OwnRenovations, f'year_{year}_amount') if getattr(self.OwnRenovations, f'year_{year}_amount') else 0)
#
#         else:
#             ownrenovations = [0] * years
#         if self.LoanRenovations:
#             ownrenovations = list(getattr(self.LoanRenovations, f'year_{year}_amount') if getattr(self.LoanRenovations, f'year_{year}_amount') else 0)
#
#         else:
#             loanrenovations = [0] * years
#         if self.repairs_maintenance:
#
#             repairsmaintenance = list(getattr(self.repairs_maintenance, f'year_{year}_amount') if getattr(self.repairs_maintenance, f'year_{year}_amount') else 0)
#
#         else:
#             repairsmaintenance = [0] * years
#
#
#         total_property_expenses_per_year = []
#         for year in range(1, years+1):
#             expenses = special_expenses[year-1] + property_expenses_per_year[year-1] + loanrenovations[year-1]+ ownrenovations[year-1] + repairsmaintenance[year-1]
#             total_property_expenses_per_year.append(expenses)
#         return total_property_expenses_per_year
#     #determine pre-tax cash flow
#     def determine_pre_tax_cash_flow_per_year(self, years=30):
#         gross_rental_income = self.determine_gross_rental_income(years)
#         total_property_expenses = self.determine_total_property_expenses_per_year(years)
#
#         pre_tax_cash_flow = []
#         for year in range(1, years + 1):
#             cash_flow = gross_rental_income[year - 1] - total_property_expenses[year - 1]
#             pre_tax_cash_flow.append(cash_flow)
#
#         return pre_tax_cash_flow
#     #determine cash outflow initial
#     def determine_initial_capital_outflow_per_year(self, years=30):
#         deposit = self.deposit
#         if self.other_cost:
#             other_costs = self.other_cost.other_costs
#         else:
#             other_costs = 0
#         # other_costs = self.other_cost.other_costs
#         initial_capital_outflow_per_year = []
#         for year in range(1, years+1):
#             outflow = deposit + other_costs
#             initial_capital_outflow_per_year.append(outflow)
#         return initial_capital_outflow_per_year
#     #pre tax cash on cash
#     def determine_pre_tax_cash_on_cash(self, years=30):
#         pre_tax_cash_flow_per_year = self.determine_pre_tax_cash_flow_per_year(years)
#         initial_capital_outflow_per_year = self.determine_initial_capital_outflow_per_year(years)
#         pre_tax_cash_on_cash = []
#         for year in range(1, years+1):
#             cash_on_cash = (pre_tax_cash_flow_per_year[year-1] / initial_capital_outflow_per_year[year-1]) * 100
#             pre_tax_cash_on_cash.append(cash_on_cash)
#         return pre_tax_cash_on_cash
#     #total taxable deductions
#     def determine_taxable_deductions(self, years=30):
#         loan_interest = self.determine_loan_interest()
#         total_property_expenses = self.determine_total_property_expenses_per_year(years)
#         taxable_deductions = []
#         for year in range(1, years+1):
#             deductions = loan_interest[year-1] + total_property_expenses[year-1]
#             taxable_deductions.append(deductions)
#         return taxable_deductions
#     # rental income per month
#     def determine_income_per_month(self, years=30):
#         after_tax_cashflow = self.determine_after_tax_cashflow(years)
#         income_per_month = []
#         for year in range(1, years+1):
#             income = after_tax_cashflow[year-1] / 12
#             income_per_month.append(income)
#         return income_per_month
#     def determine_gross_rental_income(self, years=30):
#         if self.RentalIncome:
#             rental_income =list(self.RentalIncome.amount * 12 if self.RentalIncome.amount * 12 else 0)
#             management_expenses = list(self.managementexpenses.managementfeeperyear * 12 if self.managementexpenses.managementfeeperyear * 12 else 0)
#         else:
#             rental_income = 0
#             management_expenses = 0
#         # rental_income = self.RentalIncome.get(property=self).amount * 12
#
#
#         gross_rental_income = []
#         for year in range(1, years+1):
#             income = rental_income - management_expenses
#             gross_rental_income.append(income)
#         return gross_rental_income
#     #depreciation
#     def calculate_depreciation(self, depreciation_type='straight'):
#         if depreciation_type == 'straight':
#
#             try:
#
#                 rate = self.Depreciation.rate/100
#
#             except AttributeError:
#                 rate = 0
#             try:
#
#                 rate = self.Depreciation.years
#
#             except AttributeError:
#                 years = 30
#             purchase_date = self.purchase_date
#             purchase_price = self.purchase_price
#
#             annual_depreciation = purchase_price * rate
#             # diminishing annual_depreciation = purchase_price*(rate*(years-year+1))/years
#             total_depreciation = annual_depreciation * years
#             remaining_value = purchase_price - total_depreciation
#
#             depreciation_schedule = []
#             for year in range(1, years+1):
#                 current_date = purchase_date + timedelta(days=365*year)
#                 current_depreciation = annual_depreciation*year
#                 depreciation_schedule.append({
#                     'year': year,
#                     'date': current_date,
#                     'depreciation': current_depreciation,
#                     'remaining_value': remaining_value
#                 })
#             return depreciation_schedule
#         #taxable amount
#     def calculate_taxable_amount(self, years=30):
#         gross_rental_income = self.determine_gross_rental_income(years)
#         taxable_deductions = self.determine_taxable_deductions(years)
#         taxable_amount = []
#         for year in range(1, years+1):
#             amount = gross_rental_income[year-1] - taxable_deductions[year-1]
#             taxable_amount.append(amount)
#         return taxable_amount
#     #sample tax-credt formula
#     def determine_tax_credits(self, years=30):
#         taxable_deductions = self.determine_taxable_deductions(years)
#         tax_credits = []
#         for year in range(1, years+1):
#             credit = taxable_deductions[year-1] * 0.3
#             tax_credits.append(credit)
#         return tax_credits
#     #after tax cash flow
#     def determine_after_tax_cashflow(self, years=30):
#         pre_tax_cashflow = self.determine_pre_tax_cash_flow_per_year(years)
#         tax_credits = self.determine_tax_credits(years)
#         after_tax_cashflow = []
#         for year in range(1, years+1):
#             cashflow = pre_tax_cashflow[year-1] - tax_credits[year-1]
#             after_tax_cashflow.append(cashflow)
#         return after_tax_cashflow
#     #income per month
#     def determine_income_per_month(self, years=30):
#         after_tax_cashflow = self.determine_after_tax_cashflow(years)
#         income_per_month = []
#         for year in range(1, years+1):
#             income = after_tax_cashflow[year-1] / 12
#             income_per_month.append(income)
#         return income_per_month
#     #after cash on cash
#     def determine_after_tax_cash_on_cash(self, years=30):
#         after_tax_cashflow = self.determine_after_tax_cashflow(years)
#         initial_cash_outflow = self.determine_initial_capital_outflow_per_year(years)
#         after_tax_cash_on_cash = []
#         for year in range(1, years+1):
#             cash_on_cash = (after_tax_cashflow[year-1] / initial_cash_outflow[year-1]) * 100
#             after_tax_cash_on_cash.append(cash_on_cash)
#         return after_tax_cash_on_cash
#
# # def determine_irr(self, years=30):
# #     after_tax_cashflow = self.determine_after_tax_cashflow(years)
# #     initial_capital_outflow_per_year = self.determine_initial_capital_outflow_per_year(years)
# #     irr_list = []
# #     for year in range(1, years+1):
# #         cashflows = after_tax_cashflow[:year] + [-initial_capital_outflow_per_year[year-1]]
# #         irr = root(lambda r: sum([cf/(1+r)**(year-i) for i, cf in enumerate(cashflows)]), 0.1).x[0]
# #         irr_list.append(irr)
# #     return irr_list
#
#     #from scipy.optimize import root_scalar
#
# # def determine_irr(self, years=30):
# #     after_tax_cashflow = self.determine_after_tax_cashflow(years)
# #     initial_outflow = self.determine_initial_capital_outflow_per_year(years)[0]
# #     def net_present_value(rate):
# #         npv = 0
# #         for i in range(years):
# #             npv += after_tax_cashflow[i] / (1 + rate)**(i+1)
# #         npv -= initial_outflow
# #         return npv
# #     irr = root_scalar(net_present_value, bracket=[-1, 1]).root
# #     return irr
#     # def determine_equity(self):
#     #     property_value = self.determine_property_value()
#     #     loan_amount = self.determine_outstanding_loan_per_year()
#     #     equity = []
#     #     return equity
#     # def determine_outstanding_loan(self):
#     #     interest_rate = self.InterestRates.rate/100
#     #     term = self.InterestRates.term
#     #     outstanding_loan = self.bond_value * (1 + interest_rate)**term
#     #     return outstanding_loan
#     #property = Property.objects.get(id=1)
#     # outstanding_loan = property.determine_outstanding_loan()
#     # print(outstanding_loan)
#     @property
#     def market_value(self):
#         # assumption -> market value is based on depreciation
#         today = date.today()
#         diff = self.purchase_date - (today)
#         period = diff.days
#         value = self.purchase_price - (period * 100.60)
#         return value
#     @property
#     def irr_year_one(self):
#         initial_investment = -1 * self.purchase_price
#         irr_calc = round(npf.irr([initial_investment, 39, 59, 55, 20]), 4) * 100
#         irr = round(irr_calc, 2)
#         return irr
#
#     @property
#     def irr_year_two(self):
#         initial_investment = -1 * self.purchase_price
#         irr_calc = round(npf.irr([initial_investment, -39, 5900, -2000, 20]), 4) * 100
#         irr = round(irr_calc, 2)
#         return irr
#
#     @property
#     def irr_year_three(self):
#         initial_investment = -1 * self.purchase_price
#         irr_calc = round(npf.irr([initial_investment, -39, 59, -6000, 20000]), 4) * 100
#         irr = round(irr_calc, 2)
#         return irr
#
#     @property
#     def irr_year_four(self):
#         initial_investment = -1 * self.purchase_price
#         irr_calc = round(npf.irr([initial_investment, -3999, 59, -9000, 20000]), 4) * 100
#         irr = round(irr_calc, 2)
#         return irr
#
#
