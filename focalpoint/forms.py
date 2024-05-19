from .models import Categorie, FocalPoint, Information, Publication
from users.models import Alerte
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class FocalPointCreateForm(forms.ModelForm):
    name = forms.CharField(label='Nom', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    country = CountryField(null=True, blank=True).formfield(
        label='Pays',
        widget=CountrySelectWidget(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    access_code = forms.CharField(label='Code d\'accès', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    telephone = forms.CharField(label='Téléphone', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    access_pass = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control'}))
    access_pass_2 = forms.CharField(label='Confirmation du mot de passe', widget=forms.PasswordInput(attrs={'autofocus': True, 'class': 'form-control'}))

    class Meta:
        model = FocalPoint
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.country:
            self.fields['country'].initial = instance.get_country_display_full()

    def clean_email(self):
        '''
        Vérifiez que l'e-mail est disponible.
        '''
        email = self.cleaned_data.get('email')
        qs = FocalPoint.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà enregistrée.")
        return email

    def save(self, commit=True):
        # Enregistrez le mot de passe fourni au format haché
        fp = super().save(commit=False)
        fp.access_pass = self.cleaned_data["access_pass"]
        if commit:
            fp.active=True
            fp.save()
        return fp
    

class FocalPointEditForm(forms.ModelForm):
    name = forms.CharField(label='Nom', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    country = CountryField(null=True, blank=True).formfield(
        label='Pays',
        widget=CountrySelectWidget(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    access_code = forms.CharField(label='Code d\'accès', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    telephone = forms.CharField(label='Téléphone', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    access_pass = forms.CharField(label='Mot de passe', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))

    class Meta:
        model = FocalPoint
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.country:
            self.fields['country'].initial = instance.get_country_display_full()

    # def clean_email(self):
    #     '''
    #     Vérifiez que l'e-mail est disponible.
    #     '''
    #     email = self.cleaned_data.get('email')
    #     qs = FocalPoint.objects.get(email=email)
    #     if qs.id is not self.id:
    #         raise forms.ValidationError("Cette adresse e-mail est déjà enregistrée.")
    #     return email

    def save(self, commit=True):
        # Enregistrez le mot de passe fourni au format haché
        fp = super().save(commit=False)
        fp.access_pass = self.cleaned_data["access_pass"]
        if commit:
            fp.active=True
            fp.save()
        return fp


class FocalPointForm(forms.ModelForm):
    name = forms.CharField(label='Nom', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    country = CountryField(null=True, blank=True).formfield(
        label='Pays',
        widget=CountrySelectWidget(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    access_code = forms.CharField(label='Code d\'accès', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))

    class Meta:
        model = FocalPoint
        fields = ['name', 'email', 'country', 'access_code']

class AlterFPForm(forms.ModelForm):
    key=forms.IntegerField()
    name = forms.CharField(label='Nom', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    country = CountryField(null=True, blank=True).formfield(
        label='Pays',
        widget=CountrySelectWidget(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    access_code = forms.CharField(label='Code d\'accès', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    class Meta:
        model = FocalPoint
        fields = ['name', 'country', 'email', 'access_code']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        key = self.cleaned_data.get('key')
        if FocalPoint.objects.filter(email=email).exclude(pk=key).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà enregistrée.")
        return email

    def save(self, commit=True):
        fp = super().save(commit=False)        
        if commit:
            fp.save(update_fields=['name', 'country', 'email', 'access_code'])
        return fp


class EditAlertForm(forms.ModelForm):
    title = forms.CharField(label='Titre', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    #file = forms.FileField(label='Fichier à joindre', widget=forms.FileInput(attrs={'autofocus': True, 'class': 'form-control'}))
    contenu = forms.CharField(
        label='Contenu',  
        widget=forms.Textarea(attrs={'autofocus': True, 'class': 'form-control'}),  
    )
    
    class Meta:
        model = Alerte
        fields = ['title', 'contenu']


class PublicateForm(forms.ModelForm):
    focalpoint = forms.ModelMultipleChoiceField(
        label='Points focaux',
        queryset=FocalPoint.objects.all(), 
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Publication 
        fields = ['focalpoint']


class AddInfoForm(forms.ModelForm):
    title = forms.CharField(label='Titre', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    categorie = forms.ModelChoiceField(
        label='Catégorie',  # Label pour le champ
        queryset=Categorie.objects.all(),  # Le queryset pour charger les options depuis la base de données
        widget=forms.Select(attrs={'class': 'form-control'}),  # Le widget Select avec des attributs de classe CSS
    )
    description = forms.CharField(
        label='Description',  # Label pour le champ
        widget=forms.Textarea(attrs={'autofocus': True, 'class': 'form-control'}),  # Utilisez Textarea pour les champs de texte long
    )
    class Meta:
        model = Information 
        fields = ['title', 'categorie', 'description',]

class CreateInformation(forms.Form):
    title = forms.CharField(label='Titre', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    categorie = forms.ModelChoiceField(
        label='Catégorie',  # Label pour le champ
        queryset=Categorie.objects.all(),  # Le queryset pour charger les options depuis la base de données
        widget=forms.Select(attrs={'class': 'form-control'}),  # Le widget Select avec des attributs de classe CSS
    )
    description = forms.CharField(
        label='Description',  # Label pour le champ
        widget=forms.Textarea(attrs={'autofocus': True, 'class': 'form-control'}),  # Utilisez Textarea pour les champs de texte long
    )
    focalpoint = forms.ModelMultipleChoiceField(
        label='Points focaux',
        queryset=FocalPoint.objects.all(), 
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )


class AddCategorieForm(forms.ModelForm):
    label = forms.CharField(label='Non de la categorie', widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    class Meta:
        model = Categorie 
        fields = ['label']



    
    