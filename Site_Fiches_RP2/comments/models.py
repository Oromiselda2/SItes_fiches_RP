from django.db import models
from django.conf import settings
from fiches.models import Fiche


class Comment(models.Model):
    fiche = models.ForeignKey(Fiche, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    
    content = models.TextField(verbose_name="Contenu du commentaire")
    is_approved = models.BooleanField(default=True, verbose_name="Approuvé")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
    
    def __str__(self):
        return f"Commentaire de {self.author} sur {self.fiche}"