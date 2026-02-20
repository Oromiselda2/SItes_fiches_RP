from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from fiches.models import Fiche, Server
from comments.models import Comment
from .models import User, Role, AuditLog
from .decorators import owner_required, admin_or_owner_required

def login_view(request):
    """Page de connexion"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'core/login.html')


def home(request):
    """Page d'accueil"""
    recent_fiches = Fiche.objects.filter(is_deleted=False).select_related('server', 'author').order_by('-created_at')[:6]
    
    # Si l'utilisateur est connecté, récupérer ses serveurs
    user_servers = []
    if request.user.is_authenticated:
        # Serveurs où l'utilisateur a créé au moins une fiche
        user_servers = Server.objects.filter(
            Q(fiches__author=request.user) | 
            Q(admins=request.user)
        ).distinct().order_by('name')
    
    context = {
        'recent_fiches': recent_fiches,
        'user_servers': user_servers,
    }
    
    return render(request, 'core/home.html', context)


@login_required
def profile(request):
    """Profil utilisateur avec ses fiches"""
    user_fiches = Fiche.objects.filter(
        author=request.user, 
        is_deleted=False
    ).select_related('server').order_by('-created_at')
    
    # Statistiques utilisateur
    stats = {
        'total_fiches': user_fiches.count(),
        'total_comments': Comment.objects.filter(author=request.user).count(),
        'servers_count': Server.objects.filter(fiches__author=request.user).distinct().count(),
    }
    
    context = {
        'user_fiches': user_fiches,
        'stats': stats,
    }
    
    return render(request, 'core/profile.html', context)


def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')


@owner_required
def owner_dashboard(request):
    """Dashboard owner - accès complet à tout"""
    
    # Statistiques globales
    total_users = User.objects.count()
    total_servers = Server.objects.count()
    total_fiches = Fiche.objects.count()
    total_fiches_active = Fiche.objects.filter(is_deleted=False).count()
    total_comments = Comment.objects.count()
    
    # Utilisateurs actifs (connectés dans les 30 derniers jours)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_users = User.objects.filter(last_login__gte=thirty_days_ago).count()
    
    # Nouvelles inscriptions (7 derniers jours)
    seven_days_ago = timezone.now() - timedelta(days=7)
    new_users = User.objects.filter(date_joined__gte=seven_days_ago).count()
    
    # Fiches créées cette semaine
    new_fiches = Fiche.objects.filter(created_at__gte=seven_days_ago).count()
    
    # Derniers utilisateurs
    recent_users = User.objects.select_related().order_by('-date_joined')[:10]
    
    # Derniers serveurs
    recent_servers = Server.objects.annotate(
        fiche_count=Count('fiches', filter=Q(fiches__is_deleted=False)),
        user_count=Count('fiches__author', distinct=True, filter=Q(fiches__is_deleted=False))
    ).order_by('-created_at')[:10]
    
    # Dernières fiches
    recent_fiches = Fiche.objects.select_related('author', 'server').order_by('-created_at')[:15]
    
    # Logs d'audit récents
    recent_logs = AuditLog.objects.select_related('user').order_by('-created_at')[:30]
    
    # Utilisateurs les plus actifs (par nombre de fiches)
    top_creators = User.objects.annotate(
        fiche_count=Count('fiches', filter=Q(fiches__is_deleted=False))
    ).filter(fiche_count__gt=0).order_by('-fiche_count')[:10]
    
    # Serveurs les plus actifs (par nombre de fiches)
    top_servers = Server.objects.annotate(
        fiche_count=Count('fiches', filter=Q(fiches__is_deleted=False)),
        user_count=Count('fiches__author', distinct=True, filter=Q(fiches__is_deleted=False))
    ).filter(fiche_count__gt=0).order_by('-fiche_count')[:10]
    
    # Tous les serveurs pour la sidebar
    all_servers = Server.objects.all().order_by('name')
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'new_users': new_users,
        'total_servers': total_servers,
        'total_fiches': total_fiches,
        'total_fiches_active': total_fiches_active,
        'new_fiches': new_fiches,
        'total_comments': total_comments,
        'recent_users': recent_users,
        'recent_servers': recent_servers,
        'recent_fiches': recent_fiches,
        'recent_logs': recent_logs,
        'top_creators': top_creators,
        'top_servers': top_servers,
        'all_servers': all_servers,
    }
    
    return render(request, 'core/owner_dashboard.html', context)


@admin_or_owner_required
def admin_dashboard(request):
    """Dashboard admin - accès à la gestion des serveurs dont l'admin est responsable"""
    
    user = request.user
    
    if user.is_owner:
        # L'owner voit tous les serveurs
        managed_servers = Server.objects.all()
    else:
        # Les admins voient uniquement leurs serveurs
        managed_servers = user.admin_servers.all()
    
    # Statistiques pour les serveurs gérés
    total_fiches = Fiche.objects.filter(server__in=managed_servers, is_deleted=False).count()
    total_comments = Comment.objects.filter(fiche__server__in=managed_servers).count()
    total_users = User.objects.filter(fiches__server__in=managed_servers).distinct().count()
    
    # Serveurs avec leur nombre de fiches
    servers_with_stats = managed_servers.annotate(
        fiche_count=Count('fiches', filter=Q(fiches__is_deleted=False)),
        user_count=Count('fiches__author', distinct=True, filter=Q(fiches__is_deleted=False)),
        comment_count=Count('fiches__comments', filter=Q(fiches__is_deleted=False))
    ).order_by('-fiche_count')
    
    # Logs récents pour les serveurs gérés
    recent_logs = AuditLog.objects.filter(
        server_id__in=managed_servers.values_list('id', flat=True)
    ).select_related('user').order_by('-created_at')[:20]
    
    # Fiches récentes dans les serveurs gérés
    recent_fiches = Fiche.objects.filter(
        server__in=managed_servers,
        is_deleted=False
    ).select_related('author', 'server').order_by('-created_at')[:10]
    
    # Tous les serveurs pour la sidebar
    all_servers = Server.objects.all().order_by('name')
    
    context = {
        'total_servers': managed_servers.count(),
        'total_fiches': total_fiches,
        'total_comments': total_comments,
        'total_users': total_users,
        'servers': servers_with_stats,
        'recent_logs': recent_logs,
        'recent_fiches': recent_fiches,
        'is_owner': user.is_owner,
        'all_servers': all_servers,
    }
    
    return render(request, 'core/admin_dashboard.html', context)


@owner_required
def manage_users(request):
    """Gestion des utilisateurs (owner uniquement)"""
    
    # Filtres
    search = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    
    users = User.objects.annotate(
        fiche_count=Count('fiches', filter=Q(fiches__is_deleted=False)),
        comment_count=Count('comments')
    )
    
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(discord_username__icontains=search) |
            Q(email__icontains=search) |
            Q(discord_id__icontains=search)
        )
    
    if role_filter:
        users = users.filter(roles__id=role_filter)
    
    users = users.order_by('-date_joined')
    
    all_roles = Role.objects.all()
    all_servers = Server.objects.all().order_by('name')
    
    context = {
        'users': users,
        'all_roles': all_roles,
        'search': search,
        'role_filter': role_filter,
        'all_servers': all_servers,
    }
    
    return render(request, 'core/manage_users.html', context)


@owner_required
def manage_servers(request):
    """Gestion des serveurs (owner uniquement)"""
    servers = Server.objects.annotate(
        fiche_count=Count('fiches', filter=Q(fiches__is_deleted=False)),
        user_count=Count('fiches__author', distinct=True, filter=Q(fiches__is_deleted=False)),
        admin_count=Count('admins')
    ).order_by('-fiche_count')
    
    all_servers_sidebar = Server.objects.all().order_by('name')
    
    context = {
        'servers': servers,
        'all_servers': all_servers_sidebar,
    }
    
    return render(request, 'core/manage_servers.html', context)


@owner_required
def user_detail(request, user_id):
    """Détails d'un utilisateur avec toutes ses statistiques"""
    target_user = get_object_or_404(User, pk=user_id)
    
    # Statistiques
    user_fiches = Fiche.objects.filter(author=target_user, is_deleted=False)
    user_comments = Comment.objects.filter(author=target_user)
    
    stats = {
        'total_fiches': user_fiches.count(),
        'total_comments': user_comments.count(),
        'servers_count': Server.objects.filter(fiches__author=target_user).distinct().count(),
        'admin_servers_count': target_user.admin_servers.count(),
    }
    
    # Fiches de l'utilisateur
    fiches = user_fiches.select_related('server').order_by('-created_at')
    
    # Serveurs où l'utilisateur est actif
    active_servers = Server.objects.filter(
        fiches__author=target_user
    ).annotate(
        fiche_count=Count('fiches', filter=Q(fiches__author=target_user, fiches__is_deleted=False))
    ).order_by('-fiche_count')
    
    # Rôles
    user_roles = target_user.roles.all()
    all_roles = Role.objects.all()
    
    # Logs d'actions de cet utilisateur
    user_logs = AuditLog.objects.filter(user=target_user).order_by('-created_at')[:20]
    
    all_servers = Server.objects.all().order_by('name')
    
    context = {
        'target_user': target_user,
        'stats': stats,
        'fiches': fiches,
        'active_servers': active_servers,
        'user_roles': user_roles,
        'all_roles': all_roles,
        'user_logs': user_logs,
        'all_servers': all_servers,
    }
    
    return render(request, 'core/user_detail.html', context)


@owner_required
def user_edit_roles(request, user_id):
    """Modifier les rôles d'un utilisateur (owner uniquement)"""
    target_user = get_object_or_404(User, pk=user_id)
    all_roles = Role.objects.all()
    
    if request.method == 'POST':
        selected_roles = request.POST.getlist('roles')
        target_user.roles.clear()
        
        for role_id in selected_roles:
            role = Role.objects.get(pk=role_id)
            target_user.roles.add(role)
        
        # Log l'action
        AuditLog.objects.create(
            user=request.user,
            action='role_add',
            new_value=f"Rôles modifiés pour {target_user.username}",
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        messages.success(request, f"Rôles de {target_user.username} mis à jour !")
        return redirect('user_detail', user_id=user_id)
    
    all_servers = Server.objects.all().order_by('name')
    
    context = {
        'target_user': target_user,
        'all_roles': all_roles,
        'all_servers': all_servers,
    }
    
    return render(request, 'core/user_edit_roles.html', context)


@owner_required
def server_detail(request, server_id):
    """Détails d'un serveur"""
    server = get_object_or_404(Server, pk=server_id)
    
    # Statistiques du serveur
    fiches = Fiche.objects.filter(server=server, is_deleted=False).select_related('author')
    
    stats = {
        'total_fiches': fiches.count(),
        'total_users': User.objects.filter(fiches__server=server).distinct().count(),
        'total_comments': Comment.objects.filter(fiche__server=server).count(),
        'total_admins': server.admins.count(),
    }
    
    # Top créateurs sur ce serveur
    top_creators = User.objects.filter(
        fiches__server=server,
        fiches__is_deleted=False
    ).annotate(
        fiche_count=Count('fiches')
    ).order_by('-fiche_count')[:10]
    
    # Fiches récentes
    recent_fiches = fiches.order_by('-created_at')[:10]
    
    # Admins du serveur
    server_admins = server.admins.all()
    
    # Tous les utilisateurs (pour ajouter des admins)
    all_users = User.objects.all().order_by('username')
    
    all_servers = Server.objects.all().order_by('name')
    
    context = {
        'server': server,
        'stats': stats,
        'top_creators': top_creators,
        'recent_fiches': recent_fiches,
        'server_admins': server_admins,
        'all_users': all_users,
        'all_servers': all_servers,
    }
    
    return render(request, 'core/server_detail.html', context)


@owner_required
def server_add_admin(request, server_id):
    """Ajouter un admin à un serveur"""
    server = get_object_or_404(Server, pk=server_id)
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        
        server.admins.add(user)
        
        # Log
        AuditLog.objects.create(
            user=request.user,
            action='role_add',
            server_id=server.id,
            new_value=f"{user.username} ajouté comme admin du serveur {server.name}",
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        messages.success(request, f"{user.username} ajouté comme administrateur de {server.name}")
        return redirect('server_detail', server_id=server.id)
    
    return redirect('server_detail', server_id=server.id)


@owner_required
def server_remove_admin(request, server_id, user_id):
    """Retirer un admin d'un serveur"""
    server = get_object_or_404(Server, pk=server_id)
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        server.admins.remove(user)
        
        # Log
        AuditLog.objects.create(
            user=request.user,
            action='role_remove',
            server_id=server.id,
            new_value=f"{user.username} retiré comme admin du serveur {server.name}",
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        messages.success(request, f"{user.username} retiré des administrateurs de {server.name}")
    
    return redirect('server_detail', server_id=server.id)