from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name="home"),
    # path('property/', views.propertylist, name="propertylist"),
    # path('property/<str:id>/', views.propertyitem, name="propertyitem"),
    # path('propertytype/', views.propertytype, name="propertytype"),
    # path('contactus/',views.contactus, name="contactus"),

    # path('login/', views.loginuser, name='login'),
    # path('logout', views.logoutuser, name='logout'),

    # path('administrator/',views.administrator, name="administrator"),
    # path('administrator/propertytype',views.admin_property_type, name='admin-propertytype'),
    # path('administrator/currency',views.admin_currency, name='admin-currency'),
    # path('administrator/region',views.admin_region, name='admin-region'),
    # path('administrator/location',views.admin_location, name='admin-location'),
    # path('administrator/images',views.admin_images, name='admin-images'),

]