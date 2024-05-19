from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . forms import *
from .models import *

# Register your models here.

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # Les formulaires pour ajouter et modifier des instances d'utilisateur
    add_form = UserAdminCreationForm

    # Les champs à utiliser pour afficher le modèle User.
    # Celles-ci remplacent les définitions de la baseUserAdmin
    # qui font référence à des champs spécifiques sur auth.User.
    list_display = ['email', 'nom', 'prenom', 'departement', 'is_admin']
    list_filter = ['email', 'nom', 'prenom', 'departement', 'is_admin']
    fieldsets = (
    (None, {'fields': ('email', 'password')}),
    ('Personal info', {'fields': ('nom', 'prenom', 'departement',)}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin')}),
    )
    # add_fieldsets n'est pas un attribut ModelAdmin standard. UtilisateurAdmin
    # remplace get_fieldsets pour utiliser cet attribut lors de la création d'un utilisateur.
    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('email', 'nom', 'prenom', 'departement', 'password', 'password_2', 'is_staff', 'is_analyst', 'is_admin', 'is_active')}
    ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

admin.site.register(Member)
admin.site.register(Alerte)
admin.site.register(Commentaire)
admin.site.register(Like)