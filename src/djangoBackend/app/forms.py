from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Uzivatel, Kategorie, Produkt, Atribut, AtributHodnota, Samosber, Produkt_Objednavka

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone_number", "password1", "password2"]
        
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Přihlašovací jméno"
        self.fields['username'].help_text = ""
        self.fields['first_name'].label = "Jméno"
        self.fields['last_name'].label = "Příjmení"
        self.fields['phone_number'].label = "Telefonní číslo"
        self.fields['password1'].label = "Heslo"
        self.fields['password1'].help_text = "<ul><li>Heslo nesmí být podobné přihlašovacímu jménu</li><li>Heslo musí obsahovat alespoň 8 znaků</li><li>Heslo nesmí být moc jednoduché a nesmí obsahovat pouze čísla</li></ul>"
        self.fields['password2'].label = "Potvrzení hesla"
        self.fields['password2'].help_text = ""
 
class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["password"]
        
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Přihlašovací jméno"
        self.fields['username'].help_text = ""
        self.fields['first_name'].label = "Jméno"
        self.fields['last_name'].label = "Příjmení"
        self.fields['email'].label = "Emailová adresa"
        
class UpdateUzivatelForm(forms.ModelForm):
    phone_number = forms.CharField(required=False)
    
    class Meta:
        model = Uzivatel
        fields = ["phone_number"]
        
    def __init__(self, *args, **kwargs):
        super(UpdateUzivatelForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].label = "Telefonní číslo"
        
class NewCategoryForm(forms.ModelForm):
    class Meta:
        model = Kategorie
        fields = ["name", "nadkategorie"]
        
    def __init__(self, *args, **kwargs):
        super(NewCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Název kategorie"
        
class NewAtributeForm(forms.ModelForm):
    class Meta:
        model = Atribut
        fields = ["name", "datatype", "is_required", "kategorie"]
        
    def __init__(self, *args, **kwargs):
        super(NewAtributeForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Název atributu"
        self.fields['datatype'].label = "Typ atributu"
        self.fields['is_required'].label = "Atribut se musí zadat"
        self.fields['kategorie'].label = "Patří kategorii"    
        
class Create_offer_form(forms.ModelForm):
    dostupne_mnozstvi=forms.IntegerField(required=True)
    class Meta:
        model = Produkt
        fields = ["name", "kategorie","dostupne_mnozstvi"] 
        
    def __init__(self, *args, **kwargs):
        super(Create_offer_form, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Název plodiny"
        self.fields['kategorie'].queryset = Kategorie.objects.filter(validated=True)
        self.fields['kategorie'].label = "Kategorie"
        self.fields['dostupne_mnozstvi'].label="Dostupné Množství"
        
class save_price_form(forms.ModelForm):
    floatHodnota = forms.CharField(required=True)
    
    class Meta:
        model = AtributHodnota
        fields = ["floatHodnota"]
        
    def __init__(self, *args, **kwargs):
        super(save_price_form, self).__init__(*args, **kwargs)
        self.fields['floatHodnota'].label = "Cena"
        
class samosber_form(forms.ModelForm):
    class Meta:
        model = Samosber
        fields = ["zacatek", "konec", "misto_konani"]
        
    def __init__(self, *args, **kwargs):
        super(samosber_form, self).__init__(*args, **kwargs)
        self.fields['zacatek'].label = "Začátek samosběru"
        self.fields['zacatek'].widget.attrs['placeholder'] = "YYYY-MM-DD"
        self.fields['konec'].label = "Konec samosběru"
        self.fields['konec'].widget.attrs['placeholder'] = "YYYY-MM-DD"
        self.fields['misto_konani'].label = "Místo konání"
        
class kosik_form(forms.ModelForm):
    class Meta:
        model = Produkt_Objednavka
        fields = ['mnozstvi']
        
    def __init__(self, *args, **kwargs):
        super(kosik_form, self).__init__(*args, **kwargs)
        self.fields['mnozstvi'].label = "Množství"
    
class ProduktNameChange(forms.ModelForm):
    name = forms.CharField(required=True)
    dostupne_mnozstvi = forms.IntegerField(required=True)

    class Meta:
        model = Produkt
        fields = ["name","dostupne_mnozstvi"]
        
    def __init__(self, *args, **kwargs):
        super(ProduktNameChange, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Název"
        self.fields['dostupne_mnozstvi'].label = "Dostupné množství"
