from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Property)
admin.site.register(PropertyType)
admin.site.register(OtherCosts)
admin.site.register(Images)
admin.site.register(InterestRates)
admin.site.register(InflationRates)
admin.site.register(Depreciation)
admin.site.register(CapitalGrowthRates)
admin.site.register(specialexpenses)
admin.site.register(MonthlyExpense)
admin.site.register(OwnRenovations)
admin.site.register(LoanRenovations)
admin.site.register(repairs_maintenance)
admin.site.register(managementexpenses)
admin.site.register(taxoptions)
admin.site.register(Additionalloanpayments)
admin.site.register(Capitalincome)
admin.site.register(RentalIncome)
admin.site.register(comparison)



