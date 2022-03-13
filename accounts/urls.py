from django.urls import path
from . import views
from djgeojson.views import GeoJSONLayerView




urlpatterns = [
    path('', views.register , name='register'),
    path('owner/', views.ownerregister , name='ownerregister'),
    path('login/', views.login , name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ghanadiregister', views.ghanadiregister , name='ghanadiregister'),
    path('ghanadilogin/', views.ghanadilogin , name='ghanadilogin'),
    path('logout/', views.logout, name='logout'),

]
 