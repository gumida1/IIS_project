from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register([Uzivatel, Produkt, Kategorie, Atribut, AtributHodnota, Samosber, Objednavka, Produkt_Objednavka, Recenze])
