from django_unicorn.components import UnicornView
from django.contrib.auth.models import User
from app.models import Objednavka, Produkt, Produkt_Objednavka, AtributHodnota, Samosber, Recenze
from django.views.generic import ListView
from django.shortcuts import redirect

class Objednavky(UnicornView):
    template_name = "objednavky.html"
    model = User
    paginate_by = 9999
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            context["message"] = "Nelze"
            return context
        objednavky=[]
        produkty=[]
        cena={}
        mnozstvi=0
        objednavkyy = Objednavka.objects.filter(objednavajici=self.request.user)
        for k in objednavkyy:
            if(k.objednavajici == self.request.user and k.vyrizena == True):
                objednavky.append(k)
                temp=0
                for h in Produkt_Objednavka.objects.all():
                    if(k.id == h.objednavka.id):
                        produkty.append(h)
                        for j in AtributHodnota.objects.all():
                            if(j.produkt.id == h.produkt.id): 
                                if(j.floatHodnota):   
                                    temp=j.floatHodnota*h.mnozstvi+temp
                                elif(j.intHodnota):
                                    temp=j.intHodnota*h.mnozstvi+temp
                                cena[k.id]=(round(temp,2))
        context["orders"]=objednavky
        context["atr"]=cena
        samosbers = Samosber.objects.all()
        cena_samo=0
        samo=[]
        for i in samosbers:
            samosbery=i.uzivatele.all()
            x=samosbery.values_list('username')

            for y in x:
                if(str(y[0]) == str(self.request.user)):
                    for atri in AtributHodnota.objects.filter(produkt=i.produkty):
                        if atri.atribut.name == "_cena_":
                            cena_samo = atri.floatHodnota if atri.floatHodnota != None else atri.intHodnota
                            typ = "kus" if type(cena_samo) == int else "kg"
                            cena_samo =str(cena_samo) + " Kč/"+typ
                            samo.append((i,cena_samo))
                else:
                    pass

        context["samos"]=samo
        context["products"]=produkty
            
        return context
    
class recenze(ListView):
    template_name = "recenze.html"
    model = User
    success_url = "/index"
    paginate_by = 9999
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prod_id = Produkt.objects.get(pk=self.kwargs['id'])
        
        context['produkt'] = prod_id
        
        return context

class pomocna(ListView):
    template_name = "recenze.html"
    model = User
    success_url = "/index"
    paginate_by = 9999
    
    def get(self, *args, **kwargs):
        p = Produkt.objects.get(pk=self.kwargs['id'])
        rec_all = Recenze.objects.all().filter(hodnotitel=self.request.user, produkt=p)
        
        if not (rec_all.exists()):
            recenze = Recenze.objects.create(hodnoceni=self.kwargs['rec'], produkt=p, hodnotitel=self.request.user)
        else:
            recenze = Recenze.objects.get(hodnotitel=self.request.user, produkt=p)
            recenze.hodnoceni = self.kwargs['rec']
            
        recenze.save()
            
        return redirect("objednavky")