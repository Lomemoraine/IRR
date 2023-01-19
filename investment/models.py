from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField
import numpy_financial as npf




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
    amount = models.IntegerField(null=True, max_length=255)

    def __str__(self):
        return self.other_costs


class Property(models.Model):
    name = models.CharField(max_length=252, null=True)
    property_type = models.ForeignKey(PropertyType, null=True, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True, null=True)
    purchase_price = models.FloatField(null=True)
    deposit = models.FloatField(null=True)
    City = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    other_cost = models.ForeignKey(OtherCosts, null=True, on_delete=models.CASCADE)
    bond_value = models.IntegerField(max_length=252, null=True)
    notes = models.TextField(max_length=1260, null=True)
    CapitalGrowthRates = models.ForeignKey(CapitalGrowthRates,null=False,on_delete=models.CASCADE)
    InterestRates = models.ForeignKey(InterestRates,null=False,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def save_property(self):
        """Add property to database"""
        self.save()
    #determine the property value
    def determine_property_value(self, years):
        value = self.purchase_price
        rate = self.CapitalGrowthRates
        for year in range(years):
            value += value * (1+rate)
        return value
    #property = Property.objects.get(id=1)
    # property_value = property.determine_property_value(5)
    # print(property_value)
    #determine loan amount
    def determine_outstanding_loan_per_year(self):
        interest_rate = self.InterestRates.averageinterestrate/100
        term = self.InterestRates.term
        outstanding_loan_per_year = []
        for year in range(1, term + 1):
            outstanding_loan = self.bond_value * (1 + interest_rate)**year
            outstanding_loan_per_year.append(outstanding_loan)
        return outstanding_loan_per_year
    def determine_equity_per_year(self):
        property_value_per_year = self.determine_property_value()
        outstanding_loan_per_year = self.determine_outstanding_loan_per_year()
        equity_per_year = []
        for i in range(len(property_value_per_year)):
            equity = property_value_per_year[i] - outstanding_loan_per_year[i]
            equity_per_year.append(equity)
            return equity_per_year
    #determine loan interest
    def determine_loan_interest(self):
        interest_rate = self.InterestRates.rate/100
        term = self.InterestRates.term
        outstanding_loan_per_year = self.determine_outstanding_loan_per_year()
        loan_interest = []
        for year in range(1, term + 1):
            interest = outstanding_loan_per_year[year-1] * interest_rate
            loan_interest.append(interest)
        return loan_interest
    def determine_loan_principal(self):
        interest_rate = self.InterestRates.rate/100
        term = self.InterestRates.term
        outstanding_loan_per_year = self.determine_outstanding_loan_per_year()
        loan_interest = self.determine_loan_interest()
        loan_principal = []
        for year in range(1, term + 1):
            principal = outstanding_loan_per_year[year-1] - loan_interest[year-1]
            loan_principal.append(principal)
        return loan_principal
    # def determine_equity(self):
    #     property_value = self.determine_property_value()
    #     loan_amount = self.determine_outstanding_loan_per_year()
    #     equity = []
    #     return equity
    # def determine_outstanding_loan(self):
    #     interest_rate = self.InterestRates.rate/100
    #     term = self.InterestRates.term
    #     outstanding_loan = self.bond_value * (1 + interest_rate)**term
    #     return outstanding_loan
    #property = Property.objects.get(id=1)
    # outstanding_loan = property.determine_outstanding_loan()
    # print(outstanding_loan)
    @property
    def market_value(self):
        # assumption -> market value is based on depreciation
        today = date.today()
        diff = self.purchase_date - (today)
        period = diff.days
        value = self.purchase_price - (period * 100.60)
        return value

    @property
    def irr_year_one(self):
        initial_investment = -1 * self.purchase_price
        irr_calc = round(npf.irr([initial_investment, 39, 59, 55, 20]), 4) * 100
        irr = round(irr_calc, 2)
        return irr

    @property
    def irr_year_two(self):
        initial_investment = -1 * self.purchase_price
        irr_calc = round(npf.irr([initial_investment, -39, 5900, -2000, 20]), 4) * 100
        irr = round(irr_calc, 2)
        return irr

    @property
    def irr_year_three(self):
        initial_investment = -1 * self.purchase_price
        irr_calc = round(npf.irr([initial_investment, -39, 59, -6000, 20000]), 4) * 100
        irr = round(irr_calc, 2)
        return irr

    @property
    def irr_year_four(self):
        initial_investment = -1 * self.purchase_price
        irr_calc = round(npf.irr([initial_investment, -3999, 59, -9000, 20000]), 4) * 100
        irr = round(irr_calc, 2)
        return irr

class Images(models.Model):
    image = CloudinaryField('images',default='http://res.cloudinary.com/dim8pysls/image/upload/v1639001486'
                                    '/x3mgnqmbi73lten4ewzv.png')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
#contination models
class InterestRates(models.Model):

    type = models.CharField(null=True,max_length=50,default='Interest & capital', choices=(
        ('Interest & capital', 'Interest & capital'),
        ('Interest Only', 'Interest Only'),
       
    ))
    rate = models.IntegerField(null=True,max_length=255,default=10)
    averageinterestrate = models.FloatField(('Average Interest Rate (%)'),null=True,default=10)
    term = models.IntegerField(null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.term
    
class InflationRates(models.Model):

    rate = models.IntegerField(null=True,max_length=255,default=8)
    averageinflationrate = models.FloatField(('Average Inflation Rate (%)'),null=True,default=8)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.rate
    

class Depreciation(models.Model):

    type = models.CharField(null=True,max_length=50,default='Interest & capital', choices=(
        ('Straight', 'Straight'),
        ('Diminishing', 'Diminishing'),
       
    ))
    description = models.CharField(null=True,max_length=255)
    value = models.FloatField(null=True)
    rate = models.IntegerField(('Rate (%)'),null=True,max_length=255,default=8)
    years = models.IntegerField(null=True,max_length=255)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.rate
class CapitalGrowthRates(models.Model):

    rate = models.IntegerField(null=True,default=8)
    averagecapitalGrowthrate = models.FloatField(('Average Capital Growth Rate (%)'),null=False,default=8)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.rate
    
class MonthlyExpense(models.Model):
    
    description = models.CharField(max_length=255, null=True)
    value = models.IntegerField(null=True, max_length=255)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.description
    
class OwnRenovations(models.Model):
    
    incomeperyear = models.FloatField(('Income per year'),max_length=255, null=True,default=0)
    amount = models.IntegerField(null=True, max_length=255,default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.amount  
class LoanRenovations(models.Model):
    
    incomeperyear = models.FloatField(('Income per year'),max_length=255, null=True,default=0)
    amount = models.IntegerField(null=True, max_length=255,default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.amount  
class repairs_maintenance(models.Model):
    amount = models.IntegerField(null=True, max_length=255,default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.amount  
class specialexpenses(models.Model):
    
    amount = models.IntegerField(null=True, max_length=255,default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.amount  
class taxoptions(models.Model):

    taxationcapacity = models.CharField(null=True,max_length=50,default='Interest & capital', choices=(
        ('Personal', 'Personal'),
        ('close corporation', 'close corporation'),
        ('private company', 'private company'),
        ('trust', 'trust'),
       
    ))
    method = models.CharField(null=True,max_length=50,default='Interest & capital', choices=(
        ('0%', '0%'),
        ('Marginal', 'Marginal'),
        ('Use Tax Table', 'Use Tax Table'),
        ('Custom', 'Custom'),
       
    ))
    
    taxrate = models.FloatField(('Tax Rate(%)'),null=True)
    annualtaxableincome = models.FloatField(('Annual Taxableincome(%)'),null=False)
    maximumtaxrate = models.IntegerField(('Maximum Tax Rate (%)'),null=False,max_length=255)
    income = models.IntegerField(null=True,max_length=255)
    rate = models.IntegerField(null=True,max_length=255)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.rate
class managementexpenses(models.Model):
    
    vacancyrate = models.IntegerField(('Vacancy Rate (%)'),null=True, max_length=255,default=0)
    managementfee = models.IntegerField(('Management Fee (%)'),null=True, max_length=255,default=0)
    managementfeeperyear = models.IntegerField(('Management Fee per Year '))
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.vacancyrate
    
class Additionalloanpayments(models.Model):
    
    amount = models.IntegerField(null=True, max_length=255,default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
    

    def __str__(self):
        return self.amount
class Capitalincome(models.Model):
    
    amount = models.IntegerField(null=True, max_length=255,default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
    

    def __str__(self):
        return self.amount

class RentalIncome(models.Model):

    rentalincreasetype = models.CharField(null=True,max_length=50,default='Interest & capital', choices=(
        ('capital', 'capital'),
        ('inflation', 'inflation'),
        ('percent', 'percent'),
       
    ))
    increasepercentage = models.IntegerField(('Increase Percentage (%)'),max_length=255)
    averagerentalincomepermonth = models.FloatField(('Average Rental Income Per Month'),null=True)
    amount = models.IntegerField(('Amount'),null=True,max_length=255)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.rentalincreasetype
    
class comparison(models.Model):
    description = models.CharField(max_length=255, null=True)
    rate = models.IntegerField(('Rate (%)'),null=True, max_length=255,default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
    

    def __str__(self):
        return self.description
  