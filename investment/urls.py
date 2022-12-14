from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name="home"),
    path('/logout', views.log_out_user, name="logout"),
    path('/addproperty', views.add_property, name="addproperty"),
    path('/addimages', views.addimages, name="addimages"),
    path('/property/<str:id>/', views.view_one_property, name="propertyitem"),

    path('login/', views.login_user, name='login'),
    path('logout', views.log_out_user, name='logout'),
]