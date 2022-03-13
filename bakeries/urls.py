from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.bakeries, name='bakeries'),
    path('zone/', views.bakerieszone, name='bakeries-zone'),
    path('mahsoolat/<int:id>/', views.mahsoolat, name='mahsoolat'),
    path('mahsool-jadid/<int:id>/', views.mahsool_jadid , name='mahsool-jadid'),
    path('mahsool-detail/<int:id>/', views.mahsool_detail, name='mahsool-detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:mahsool_id>/', views.submit_review, name='submit_review'),




]
     