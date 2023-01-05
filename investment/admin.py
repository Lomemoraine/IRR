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


