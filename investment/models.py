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


class CapitalGrowthRates(models.Model):
    average_capital_growth_rate = models.FloatField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)

    def add_year_rate(self, year, rate):
        PeriodRate.objects.create(interest_rate=self, year=year, rate=rate)


class PeriodRate(models.Model):
    year = models.PositiveSmallIntegerField()
    rate = models.FloatField()
    interest_rate = models.ForeignKey(InterestRates, on_delete=models.CASCADE)


class MonthlyExpense(models.Model):
    description = models.CharField(max_length=255, null=True)
    value = models.IntegerField(null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)


class OwnRenovations(models.Model):
    year = models.PositiveSmallIntegerField()
    amount = models.FloatField()
    income_per_year = models.FloatField()


class LoanRenovations(models.Model):
    year = models.PositiveSmallIntegerField()
    amount = models.FloatField()
    income_per_year = models.FloatField()


class RepairsMaintenance(models.Model):
    year = models.PositiveSmallIntegerField
    amount = models.IntegerField(null=True,default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)


class SpecialExpenses(models.Model):
    year = models.PositiveSmallIntegerField
    amount = models.IntegerField(null=True, default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)


class TaxOptions(models.Model):
    taxation_capacity = models.CharField(null=True,max_length=50,default='Interest & capital', choices=(
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
    tax_rate = models.FloatField(null=True)
    annual_taxable_income = models.FloatField(null=False)
    maximum_tax_rate = models.IntegerField(null=False)
    income = models.IntegerField(null=True)
    rate = models.IntegerField(null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)


class ManagementExpenses(models.Model):
    vacancy_rate = models.IntegerField(null=True,default=0)
    management_fee = models.IntegerField(null=True,default=0)
    management_fee_per_year = models.IntegerField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)


class AdditionalLoanPayments(models.Model):
    year = models.PositiveSmallIntegerField()
    amount = models.IntegerField(null=True, default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)


class CapitalIncome(models.Model):
    year = models.PositiveSmallIntegerField()
    amount = models.IntegerField(null=True,default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)


class RentalIncome(models.Model):
    rental_increase_type = models.CharField(('Type'),null=True,max_length=50,default='Interest & capital', choices=(
        ('capital', 'capital'),
        ('inflation', 'inflation'),
        ('percent', 'percent'),
    ))
    increase_percentage = models.IntegerField(('Increase Percentage (%)'))
    average_rental_income_per_month = models.FloatField(('Average Rental Income Per Month'),null=True)
    amount = models.IntegerField(('Amount'),null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)


class comparison(models.Model):
    description = models.CharField(max_length=255, null=True)
    rate = models.IntegerField(('Rate (%)'),null=True,default=0)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)

