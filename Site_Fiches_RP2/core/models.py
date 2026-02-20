from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class User(AbstractUser):
    discord_id = models.CharField(max_length=50, unique=True, null=True)
    discord_username = models.CharField(max_length=100, blank=True)
    discord_discriminator = models.CharField(max_length=10, blank=True)
    avatar = models.URLField(null=True, blank=True)
    is_owner = models.BooleanField(default=False)
    roles = models.ManyToManyField(Role, blank=True)
    
    def save(self, *args, **kwargs):
        # Automatiquement définir is_owner si c'est votre Discord ID
        if self.discord_id == '1092106789937492079':
            self.is_owner = True
        super().save(*args, **kwargs)
    
    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()
    
    @property
    def discord_tag(self):
        if self.discord_discriminator and self.discord_discriminator != '0':
            return f"{self.discord_username}#{self.discord_discriminator}"
        return self.discord_username

class AuditLog(models.Model):
    ACTIONS = [
        ('create_fiche', 'Create Fiche'),
        ('edit_fiche', 'Edit Fiche'),
        ('delete_fiche', 'Delete Fiche'),
        ('comment', 'Comment'),
        ('role_add', 'Role Add'),
        ('role_remove', 'Role Remove'),
        ('server_create', 'Server Create'),
        ('server_edit', 'Server Edit'),
        ('server_delete', 'Server Delete'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50, choices=ACTIONS)
    fiche_id = models.IntegerField(null=True, blank=True)
    server_id = models.IntegerField(null=True, blank=True)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Log d'audit"
        verbose_name_plural = "Logs d'audit"