from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from fiches.models import Fiche
from .models import Comment
from .forms import CommentForm


@login_required
def comment_create(request, fiche_pk):
    """Ajouter un commentaire à une fiche"""
    fiche = get_object_or_404(Fiche, pk=fiche_pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.fiche = fiche
            comment.save()
            messages.success(request, "Commentaire ajouté !")
            return redirect('fiche_detail', pk=fiche.pk)
    else:
        form = CommentForm()
    
    return render(request, 'comments/comment_form.html', {'form': form, 'fiche': fiche})


@login_required
def comment_edit(request, pk):
    """Modifier un commentaire"""
    comment = get_object_or_404(Comment, pk=pk)
    
    # Seul l'auteur peut modifier
    if comment.author != request.user:
        messages.error(request, "Vous ne pouvez pas modifier ce commentaire.")
        return redirect('fiche_detail', pk=comment.fiche.pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Commentaire modifié !")
            return redirect('fiche_detail', pk=comment.fiche.pk)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'comments/comment_form.html', {'form': form, 'comment': comment})


@login_required
def comment_delete(request, pk):
    """Supprimer un commentaire"""
    comment = get_object_or_404(Comment, pk=pk)
    fiche_pk = comment.fiche.pk
    
    # Seul l'auteur peut supprimer
    if comment.author != request.user:
        messages.error(request, "Vous ne pouvez pas supprimer ce commentaire.")
        return redirect('fiche_detail', pk=fiche_pk)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Commentaire supprimé !")
        return redirect('fiche_detail', pk=fiche_pk)
    
    return render(request, 'comments/comment_confirm_delete.html', {'comment': comment})