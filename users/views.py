import json
from urllib import response
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, authenticate
from django.views import View
from django.contrib import messages
import requests
from rest_framework.response import Response
from onesignal_sdk.client import Client
import onesignal_sdk
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

from focalpoint.forms import (
    AddInfoForm, CreateInformation,AddCategorieForm,
    FocalPointEditForm, FocalPointCreateForm,
    PublicateForm, EditAlertForm)
from focalpoint.models import Categorie, FocalPoint,Forum, Information, Publication, PublicationFocalPoint
from users.forms import AdminCreationForm,AdminEditionForm, LoginForm, ManagerRegistrationForm,AddMemberForm
from users.models import Alerte, Member, User
from member.models import Message


#-----------------------------API FUNCTIONS-----------------------
'''ceci permet de faire des notifications aux utilisateurs 
sur l application mobile'''
def mobile_notification(sender, focalpoint_id, **kwargs):

    if sender._name_ == "PublicationFocalPoint":

        members=Member.objects.filter(focal_point_id=focalpoint_id)
        for member in members:
            external_id = Token.objects.get(id=member.user_ptr_id).key

        header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {settings.ONESIGNAL_AUTH_TOKEN}"
        }

        payload = {
            "app_id": settings.ONESIGNAL_APP_ID,
            "include_external_user_ids": [f"{external_id}"],
            "headings": {"en": "Transfert réussi"},
            "contents": {
                "en": f"Publication d'une nouvelle information"},
            "priority": 10,
            #"big_picture": "https://media.onesignal.com/automated_push_templates/feature_announcement_template.png"
        }

        req = requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers=header, data=json.dumps(payload)
        )
    return None



#-------------------------------ADMIN CAERT--------------------------
@login_required
def user_profile(request):
    user = User.objects.get(id=request.user.id)
    if user.is_admin:
        return render(request, 'administrator/profile.html', locals())
    elif user.is_staff:
        return render(request, 'staff/profile.html', locals())
    else:
        return render(request, 'analyst/profile.html', locals())

@login_required
def admin_home(request):
    count_fp=FocalPoint.objects.count()
    prctg=count_fp/55
    prctg=round(prctg, 2)
    count_users=User.objects.count()
    prctg_users=count_users/1453950847
    prctg_users=round(prctg_users, 2)
    return render(request, 'administrator/dashboard.html', locals())


@method_decorator(login_required, name='dispatch')
class FocalPointCreateView(View):
    def get(self, request):
        form=FocalPointCreateForm
        return render(request, 'administrator/add_fp.html', locals())
    
    def post(self, request):
        form=FocalPointCreateForm(request.POST)
        if form.is_valid():
            new_focalpoint=form.save()
            new_forum=Forum(
             name=f"Point focal {form.cleaned_data['name']}",
             focal_point=new_focalpoint
            )
            new_forum.save()
            messages.success(request, "Point Focal enregistré!")
            return redirect('all_fp')
        else:
            messages.warning(request, "Données incorrectes")
            return render(request, 'administrator/add_fp.html', locals())


@method_decorator(login_required, name='dispatch')
class FocalPointEditView(View):
    def get(self, request,pk):
        focalpoint=FocalPoint.objects.get(pk=pk)
        form=FocalPointEditForm(instance=focalpoint)
        return render(request, 'administrator/edit_fp.html', locals())
    
    def post(self, request,pk):
        focalpoint=FocalPoint.objects.get(pk=pk)
        form=FocalPointEditForm(request.POST,instance=focalpoint)
        if form.is_valid():
            form.save()
            messages.success(request, "Point Focal enregistré!")
            return redirect('all_fp')
        else:
            messages.warning(request, "Données incorrectes")
            return render(request, 'administrator/edit_fp.html', locals())
    

@login_required
def all_fp(request):
    all_fp = FocalPoint.objects.filter(active=True)
    all_fp = sorted(all_fp, key=lambda x: x.id, reverse=True)
    user=request.user
    print(all_fp)
    return render(request, 'administrator/all_fp.html', {'all_fp': all_fp, 'user': user})


@login_required
def deletefp(request, pk):
    fp=FocalPoint.objects.get(pk=pk)
    fp.active= not fp.active
    fp.save()
    return redirect('all_fp')


@login_required
def admin_caert(request):
    admins=User.objects.filter(is_admin=True)
    return render(request, 'administrator/admin_caert.html', locals())


@method_decorator(login_required, name='dispatch')
class AddAdminCAERT(View):
    def get(self, request):
        form = AdminCreationForm()
        return render(request, 'administrator/add_admin.html', {'form': form})
    
    def post(self, request):
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password('administateur')
            user.is_admin = True
            user.is_active = True
            user.staff = False
            user.save()
            messages.success(request, "Administrteur crée!")
            return redirect('admin_caert')
        else:
            messages.warning(request, "Données incorrectes")
            return render(request, 'administrator/add_admin.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditAdminCAERT(View):
    def get(self, request,pk):
        admin=User.objects.get(pk=pk)
        form = AdminEditionForm(instance=admin)
        return render(request, 'administrat or/edit_admin.html', {'form': form})
    
    def post(self, request,pk):
        admin=User.objects.get(pk=pk)
        form = AdminCreationForm(request.POST,instance=admin)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request, "Administrteur crée!")
            return redirect('admin_caert')
        else:
            messages.warning(request, "Données incorrectes")
            return render(request, 'administrator/add_admin.html', {'form': form})


@login_required
def delete_admin_caert(request,pk):
    user=User.objects.get(pk=pk)
    user.is_admin= False
    user.is_staff= False 
    user.is_active= False
    user.is_analyst= False
    user.save()
    return redirect('admin_caert')


@method_decorator(login_required, name='dispatch')
class AddManager(View):

    def get(self, request):
        form = ManagerRegistrationForm()
        return render(request, 'administrator/add_manager.html', {'form': form})
    
    def post(self, request):
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password('manager_001')
            user.is_staff=True
            user.save()
            messages.success(request, "Manager crée!")
            return redirect('all_manager')
        else:
            print('False')
            messages.warning(request, "Données incorrectes")
            return render(request, 'administrator/add_manager.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditManager(View):

    def get(self, request,pk):
        manager=Member.objects.get(user_ptr_id=pk)
        form = ManagerRegistrationForm(instance=manager)
        return render(request, 'administrator/edit_manager.html', {'form': form})
    
    def post(self, request,pk):
        manager=Member.objects.get(user_ptr_id=pk)
        form = ManagerRegistrationForm(request.POST,instance=manager)
        if form.is_valid():
            user = form.save()
            user.save()
            member=Member.objects.get(user_ptr_id=pk)
            fp_id=member.focal_point_id
            messages.success(request, "Manager crée!")
            return redirect(reverse('all_manager_fp', args=[fp_id]))
        else:
            print('False')
            messages.warning(request, "Données incorrectes")
            return render(request, 'administrator/edit_manager.html', {'form': form})


@login_required
def all_manager(request, fp=None):
    fps = FocalPoint.objects.all()

    if fp is None:
        init_fp = FocalPoint.objects.first()
    else:
        init_fp = FocalPoint.objects.get(pk=fp)

    managers = Member.objects.filter(is_staff=True, focal_point=init_fp)

    return render(request, 'administrator/all_manager.html', {'fps': fps, 'init_fp': init_fp, 'managers': managers})


@login_required
def delete_manager(request,pk):
    member=Member.objects.get(user_ptr_id=pk)
    fp_id=member.focal_point_id
    user=User.objects.get(pk=pk)
    user.is_staff= False 
    user.save()
    return redirect(reverse('all_manager_fp', args=[fp_id]))
    

@method_decorator(login_required, name='dispatch')
class AddMember(View):

    def get(self, request):
        form = AddMemberForm()
        return render(request, 'staff/add_member.html', {'form': form})
    
    def post(self, request):
        form = AddMemberForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password('member_001')
            user.is_active=True
            user.save()
            messages.success(request, "Membre crée!")
            return redirect('staff_all_member')
        else:
            print('False')
            messages.warning(request, "Données incorrectes")
            return render(request, 'staff/add_member.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditMember(View):

    def get(self, request,pk):
        member=Member.objects.get(pk=pk)
        form = AddMemberForm(instance=member)
        return render(request, 'staff/edit_member.html', {'form': form})
    
    def post(self, request,pk):
        member=Member.objects.get(pk=pk)
        form = AddMemberForm(request.POST,instance=member)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request, "Membre modifié!")
            return redirect('staff_all_member')
        else:
            print('False')
            messages.warning(request, "Données incorrectes")
            return render(request, 'staff/edit_member.html', {'form': form})


@login_required
def delete_member(request,pk):
    member=Member.objects.get(user_ptr_id=pk)
    fp_id=member.focal_point_id
    user=User.objects.get(pk=pk)
    user.is_active= False 
    user.save()
    return redirect('staff_all_member')

    
@login_required
def all_member(request, fp=None):
    fps = FocalPoint.objects.all()

    if fp is None:
        init_fp = FocalPoint.objects.first()
    else:
        init_fp = FocalPoint.objects.get(pk=fp)

    members = Member.objects.filter(focal_point=init_fp)

    return render(request, 'administrator/all_member.html', {'fps': fps, 'init_fp': init_fp, 'members': members})


@login_required
def all_infos(request, fp=None):
    form=PublicateForm()
    fps = Categorie.objects.all()
    if fp is None:
        init_fp = Categorie.objects.first()
    else:
        init_fp = Categorie.objects.get(pk=fp)

    all_infos = Information.objects.filter(categorie=init_fp)
    all_infos = sorted(all_infos, key=lambda x: x.id, reverse=True)
    return render(request, 'administrator/all_infos.html', { 'infos': all_infos, 'fps': fps, 'init_fp': init_fp, 'form': form})


@login_required
def delete_manager(request,pk):
    member=Member.objects.get(user_ptr_id=pk)
    fp_id=member.focal_point_id
    user=User.objects.get(pk=pk)
    user.is_staff= False 
    user.save()
    return redirect(reverse('all_manager_fp', args=[fp_id]))
    

@method_decorator(login_required, name='dispatch')
class AddCategorie(View):

    def get(self, request):
        form = AddCategorieForm()
        return render(request, 'administrator/add_categorie.html', {'form': form})
    
    def post(self, request):
        form = AddCategorieForm(request.POST)
        if form.is_valid():
            categorie = form.save()
            categorie.save()
            messages.success(request, "Categorie crée!")
            return redirect('all_categorie')
        else:
            print('False')
            messages.warning(request, "Données incorrectes")
            return render(request, 'administrator/add_categorie.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditCategorie(View):

    def get(self, request,pk):
        categorie=Categorie.objects.get(pk=pk)
        form = AddCategorieForm(instance=categorie)
        return render(request, 'administrator/edit_categorie.html', {'form': form})
    
    def post(self, request,pk):
        categorie=Categorie.objects.get(pk=pk)
        form = AddCategorieForm(request.POST,instance=categorie)
        if form.is_valid():
            categorie = form.save()
            categorie.save()
            messages.success(request, "Categorie modifiée!")
            return redirect('all_categorie')
        else:
            messages.warning(request, "Données incorrectes")
            return render(request, 'administrator/edit_categorie.html', {'form': form})

@login_required
def all_categorie(request):
    categories=Categorie.objects.all()
    return render(request, 'administrator/all_categorie.html', locals())



@method_decorator(login_required, name='dispatch')
class AddInformation(View):
    def get(self, request):
        form = AddInfoForm()
        return render(request, 'administrator/add_info.html', {'form': form,})

    def post(self, request):
        form = AddInfoForm(request.POST)
        if form.is_valid():
            # Créez une nouvelle instance de votre modèle (par exemple, Member)
            new_instance = form.save(commit=False)  # N'enregistrez pas encore l'objet dans la base de données
            new_instance.save()
            messages.success(request, "Nouvelle information créée avec succès!")  # Message de succès adapté
            
            return redirect('all_infos')
        else:            
            messages.warning(request, "Données incorrectes")
            return render(request, 'administrator/add_info.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditInformation(View):
    def get(self, request,pk):
        information=Information.objects.get(pk=pk)
        form = AddInfoForm(instance=information)
        return render(request, 'administrator/edit_info.html', {'form': form,})

    def post(self, request,pk):
        information=Information.objects.get(pk=pk)
        form = AddInfoForm(request.POST,instance=information)
        if form.is_valid():
            # Créez une nouvelle instance de votre modèle (par exemple, Member)
            new_instance = form.save(commit=False)  # N'enregistrez pas encore l'objet dans la base de données
            new_instance.save()
            messages.success(request, "Nouvelle information créée avec succès!")  # Message de succès adapté
            
            return redirect('all_infos')
        else:            
            messages.warning(request, "Données incorrectes")
            return render(request, 'administrator/edit_info.html', {'form': form})


@login_required
def publier_information(request, pk):
        form = PublicateForm(request.POST)
        if form.is_valid():
            new_publication = form.save(commit=False)  
            info = Information.objects.get(pk=pk)
            publications=Publication.objects.filter(information_id=pk)
            focalpoint=[]
            for publication in publications:
                fps=publication.focalpoint.all()
                for fp in fps:
                    if fp not in focalpoint:
                        focalpoint.append(fp)
                    
            focal_points=form.cleaned_data['focalpoint']
            
            info.is_published=True
            info.published_at=timezone.now()
            info.save()
            new_publication.information = info
            new_publication.save()

            for focal_point in focal_points:
                if focal_point not in focalpoint:
                    new_publication.focalpoint.add(focal_point)
                    mobile_notification(focal_point.id)
                    #code de notification

            messages.success(request, "Nouvelle instance créée avec succès!")  # Message de succès adapté
            
            return redirect('all_infos')
        else:
            info = Information.objects.get(pk=pk)
            fp = FocalPoint.objects.all()
            
            # Créer un formulaire en utilisant les données du point focal existant
            form = PublicateForm(initial={'information': info})  # Associez le formulaire à l'objet Information
            
            messages.warning(request, "Données incorrectes")
            return render(request, 'administrator/public.html', {'form': form, 'info': info})


@login_required
def all_alerts(request, fp=None):
    fps = FocalPoint.objects.all()
    if fp is None:
        init_fp = FocalPoint.objects.first()
    else:
        init_fp = FocalPoint.objects.get(pk=fp)

    all_alerte=Alerte.objects.all()
    alerts=[]
    if fp is None:
        alerts=Alerte.objects.all()
    else:
        for alerte in all_alerte:
            if alerte.membre.focal_point.id == fp:
                alerts.append(alerte)
         
    alerts = sorted(alerts, key=lambda x: x.id, reverse=True)

    return render(request, 'administrator/all_alerts.html',locals())


#-------------------------------MANAGER---------------------
@login_required
def staff_home(request):
    member=Member.objects.get(user_ptr_id=request.user.id)
    focal_point=member.focal_point
    count_fp=FocalPoint.objects.count()
    prctg=count_fp/55
    prctg=round(prctg, 2)
    count_users=User.objects.count()
    prctg_users=count_users/1453950847
    prctg_users=round(prctg_users, 2)
    return render(request, 'staff/dashboard.html', locals())

@login_required
def staff_forum(request):
    return render(request, 'staff/forum.html')


@login_required
def staff_all_member(request):
    member=Member.objects.get(user_ptr_id=request.user.id)
    fp = FocalPoint.objects.get(id=member.focal_point_id)
    members=Member.objects.filter(focal_point_id=fp.id,is_active=True)
    return render(request, 'staff/all_member.html', {'fp': fp, 'members': members})


@login_required
def staff_all_infos(request, cat=None):
    form=PublicateForm()
    categories = Categorie.objects.all()
    if cat is None:
        init_cat = Categorie.objects.first()
    else:
        init_cat = Categorie.objects.get(pk=cat)
    
    member=Member.objects.get(user_ptr_id=request.user.id)
    focal_point=member.focal_point
    publications=focal_point.publication_set.all()

    all_infos=[]
    for publication in publications:
        all_infos.append(publication.information)

    #all_infos = Information.objects.filter(categorie=init_cat)
    all_infos = sorted(all_infos, key=lambda x: x.id, reverse=True)
    return render(request, 'staff/staff_all_infos.html', { 'infos': all_infos, 'categories': categories, 'init_cat': init_cat, 'form': form})


@login_required
def relayer_information(request, pk): 
    member=Member.objects.get(user_ptr_id=request.user.id) 
    info = Information.objects.get(pk=pk)
    publications=Publication.objects.filter(information_id=pk)
    for publication in publications:
        publication_focalpoints=PublicationFocalPoint.objects.filter(focalpoint_id=member.focal_point.id)
        for publication_focalpoint in publication_focalpoints: 
            if publication_focalpoint.publication_id==publication.id:
                publication_focalpoint.is_active=True
                publication_focalpoint.save()

    return redirect('staff_all_infos')


@method_decorator(login_required, name='dispatch')
class RelayerAlerte(View):
    def get(self, request,pk):
        alert=Alerte.objects.get(pk=pk)
        form = EditAlertForm(instance=alert)
        return render(request, 'staff/edit_alert.html', {'form': form,})

    def post(self, request,pk):
        alert=Alerte.objects.get(pk=pk)
        form = EditAlertForm(request.POST,instance=alert)
        if form.is_valid():
            new_alerte = form.save(commit=False)
            print(new_alerte)
            new_alerte.save() 

            new_information=Information(
            title=form.cleaned_data['title'],
            description=form.cleaned_data['contenu'],
            published_at=timezone.now(),
            is_published=True,
            categorie_id=2

            )

            new_information.save()

            new_publication=Publication(
             information_id=new_information.id,
             published_at=timezone.now()
            )

            new_publication.save()

            member=Member.objects.get(user_ptr_id=request.user.id)

            new_publication.focalpoint.add(member.focal_point)
            new_publication.save()
            publication_focalpoint=PublicationFocalPoint.objects.get(publication_id=new_publication.id)
            publication_focalpoint.is_active=True
            publication_focalpoint.save()

            messages.success(request, "Alerte relayée avec succès!") 
            return redirect('staff_all_alerts')
        else:
             messages.success(request, "Alerte non relayée!")
             return redirect('staff_all_alerts')

@login_required
def staff_all_alerts(request):
    member=Member.objects.get(user_ptr_id=request.user.id)
    focalpoint = member.focal_point
    all_alerte=Alerte.objects.all()
    alertes=[]
    for alerte in all_alerte:
        if alerte.membre.focal_point == focalpoint:
            alertes.append(alerte)
    
    alertes = sorted(alertes, key=lambda x: x.id, reverse=True)
           
    return render(request, 'staff/all_alerts.html', locals())


#-----------------------------ANALYST------------------------------------
@login_required
def analyst_home(request):
    count_fp=FocalPoint.objects.count()
    prctg=count_fp/55
    prctg=round(prctg, 2)
    count_users=User.objects.count()
    prctg_users=count_users/1453950847
    prctg_users=round(prctg_users, 2)
    return render(request, 'analyst/dashboard.html', locals())


@login_required
def analyst_all_fp(request):
    all_fp = FocalPoint.objects.filter(active=True)
    all_fp = sorted(all_fp, key=lambda x: x.id, reverse=True)
    user=request.user
    print(all_fp)
    return render(request, 'analyst/all_fp.html', {'all_fp': all_fp, 'user': user})


@login_required
def analyst_all_manager(request, fp=None):
    fps = FocalPoint.objects.all()

    if fp is None:
        init_fp = FocalPoint.objects.first()
    else:
        init_fp = FocalPoint.objects.get(pk=fp)

    managers = Member.objects.filter(is_staff=True, focal_point=init_fp)

    return render(request, 'analyst/all_manager.html', {'fps': fps, 'init_fp': init_fp, 'managers': managers})


@login_required
def analyst_all_member(request, fp=None):
    fps = FocalPoint.objects.all()

    if fp is None:
        init_fp = FocalPoint.objects.first()
    else:
        init_fp = FocalPoint.objects.get(pk=fp)

    members = Member.objects.filter(focal_point=init_fp)

    return render(request, 'analyst/all_member.html', {'fps': fps, 'init_fp': init_fp, 'members': members})


@login_required
def all_admin_caert(request):
    admins=User.objects.filter(is_admin=True)
    return render(request, 'analyst/admin_caert.html', locals())


@login_required
def analyst_all_infos(request, fp=None):
    form=PublicateForm()
    fps = Categorie.objects.all()
    if fp is None:
        init_fp = Categorie.objects.first()
    else:
        init_fp = Categorie.objects.get(pk=fp)

    all_infos = Information.objects.filter(categorie=init_fp)
    all_infos = sorted(all_infos, key=lambda x: x.id, reverse=True)
    return render(request, 'analyst/all_infos.html', { 'infos': all_infos, 'fps': fps, 'init_fp': init_fp, 'form': form})


@login_required
def analyst_all_alerts(request, fp=None):
    fps = FocalPoint.objects.all()
    if fp is None:
        init_fp = FocalPoint.objects.first()
    else:
        init_fp = FocalPoint.objects.get(pk=fp)

    all_alerte=Alerte.objects.all()
    alerts=[]
    if fp is None:
        alerts=Alerte.objects.all()
    else:
        for alerte in all_alerte:
            if alerte.membre.focal_point.id == fp:
                alerts.append(alerte)
         
    alerts = sorted(alerts, key=lambda x: x.id, reverse=True)

    return render(request, 'analyst/all_alerts.html',locals())


#-----------------------------------OTHERS FUNCTIONS-------------------------
def verif(request):
    if request.user.is_authenticated:
      return  redirect('redirectionner')
    else:
      return  redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            authenticate(request, email=form.username, password=form.password)
            return redirect('liste_transferts') 
        else:
            messages.error(request, 'Identifiants invalides. Veuillez réessayer.')

    else:
        form = LoginForm()  # Vous n'avez pas besoin de passer request ici
    
    return render(request, 'login.html', {'form': form})


@login_required
def redirectionner(request):
    if request.user.is_admin and request.user.is_active :
        return redirect('admin_home')
    elif request.user.is_staff and request.user.is_active:
        return redirect('staff_home')
    elif request.user.is_analyst and request.user.is_active:
       return redirect('analyst_home')
    else:
       return redirect('error_page')
    

@login_required
def deconnexion(request):
    logout(request)
    return redirect('login')


def enable_user(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = True
    user.save()
    return redirect('admin_caert')

def disable_user(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = False
    user.save()
    return redirect('admin_caert')
