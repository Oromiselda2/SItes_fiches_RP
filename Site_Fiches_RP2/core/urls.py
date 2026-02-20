from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Gestion utilisateurs (owner uniquement)
    path('owner/users/', views.manage_users, name='manage_users'),
    path('owner/users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('owner/users/<int:user_id>/roles/', views.user_edit_roles, name='user_edit_roles'),
    
    # Gestion serveurs (owner uniquement)
    path('owner/servers/', views.manage_servers, name='manage_servers'),
    path('owner/servers/<int:server_id>/', views.server_detail, name='server_detail'),
    path('owner/servers/<int:server_id>/add-admin/', views.server_add_admin, name='server_add_admin'),
    path('owner/servers/<int:server_id>/remove-admin/<int:user_id>/', views.server_remove_admin, name='server_remove_admin'),
]