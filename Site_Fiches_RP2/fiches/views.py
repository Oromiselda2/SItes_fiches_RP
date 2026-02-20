from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q 
from .models import Fiche, SectionPhysique, SectionCaractere, SectionHistoire, SectionAutres, Server  # ← Ajoutez Server
from .forms import (
    FicheForm, 
    SectionPhysiqueForm, 
    SectionCaractereForm, 
    SectionHistoireForm, 
    SectionAutresForm
)


def fiche_list(request):
    """Liste toutes les fiches non supprimées"""
    fiches = Fiche.objects.filter(is_deleted=False).select_related('server', 'author').order_by('-created_at')
    return render(request, 'fiches/fiche_list.html', {'fiches': fiches})


def fiche_detail(request, pk):
    """Détail d'une fiche avec toutes ses sections"""
    fiche = get_object_or_404(Fiche, pk=pk, is_deleted=False)
    
    # Récupérer toutes les sections (elles seront créées automatiquement si elles n'existent pas)
    physique, _ = SectionPhysique.objects.get_or_create(fiche=fiche)
    caractere, _ = SectionCaractere.objects.get_or_create(fiche=fiche)
    histoire, _ = SectionHistoire.objects.get_or_create(fiche=fiche)
    autres, _ = SectionAutres.objects.get_or_create(fiche=fiche)
    
    context = {
        'fiche': fiche,
        'physique': physique,
        'caractere': caractere,
        'histoire': histoire,
        'autres': autres,
    }
    
    return render(request, 'fiches/fiche_detail.html', context)


@login_required
@transaction.atomic
def fiche_create(request):
    """Créer une nouvelle fiche avec toutes ses sections"""
    if request.method == 'POST':
        fiche_form = FicheForm(request.POST, request.FILES)
        physique_form = SectionPhysiqueForm(request.POST)
        caractere_form = SectionCaractereForm(request.POST)
        histoire_form = SectionHistoireForm(request.POST)
        autres_form = SectionAutresForm(request.POST)
        
        if all([fiche_form.is_valid(), physique_form.is_valid(), caractere_form.is_valid(), 
                histoire_form.is_valid(), autres_form.is_valid()]):
            
            # Créer la fiche
            fiche = fiche_form.save(commit=False)
            fiche.author = request.user
            fiche.save()
            
            # Créer les sections
            physique = physique_form.save(commit=False)
            physique.fiche = fiche
            physique.save()
            
            caractere = caractere_form.save(commit=False)
            caractere.fiche = fiche
            caractere.save()
            
            histoire = histoire_form.save(commit=False)
            histoire.fiche = fiche
            histoire.save()
            
            autres = autres_form.save(commit=False)
            autres.fiche = fiche
            autres.save()
            
            messages.success(request, f"Fiche '{fiche}' créée avec succès !")
            return redirect('fiche_detail', pk=fiche.pk)
    else:
        fiche_form = FicheForm()
        physique_form = SectionPhysiqueForm()
        caractere_form = SectionCaractereForm()
        histoire_form = SectionHistoireForm()
        autres_form = SectionAutresForm()
    
    context = {
        'fiche_form': fiche_form,
        'physique_form': physique_form,
        'caractere_form': caractere_form,
        'histoire_form': histoire_form,
        'autres_form': autres_form,
        'is_edit': False,
    }
    
    return render(request, 'fiches/fiche_form.html', context)


@login_required
@transaction.atomic
def fiche_edit(request, pk):
    """Modifier une fiche existante et toutes ses sections"""
    fiche = get_object_or_404(Fiche, pk=pk)
    
    # Seul l'auteur peut modifier
    if fiche.author != request.user:
        messages.error(request, "Vous ne pouvez pas modifier cette fiche.")
        return redirect('fiche_detail', pk=pk)
    
    # Récupérer ou créer les sections
    physique, _ = SectionPhysique.objects.get_or_create(fiche=fiche)
    caractere, _ = SectionCaractere.objects.get_or_create(fiche=fiche)
    histoire, _ = SectionHistoire.objects.get_or_create(fiche=fiche)
    autres, _ = SectionAutres.objects.get_or_create(fiche=fiche)
    
    if request.method == 'POST':
        fiche_form = FicheForm(request.POST, request.FILES, instance=fiche)
        physique_form = SectionPhysiqueForm(request.POST, instance=physique)
        caractere_form = SectionCaractereForm(request.POST, instance=caractere)
        histoire_form = SectionHistoireForm(request.POST, instance=histoire)
        autres_form = SectionAutresForm(request.POST, instance=autres)
        
        if all([fiche_form.is_valid(), physique_form.is_valid(), caractere_form.is_valid(), 
                histoire_form.is_valid(), autres_form.is_valid()]):
            
            fiche_form.save()
            physique_form.save()
            caractere_form.save()
            histoire_form.save()
            autres_form.save()
            
            messages.success(request, f"Fiche '{fiche}' modifiée avec succès !")
            return redirect('fiche_detail', pk=fiche.pk)
    else:
        fiche_form = FicheForm(instance=fiche)
        physique_form = SectionPhysiqueForm(instance=physique)
        caractere_form = SectionCaractereForm(instance=caractere)
        histoire_form = SectionHistoireForm(instance=histoire)
        autres_form = SectionAutresForm(instance=autres)
    
    context = {
        'fiche': fiche,
        'fiche_form': fiche_form,
        'physique_form': physique_form,
        'caractere_form': caractere_form,
        'histoire_form': histoire_form,
        'autres_form': autres_form,
        'is_edit': True,
    }
    
    return render(request, 'fiches/fiche_form.html', context)


@login_required
def fiche_delete(request, pk):
    """Supprimer (soft delete) une fiche"""
    fiche = get_object_or_404(Fiche, pk=pk)
    
    # Seul l'auteur peut supprimer
    if fiche.author != request.user:
        messages.error(request, "Vous ne pouvez pas supprimer cette fiche.")
        return redirect('fiche_detail', pk=pk)
    
    if request.method == 'POST':
        fiche.is_deleted = True
        fiche.save()
        messages.success(request, f"Fiche '{fiche}' supprimée avec succès !")
        return redirect('fiche_list')
    
    return render(request, 'fiches/fiche_confirm_delete.html', {'fiche': fiche})


def search_fiches(request):
    """Rechercher des fiches par nom de personnage ou nom d'utilisateur"""
    query = request.GET.get('q', '')
    
    if query:
        fiches = Fiche.objects.filter(
            is_deleted=False
        ).filter(
            Q(prenom__icontains=query) |
            Q(nom__icontains=query) |
            Q(author__username__icontains=query)
        ).select_related('server', 'author').order_by('-created_at')
    else:
        fiches = Fiche.objects.none()
    
    all_servers = Server.objects.all().order_by('name')
    
    context = {
        'fiches': fiches,
        'query': query,
        'all_servers': all_servers,
    }
    
    return render(request, 'fiches/search_results.html', context)