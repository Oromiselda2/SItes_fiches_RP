from django.contrib import admin
from .models import Server, Fiche, SectionPhysique, SectionCaractere, SectionHistoire, SectionAutres


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ['name', 'discord_server_id', 'ratio_temps', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'discord_server_id']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['admins']
    
    fieldsets = (
        ('Informations Principales', {
            'fields': ('name', 'discord_server_id', 'icon', 'admins')
        }),
        ('Configuration Temps RP', {
            'fields': ('date_rp_reference', 'date_reelle_reference', 'ratio_temps')
        }),
        ('Personnalisation', {
            'fields': ('css',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class SectionPhysiqueInline(admin.StackedInline):
    model = SectionPhysique
    extra = 0
    fields = ['description', 'corpulence', 'traits_particuliers', 'poids', 'taille', 'genre', 
              'date_naissance_rp', 'age_manuel', 'autres_infos', 'css']


class SectionCaractereInline(admin.StackedInline):
    model = SectionCaractere
    extra = 0
    fields = ['contenu', 'css']


class SectionHistoireInline(admin.StackedInline):
    model = SectionHistoire
    extra = 0
    fields = ['contenu', 'css']


class SectionAutresInline(admin.StackedInline):
    model = SectionAutres
    extra = 0
    fields = ['contenu', 'css']


@admin.register(Fiche)
class FicheAdmin(admin.ModelAdmin):
    list_display = ['prenom', 'nom', 'author', 'server', 'is_deleted', 'created_at']
    list_filter = ['is_deleted', 'server', 'created_at']
    search_fields = ['prenom', 'nom', 'author__username', 'server__name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [SectionPhysiqueInline, SectionCaractereInline, SectionHistoireInline, SectionAutresInline]
    
    fieldsets = (
        ('Informations Principales', {
            'fields': ('server', 'author', 'prenom', 'nom', 'avatar', 'is_deleted')
        }),
        ('Personnalisation', {
            'fields': ('css',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SectionPhysique)
class SectionPhysiqueAdmin(admin.ModelAdmin):
    list_display = ['fiche', 'corpulence', 'taille', 'poids', 'genre']
    list_filter = ['genre']
    search_fields = ['fiche__prenom', 'fiche__nom']


@admin.register(SectionCaractere)
class SectionCaractereAdmin(admin.ModelAdmin):
    list_display = ['fiche']
    search_fields = ['fiche__prenom', 'fiche__nom', 'contenu']


@admin.register(SectionHistoire)
class SectionHistoireAdmin(admin.ModelAdmin):
    list_display = ['fiche']
    search_fields = ['fiche__prenom', 'fiche__nom', 'contenu']


@admin.register(SectionAutres)
class SectionAutresAdmin(admin.ModelAdmin):
    list_display = ['fiche']
    search_fields = ['fiche__prenom', 'fiche__nom', 'contenu']