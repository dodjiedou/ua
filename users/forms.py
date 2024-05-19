from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

from focalpoint.models import FocalPoint
from users.models import Member

User = get_user_model()

class RegisterForm(forms.ModelForm):
    """
    The default

    """
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirmation du mot de passe', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'nom', 'prenom']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("l'e-mail est pris")
        return email

    def clean(self):
        '''
        Vérifiez que les deux mots de passe correspondent.
        '''
        cleaned_data = super().clean()
        password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
        password_2 = forms.CharField(label='Confirmation du mot de passe', widget=forms.PasswordInput)
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data


class UserAdminCreationForm(forms.ModelForm):
    """
    Un formulaire pour créer de nouveaux utilisateurs. Comprend tout le nécessaire
    champs, plus un mot de passe répété.
    """
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirmation du mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_2 = cleaned_data.get('password_2')
        if password and password_2 and password != password_2:
            self.add_error("password_2", "Les mots de passe doivent correspondre!")
        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class UserAdminChangeForm(forms.ModelForm):
    """Un formulaire pour mettre à jour les utilisateurs. Inclut tous les champs sur
    l'utilisateur, mais remplace le champ du mot de passe par celui de l'administrateur
    champ d'affichage du hachage du mot de passe.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'nom',  'prenom', 'departement', 'is_active', 'is_admin', 'is_analyst',]

    def clean_password(self):
        return self.initial["password"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'autofocus' : 'True', 'class' : 'form-control'}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class' : 'form-control'}))


class AdminCreationForm(forms.ModelForm):
    email = forms.EmailField(label='Adresse email', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    nom=forms.CharField(label='Nom', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    prenom=forms.CharField(label='Prénoms', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    departement=forms.CharField(label='Département', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['email', 'nom', 'prenom', 'departement']

class AdminEditionForm(forms.ModelForm):
    email = forms.EmailField(label='Adresse email', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    nom=forms.CharField(label='Nom', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    prenom=forms.CharField(label='Prénoms', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    departement=forms.CharField(label='Département', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['email', 'nom', 'prenom', 'departement']

    def save(self, commit=True):
        fp = super().save(commit=False)        
        if commit:
            fp.save(update_fields=['email', 'nom', 'prenom', 'departement'])
        return fp


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="Mot de passe actuel",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    renew_password = forms.CharField(
        label="Entrer le mot de passe à nouveau",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class ManagerRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Adresse email', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    nom = forms.CharField(label='Nom', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    prenom = forms.CharField(label='Prénoms', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    departement = forms.CharField(label='Département', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    city = forms.CharField(label='Ville', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    country = CountryField(null=True, blank=True).formfield(
        label='Pays',
        widget=CountrySelectWidget(attrs={'class': 'form-control'}),
    )
    focal_point = forms.ModelChoiceField(
        queryset=FocalPoint.objects.all(),
        label='Point focal',
        empty_label='Sélectionnez un point focal',  # Supprimez l'option vide
        widget=forms.Select(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',  # Format AAAA-MM-JJ
            attrs={'placeholder': 'AAAA-MM-JJ', 'class': 'form-control'},
        ),
        help_text='Format: AAAA-MM-JJ',
    )    
    class Meta:
        model = Member
        fields = ['email', 'nom', 'prenom', 'departement', 'city', 'country', 'focal_point', 'date_of_birth']

# Formulaire pour le modèle Member
class AddMemberForm(forms.ModelForm):
    email = forms.EmailField(label='Adresse email', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    nom = forms.CharField(label='Nom', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    prenom = forms.CharField(label='Prénoms', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    departement = forms.CharField(label='Département', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    city = forms.CharField(label='Ville', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    phone = forms.CharField(label='Téléphone', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    country = CountryField(null=True, blank=True).formfield(
        label='Pays',
        widget=CountrySelectWidget(attrs={'class': 'form-control'}),
    )
    focal_point = forms.ModelChoiceField(
        queryset=FocalPoint.objects.all(),
        label='Point focal',
        empty_label='Sélectionnez un point focal',  # Supprimez l'option vide
        widget=forms.Select(attrs={'autofocus': True, 'class': 'form-control'}),
    )
    date_of_birth = forms.DateField(
        label='Date de naissance',
        widget=forms.DateInput(
            format='%Y-%m-%d',  # Format AAAA-MM-JJ
            attrs={'placeholder': 'JJ-MM-AAAA', 'class': 'form-control'},
        ),
        help_text='Format: JJ-MM-AAAA',
    )    
    class Meta:
        model = Member
        fields = ['email', 'nom', 'prenom', 'departement', 'city', 'country', 'focal_point', 'date_of_birth','phone']


