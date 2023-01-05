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
    
    def __str__(self):
        return self.name

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
    term = models.IntegerField(null=True,max_length=255)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.term
    
class InflationRates(models.Model):

    rate = models.IntegerField(null=True,max_length=255,default=8)
    averageinflationrate = models.FloatField(('Average Inflation Rate (%)'),null=True,default=8)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.rate
    

