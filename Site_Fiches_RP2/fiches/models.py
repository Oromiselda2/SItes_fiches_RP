from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone


class Server(models.Model):
    discord_server_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    icon = models.URLField(null=True, blank=True)
    css = models.TextField(blank=True, help_text="CSS global du serveur")
    
    # Gestion des administrateurs du serveur
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='admin_servers',
        blank=True,
        help_text="Utilisateurs pouvant gérer ce serveur"
    )
    
    # Gestion du temps RP
    date_rp_reference = models.DateField(
        verbose_name="Date RP de référence",
        help_text="Date à laquelle correspond la date réelle de référence (ex: 1er janvier 2027)"
    )
    date_reelle_reference = models.DateField(
        verbose_name="Date réelle de référence",
        help_text="Date réelle correspondant à la date RP de référence"
    )
    ratio_temps = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=1.0,
        verbose_name="Ratio temps (jours RP / jour réel)",
        help_text="Ex: 2.0 = 2 jours RP pour 1 jour réel | 0.5 = 1 jour RP pour 2 jours réels"
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Serveur Discord"
        verbose_name_plural = "Serveurs Discord"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_date_rp_actuelle(self):
        """Calcule la date RP actuelle en fonction du ratio temps"""
        jours_reels_ecoules = (timezone.now().date() - self.date_reelle_reference).days
        jours_rp_ecoules = int(jours_reels_ecoules * float(self.ratio_temps))
        date_rp_actuelle = self.date_rp_reference + timedelta(days=jours_rp_ecoules)
        return date_rp_actuelle
    
    def is_admin(self, user):
        """Vérifie si un utilisateur est admin de ce serveur"""
        return user.is_owner or self.admins.filter(pk=user.pk).exists()


class Fiche(models.Model):
    # Relations
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='fiches')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fiches')
    
    # Informations toujours visibles (comme profil Instagram)
    prenom = models.CharField(max_length=200, verbose_name="Prénom")
    nom = models.CharField(max_length=200, blank=True, verbose_name="Nom")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Avatar")
    
    # Personnalisation CSS
    css = models.TextField(blank=True, help_text="CSS personnalisé pour cette fiche")
    
    # Métadonnées
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Fiche personnage"
        verbose_name_plural = "Fiches personnages"
    
    def __str__(self):
        return f"{self.prenom} {self.nom}".strip()


class SectionPhysique(models.Model):
    fiche = models.OneToOneField(Fiche, on_delete=models.CASCADE, related_name='physique')
    
    # Tout en texte libre
    description = models.TextField(blank=True, verbose_name="Description physique")
    corpulence = models.CharField(max_length=200, blank=True, verbose_name="Corpulence")
    traits_particuliers = models.TextField(blank=True, verbose_name="Traits particuliers")
    poids = models.CharField(max_length=100, blank=True, verbose_name="Poids")
    taille = models.CharField(max_length=100, blank=True, verbose_name="Taille")
    genre = models.CharField(max_length=200, blank=True, verbose_name="Genre")
    
    # Date de naissance (dans le calendrier RP)
    date_naissance_rp = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Date de naissance (RP)",
        help_text="Date de naissance dans le temps du RP"
    )
    
    # Âge manuel (si on ne veut pas utiliser le calcul automatique)
    age_manuel = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Âge (manuel)",
        help_text="Laissez vide pour calcul automatique basé sur la date de naissance RP"
    )
    
    # Champs supplémentaires libres
    autres_infos = models.TextField(blank=True, verbose_name="Autres informations physiques")
    
    # CSS personnalisé pour cette section
    css = models.TextField(blank=True, help_text="CSS personnalisé pour la section Physique")
    
    class Meta:
        verbose_name = "Section Physique"
        verbose_name_plural = "Sections Physique"
    
    def __str__(self):
        return f"Physique - {self.fiche}"
    
    def get_age(self):
        """Calcule l'âge en fonction de la date RP actuelle du serveur"""
        if self.age_manuel:
            return self.age_manuel
        
        if not self.date_naissance_rp:
            return "Non renseigné"
        
        date_rp_actuelle = self.fiche.server.get_date_rp_actuelle()
        
        age = date_rp_actuelle.year - self.date_naissance_rp.year
        
        # Ajustement si l'anniversaire n'est pas encore passé cette année
        if (date_rp_actuelle.month, date_rp_actuelle.day) < (self.date_naissance_rp.month, self.date_naissance_rp.day):
            age -= 1
        
        return f"{age} ans"


class SectionCaractere(models.Model):
    fiche = models.OneToOneField(Fiche, on_delete=models.CASCADE, related_name='caractere')
    
    # Contenu totalement libre
    contenu = models.TextField(blank=True, verbose_name="Caractère et personnalité")
    
    # CSS personnalisé
    css = models.TextField(blank=True, help_text="CSS personnalisé pour la section Caractère")
    
    class Meta:
        verbose_name = "Section Caractère"
        verbose_name_plural = "Sections Caractère"
    
    def __str__(self):
        return f"Caractère - {self.fiche}"


class SectionHistoire(models.Model):
    fiche = models.OneToOneField(Fiche, on_delete=models.CASCADE, related_name='histoire')
    
    # Contenu totalement libre
    contenu = models.TextField(blank=True, verbose_name="Histoire du personnage")
    
    # CSS personnalisé
    css = models.TextField(blank=True, help_text="CSS personnalisé pour la section Histoire")
    
    class Meta:
        verbose_name = "Section Histoire"
        verbose_name_plural = "Sections Histoire"
    
    def __str__(self):
        return f"Histoire - {self.fiche}"


class SectionAutres(models.Model):
    fiche = models.OneToOneField(Fiche, on_delete=models.CASCADE, related_name='autres')
    
    # Contenu totalement libre
    contenu = models.TextField(blank=True, verbose_name="Autres informations")
    
    # CSS personnalisé
    css = models.TextField(blank=True, help_text="CSS personnalisé pour la section Autres")
    
    class Meta:
        verbose_name = "Section Autres"
        verbose_name_plural = "Sections Autres"
    
    def __str__(self):
        return f"Autres - {self.fiche}"