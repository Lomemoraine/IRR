from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name="home"),
    # path('/logout', views.log_out_user, name="logout"),
    path('addproperty/', views.add_property, name="addproperty"),
    path('addimages/', views.addimages, name="addimages"),
    path('interestrates/', views.interestview, name="interestrates"),
    path('inflationrates/', views.inflationview, name="inflationrates"),
    path('property/<str:id>/', views.view_one_property, name="propertyitem"),
    path('index/', views.index, name="index"),
    path('editproperty/<int:pk>/', views.edit_property, name='editproperty'),
    #  path('update/<int:pk>', update_article, name='update_article'),
    # path('/editproperty/<str:pk>/', views.edit_property, name='editproperty'),
    path('login/', views.log_in, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout', views.log_out, name='logout'),
]