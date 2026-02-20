from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    
    # Dashboards
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Gestion (owner uniquement)
    path('owner/users/', views.manage_users, name='manage_users'),
    path('owner/servers/', views.manage_servers, name='manage_servers'),
    path('owner/users/<int:user_id>/roles/', views.user_edit_roles, name='user_edit_roles'),
]