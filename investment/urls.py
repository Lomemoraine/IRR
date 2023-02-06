from django.urls import path
from . import views

urlpatterns = [
    # Authentication urls
    path('/logout', views.log_out, name="logout"),
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
    path('depreciation/<int:pk>/', views.depreciationview, name="depreciation"),
]
# urlpatterns = [
#     path('', views.welcome, name="home"),
#     # path('/logout', views.log_out_user, name="logout"),
#     path('addproperty/', views.add_property, name="addproperty"),
#     path('addimages/', views.addimages, name="addimages"),
#     path('interestrates/', views.interestview, name="interestrates"),
#     path('inflationrates/', views.inflationview, name="inflationrates"),
#     path('depreciation/', views.depreciationview, name="depreciation"),
#     path('capitalgrowth/', views.CapitalGrowthview, name="capitalgrowth"),
#     path('monthlyexpense/', views.MonthlyExpenseview, name="monthlyexpense"),
#     path('ownrenovations/', views.OwnRenovationsview, name="ownrenovations"),
#     path('loanrenovations/', views.LoanRenovationsview, name="loanrenovations"),
#     path('repairs_maintenance/', views.repairs_maintenanceview, name="repairs_maintenance"),
#     path('specialexpenses/', views.specialexpensesview, name="specialexpenses"),
#     path('taxoptions/', views.taxoptionsview, name="taxoptions"),
#     path('managementexpenses/', views.managementexpensesview, name="managementexpenses"),
#     path('Additionalloanpayments/', views.Additionalloanpaymentsview, name="Additionalloanpayments"),
#     path('Capitalincome/', views.Capitalincomeview, name="Capitalincome"),
#     path('RentalIncome/', views.RentalIncomeview, name="RentalIncome"),
#     path('comparison/', views.comparisonview, name="comparison"),
#     path('property/<str:id>/', views.view_one_property, name="propertyitem"),
#     path('index/', views.index, name="index"),
#     path('editproperty/<int:pk>/', views.edit_property, name='editproperty'),
#     #  path('update/<int:pk>', update_article, name='update_article'),
#     # path('/editproperty/<str:pk>/', views.edit_property, name='editproperty'),
#     path('login/', views.log_in, name='login'),
#     path('signup/', views.signup, name='signup'),
#     path('logout', views.log_out, name='logout'),
# ]
#
