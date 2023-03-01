from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Property)
admin.site.register(PropertyType)
admin.site.register(OtherCosts)
admin.site.register(InterestRates)
admin.site.register(Images)
admin.site.register(InflationRates)
admin.site.register(Depreciation)
admin.site.register(CapitalGrowthRates)
admin.site.register(PeriodRate)
admin.site.register(MonthlyExpense)
admin.site.register(OwnRenovations)
admin.site.register(LoanRenovations)
admin.site.register(RepairsMaintenance)
admin.site.register(SpecialExpenses)
admin.site.register(TaxOptions)
admin.site.register(ManagementExpenses)
admin.site.register(AdditionalLoanPayments)
admin.site.register(CapitalIncome)
admin.site.register(RentalIncome)
admin.site.register(Comparison)
admin.site.register(TaxOptionsIncome)


