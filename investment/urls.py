from django.urls import path
from . import views

urlpatterns = [
    # Authentication urls
    path('logout/', views.log_out, name="logout"),
    path('login/', views.log_in, name='login'),
    path('signup/', views.signup, name='signup'),

    # Landing Page
    path('', views.welcome, name="home"),

    # Property manipulation ur;s
    path('addproperty/', views.add_property, name="addproperty"),
    path('editproperty/<int:pk>/', views.edit_property, name='editproperty'),
    path('property/<str:id>/', views.view_one_property, name="propertyitem"),

    # Others
    path('addimages/<int:pk>/', views.addimages, name="addimages"),
    path('interestrates/<int:pk>/', views.interestview, name="interestrates"),
    path('inflationrates/<int:pk>/', views.inflation_view, name="inflationrates"),
    path('depreciation/<int:pk>/', views.depreciation_view, name="depreciation"),
    path('capitalgrowth/<int:pk>/', views.capital_growth_view, name="capitalgrowth"),
    path('monthlyexpense/<int:pk>/', views.monthly_expense_view, name="monthlyexpense"),
    path('ownrenovations/<int:pk>/', views.own_renovations_view, name="ownrenovations"),
    path('loanrenovations/<int:pk>/', views.loan_renovations_view, name="loanrenovations"),
    path('repairs_maintenance/<int:pk>/', views.repairs_maintenance_view, name="repairs_maintenance"),
    path('specialexpenses/<int:pk>/', views.special_expenses_view, name="specialexpenses"),
    path('taxoptions/<int:pk>/', views.tax_options_view, name="taxoptions"),
    path('managementexpenses/<int:pk>/', views.management_expenses_view, name="managementexpenses"),
    path('Additionalloanpayments/<int:pk>/', views.additional_loan_payments_view, name="Additionalloanpayments"),
    path('Capitalincome/<int:pk>/', views.capital_income_view, name="Capitalincome"),
    path('RentalIncome/<int:pk>/', views.rental_income_view, name="RentalIncome"),
    path('comparison/<int:pk>/', views.comparison_view, name="comparison"),
]

