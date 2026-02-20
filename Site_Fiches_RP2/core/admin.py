from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, AuditLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'discord_id', 'is_owner', 'is_staff']
    list_filter = ['is_owner', 'is_staff', 'is_superuser', 'roles']
    search_fields = ['username', 'email', 'discord_id']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Discord Info', {'fields': ('discord_id', 'avatar')}),
        ('Permissions Custom', {'fields': ('is_owner', 'roles')}),
    )
    
    filter_horizontal = ['roles', 'groups', 'user_permissions']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'fiche_id', 'ip', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'ip']
    readonly_fields = ['user', 'action', 'fiche_id', 'old_value', 'new_value', 'ip', 'user_agent', 'created_at']
    
    def has_add_permission(self, request):
        return False  # Les logs ne doivent pas être créés manuellement
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Seul le superuser peut supprimer des logs