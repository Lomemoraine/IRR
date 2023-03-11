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
    path('inflationrates/<int:pk>/', views.inflationview, name="inflationrates"),
    path('depreciation/<int:pk>/', views.depreciation_view, name="depreciation"),
    path('capitalgrowth/<int:pk>/', views.capital_growth_view, name="capitalgrowth"),
    path('monthlyexpense/<int:pk>/', views.MonthlyExpenseview, name="monthlyexpense"),
    path('ownrenovations/<int:pk>/', views.OwnRenovationsview, name="ownrenovations"),
    path('loanrenovations/<int:pk>/', views.LoanRenovationsview, name="loanrenovations"),
    path('repairs_maintenance/<int:pk>/', views.repairs_maintenanceview, name="repairs_maintenance"),
    path('specialexpenses/<int:pk>/', views.specialexpensesview, name="specialexpenses"),
    path('taxoptions/<int:pk>/', views.taxoptionsview, name="taxoptions"),
    path('managementexpenses/<int:pk>/', views.managementexpensesview, name="managementexpenses"),
    path('Additionalloanpayments/<int:pk>/', views.Additionalloanpaymentsview, name="Additionalloanpayments"),
    path('Capitalincome/<int:pk>/', views.Capitalincomeview, name="Capitalincome"),
    path('RentalIncome/<int:pk>/', views.RentalIncomeview, name="RentalIncome"),
    path('comparison/<int:pk>/', views.comparisonview, name="comparison"),
]

