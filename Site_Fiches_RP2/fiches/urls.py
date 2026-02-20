from django.urls import path
from . import views

urlpatterns = [
    path('', views.fiche_list, name='fiche_list'),
    path('search/', views.search_fiches, name='search_fiches'),
    path('create/', views.fiche_create, name='fiche_create'),
    path('<int:pk>/', views.fiche_detail, name='fiche_detail'),
    path('<int:pk>/edit/', views.fiche_edit, name='fiche_edit'),
    path('<int:pk>/delete/', views.fiche_delete, name='fiche_delete'),
]