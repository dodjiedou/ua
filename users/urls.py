from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static               
from django.contrib.auth import views as auth_view
from users.forms import LoginForm

urlpatterns=[
    path('', views.verif, name='verif'),
#----------------------Urls ADMIN CAERT-----------------------------

    path('user_profile/' , views.user_profile, name='user_profile'),
    path('admin_home/' , views.admin_home, name='admin_home'),
    path('add_fp/' ,views.FocalPointCreateView.as_view(), name='add_fp'),
    path('edit_fp/<int:pk>/' ,views.FocalPointEditView.as_view(), name='edit_fp'),
    path('all_fp/' ,views.all_fp, name='all_fp'),
    path('deletefp/<int:pk>/', views.deletefp, name='deletefp'),
    path('admin_caert/' ,views.admin_caert, name='admin_caert'),
    path('delete_admin_caert/<int:pk>/' ,views.delete_admin_caert, name='delete_admin_caert'),
    path('edit_admin_caert/<int:pk>/' ,views.EditAdminCAERT.as_view(), name='edit_admin_caert'),
    path('enable_user/<int:pk>/' ,views.enable_user, name='enable_user'),
    path('disable_user/<int:pk>/' ,views.disable_user, name='disable_user'),
    path('all_manager/', views.all_manager, name='all_manager'),
    path('all_manager_fp/<int:fp>/', views.all_manager, name='all_manager_fp'),
    path('add_manager/' ,views.AddManager.as_view(), name='add_manager'),
    path('edit_manager/<int:pk>/' ,views.EditManager.as_view(), name='edit_manager'),
    path('delete_manager/<int:pk>/', views.delete_manager, name='delete_manager'),
    path('add_admin/' ,views.AddAdminCAERT.as_view(), name='add_admin'),

    path('all_categorie/', views.all_categorie, name='all_categorie'),
    path('add_categorie/' ,views.AddCategorie.as_view(), name='add_categorie'),
    path('edit_categorie/<int:pk>/' ,views.EditCategorie.as_view(), name='edit_categorie'),
    
    path('add_member/', views.AddMember.as_view(), name='add_member'),
    path('edit_member/<int:pk>/' ,views.EditMember.as_view(), name='edit_member'),
    path('delete_member/<int:pk>/', views.delete_member, name='delete_member'),
    path('all_member/', views.all_member, name='all_member'),
    path('all_member/<int:fp>/', views.all_member, name='all_member'),

    path('all_infos/' ,views.all_infos, name='all_infos'),
    path('all_infos/<int:fp>/' ,views.all_infos, name='all_infos'),
    path('add_info/' ,views.AddInformation.as_view(), name='add_info'),
    path('edit_info/<int:pk>/' ,views.EditInformation.as_view(), name='edit_info'),

    path('publier_information/<int:pk>/' ,views.publier_information, name='publier_information'),
    
    path('all_alerts/',views.all_alerts, name='all_alerts'),
    path('all_alerts/<int:fp>/' ,views.all_alerts, name='all_alerts'),


#----------------------Urls ANALYST-----------------------------
    path('analyst_home/' , views.analyst_home, name='analyst_home'),
     path('analyst_all_fp/' ,views.analyst_all_fp, name='analyst_all_fp'),
    path('all_admin_caert/' ,views.all_admin_caert, name='all_admin_caert'),
    path('analyst_all_manager/', views.analyst_all_manager, name='analyst_all_manager'),
    path('analyst_all_manager_fp/<int:fp>/', views.analyst_all_manager, name='analyst_all_manager_fp'),

    path('analyst_all_member/', views.analyst_all_member, name='analyst_all_member'),
    path('analyst_all_member/<int:fp>/', views.analyst_all_member, name='analyst_all_member'),

    path('analyst_all_infos/' ,views.analyst_all_infos, name='analyst_all_infos'),
    path('analyst_all_infos/<int:fp>/' ,views.analyst_all_infos, name='analyst_all_infos'),
    
    path('analyst_all_alerts/',views.analyst_all_alerts, name='analyst_all_alerts'),
    path('analyst_all_alerts/<int:fp>/' ,views.analyst_all_alerts, name='analyst_all_alerts'),

#----------------------Urls STAFF-----------------------------

    path('staff_home/' , views.staff_home, name='staff_home'),
    path('staff_forum/' , views.staff_forum, name='staff_forum'),
    path('staff_all_member/', views.staff_all_member, name='staff_all_member'),
    path('staff_all_infos/' ,views.staff_all_infos, name='staff_all_infos'),
    path('staff_all_infos/<int:cat>/' ,views.staff_all_infos, name='staff_all_infos'),
    path('relayer_information/<int:pk>/' ,views.relayer_information, name='relayer_information'),
    path('relayer_alert/<int:pk>/' ,views.RelayerAlerte.as_view(), name='relayer_alert'),
    path('staff_all_alerts/',views.staff_all_alerts, name='staff_all_alerts'),
    path('staff_all_alerts/<int:fp>/' ,views.staff_all_alerts, name='staff_all_alerts'),

    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('redirectionner/' , views.redirectionner, name='redirectionner'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html', authentication_form=LoginForm,), name='login'),

     
    #path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
