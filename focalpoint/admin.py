from django.contrib import admin
from . models import *
from . forms import *

# Register your models here.


class FocalPointAdmin(admin.ModelAdmin):
    form = FocalPointCreateForm
    add_form = FocalPointCreateForm
    
    list_display = ['name', 'email', 'country']
    list_filter = ['name', 'email', 'country']
    fieldsets = (
    (None, {'fields': ('name', 'email', 'country', 'access_code', 'active')}),
    )
    # add_fieldsets n'est pas un attribut ModelAdmin standard. UtilisateurAdmin
    # remplace get_fieldsets pour utiliser cet attribut lors de la création d'un utilisateur.
    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('name', 'email', 'country', 'access_code', 'active',)}
    ),
    )
    search_fields = ['email', 'name', 'country']
    ordering = ['email', 'name', 'country']
    filter_horizontal = ()
admin.site.register(FocalPoint, FocalPointAdmin)

admin.site.register(Information)
admin.site.register(Media)
admin.site.register(Categorie)
admin.site.register(Publication)
