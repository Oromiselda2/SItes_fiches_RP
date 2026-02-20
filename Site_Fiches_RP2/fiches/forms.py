from django import forms
from .models import Fiche, SectionPhysique, SectionCaractere, SectionHistoire, SectionAutres, Server


class FicheForm(forms.ModelForm):
    class Meta:
        model = Fiche
        fields = ['server', 'prenom', 'nom', 'avatar', 'css']
        widgets = {
            'server': forms.Select(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom du personnage'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du personnage'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'css': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'CSS personnalisé (optionnel)'}),
        }
        labels = {
            'server': 'Serveur Discord',
            'prenom': 'Prénom',
            'nom': 'Nom',
            'avatar': 'Avatar',
            'css': 'CSS personnalisé',
        }


class SectionPhysiqueForm(forms.ModelForm):
    class Meta:
        model = SectionPhysique
        fields = [
            'description', 
            'corpulence', 
            'traits_particuliers', 
            'poids', 
            'taille', 
            'genre',
            'date_naissance_rp',
            'age_manuel',
            'autres_infos',
            'css'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Description physique détaillée'}),
            'corpulence': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Mince, Athlétique, etc.'}),
            'traits_particuliers': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Cicatrices, tatouages, etc.'}),
            'poids': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 70 kg'}),
            'taille': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1m75'}),
            'genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Homme, Femme, Non-binaire, etc.'}),
            'date_naissance_rp': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'age_manuel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Laissez vide pour calcul automatique'}),
            'autres_infos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Autres informations physiques'}),
            'css': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'CSS personnalisé pour cette section'}),
        }
        labels = {
            'description': 'Description physique',
            'corpulence': 'Corpulence',
            'traits_particuliers': 'Traits particuliers',
            'poids': 'Poids',
            'taille': 'Taille',
            'genre': 'Genre',
            'date_naissance_rp': 'Date de naissance (RP)',
            'age_manuel': 'Âge (manuel)',
            'autres_infos': 'Autres informations',
            'css': 'CSS personnalisé',
        }


class SectionCaractereForm(forms.ModelForm):
    class Meta:
        model = SectionCaractere
        fields = ['contenu', 'css']
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Décrivez le caractère et la personnalité du personnage'}),
            'css': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'CSS personnalisé pour cette section'}),
        }
        labels = {
            'contenu': 'Caractère et personnalité',
            'css': 'CSS personnalisé',
        }


class SectionHistoireForm(forms.ModelForm):
    class Meta:
        model = SectionHistoire
        fields = ['contenu', 'css']
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Racontez l\'histoire du personnage'}),
            'css': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'CSS personnalisé pour cette section'}),
        }
        labels = {
            'contenu': 'Histoire du personnage',
            'css': 'CSS personnalisé',
        }


class SectionAutresForm(forms.ModelForm):
    class Meta:
        model = SectionAutres
        fields = ['contenu', 'css']
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Autres informations sur le personnage'}),
            'css': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'CSS personnalisé pour cette section'}),
        }
        labels = {
            'contenu': 'Autres informations',
            'css': 'CSS personnalisé',
        }


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['name', 'discord_server_id', 'icon', 'date_rp_reference', 'date_reelle_reference', 'ratio_temps', 'css']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du serveur'}),
            'discord_server_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID du serveur Discord'}),
            'icon': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL de l\'icône'}),
            'date_rp_reference': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'date_reelle_reference': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'ratio_temps': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 2.0 = 2 jours RP par jour réel'}),
            'css': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'CSS global du serveur'}),
        }
        labels = {
            'name': 'Nom du serveur',
            'discord_server_id': 'ID Discord',
            'icon': 'Icône',
            'date_rp_reference': 'Date RP de référence',
            'date_reelle_reference': 'Date réelle de référence',
            'ratio_temps': 'Ratio temps (jours RP / jour réel)',
            'css': 'CSS global',
        }