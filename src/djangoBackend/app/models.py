from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Uzivatel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    is_farmer = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20)
 
class Kategorie(models.Model):
    name = models.CharField(max_length=100, unique=True)
    nadkategorie = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    validated = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class Produkt(models.Model):
    name = models.CharField(max_length=100)
    kategorie = models.ForeignKey(Kategorie, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    dostupne_mnozstvi = models.IntegerField(null=True, default=0, blank=True)
    
    def __str__(self):
        return self.name
        
class Atribut(models.Model):
    DATATYPE_CHOICES = [
        ('I', 'Integer'),
        ('F', 'Float'),
        ('S', 'String'),
    ]
    
    name = models.CharField(max_length=100)
    datatype = models.CharField(max_length=1, choices=DATATYPE_CHOICES)
    is_required = models.BooleanField(default=False)
    is_price = models.BooleanField(default=False)
    kategorie = models.ForeignKey(Kategorie, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.name
    
class AtributHodnota(models.Model):
    intHodnota = models.IntegerField(null=True, default=None, blank=True)
    floatHodnota = models.FloatField(null=True, default=None, blank=True)
    strHodnota = models.CharField(max_length=100, null=True, default=None, blank=True)
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    atribut = models.ForeignKey(Atribut, on_delete=models.CASCADE)
    
class Samosber(models.Model):
    zacatek = models.DateTimeField(default=None)
    konec = models.DateTimeField(default=None)
    misto_konani = models.CharField(max_length=100)
    uzivatel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owner')
    uzivatele = models.ManyToManyField(User, related_name='TEST_HERE')
    produkty = models.ForeignKey(Produkt, on_delete=models.CASCADE, default=None)
    
class Objednavka(models.Model):
    objednavajici = models.ForeignKey(User, on_delete=models.CASCADE)
    vyrizena = models.BooleanField(default=False)

class Produkt_Objednavka(models.Model):
    objednavka = models.ForeignKey(Objednavka, on_delete=models.CASCADE)
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    mnozstvi = models.FloatField()
    
class Recenze(models.Model):
    HODNOCENI_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    
    hodnoceni = models.IntegerField(choices=HODNOCENI_CHOICES)
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    hodnotitel = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
