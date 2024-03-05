from django.views.generic import ListView, FormView
from django.contrib.auth.models import User
from app.models import Produkt, AtributHodnota, Samosber, Produkt_Objednavka, Objednavka, Kategorie, Recenze, Atribut, Uzivatel
from django.urls import reverse
from app.forms import kosik_form
from django.contrib import messages

class IndexListView(ListView):
    template_name = "index.html"
    model = Produkt
    state = ""
    paginate_by = 10
    
    def get_queryset(self):
        test = []
        
        try:
            return super().get_queryset().filter(name__icontains=self.kwargs["produkt"]).exclude(dostupne_mnozstvi=0).order_by("name")
        except:
            ...
            
        try:
            for kat in Kategorie.objects.filter(name__icontains=self.kwargs["kategorie"]):
                for x in Produkt.objects.filter(kategorie=kat).exclude(dostupne_mnozstvi=0):
                    test.append(x.id)
            return super().get_queryset().filter(id__in=test).order_by("name")         
        except:
            ...
        
        try:
            for uz in User.objects.filter(username__icontains=self.kwargs["farmar"]):
                for x in Produkt.objects.filter(owner=uz).exclude(dostupne_mnozstvi=0):
                    test.append(x.id)
            return super().get_queryset().filter(id__in=test).order_by("name")
        except:
            ...        
        
        return super().get_queryset().all().exclude(dostupne_mnozstvi=0).order_by("name")
    
    def get_success_url(self):
        return reverse('create_offer')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produkty = self.object_list
            
        hodnoty = AtributHodnota.objects.all()
        samosber = Samosber.objects.all()
        
        button_arr = []
        button_dict = {}
        
        for samo in samosber:
            if (samo.produkty.id != None):
                button_dict[samo.produkty.id] = True
                button_arr.append(samo.produkty.id)
                
        for produkt in produkty:
            if not (produkt.id in button_arr):
                button_dict[produkt.id] = False

        recenze = Recenze.objects.all()
        recenze_dict = {}

        cnt = 0
        cislo = 0
        for r in recenze:
            pole = Recenze.objects.all().filter(produkt=r.produkt)
            for prvek in pole:
                cislo += int(prvek.hodnoceni)
                cnt += 1
            if (r.produkt.id not in recenze_dict.keys()):
                recenze_dict[r.produkt.id] = round(cislo/cnt, 1)
            cislo = 0
            cnt = 0
            
        context['produkty'] = produkty
        context['hodnoty'] = hodnoty
        context['samosbery'] = samosber
        context['is_samosber'] = button_dict
        context['recenze'] = recenze_dict

        return context
        
class add_to_kosik(FormView):
    template_name = "add_to_kosik.html"
    form_class = kosik_form
    success_url = "/index"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        produkt = Produkt.objects.get(pk=self.kwargs['id'])
        atr_dict = {}
        atributy = Atribut.objects.all()
        atr_hod = AtributHodnota.objects.all().filter(produkt=produkt.id)
        for atr in atr_hod:
            if atr.strHodnota != None:
                print(atr.strHodnota)
                for atribut in atributy:
                    if (atr.atribut.id == atribut.id):
                        atr_dict[atribut.name] = atr.strHodnota
                        
        context['atributiky'] = atr_dict
        context['pocet'] = len(atr_dict)
        print(atr_dict)
        
        return context
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if self.request.user.is_authenticated:
            username = self.request.user.username
        produktos = Produkt.objects.get(pk=self.kwargs['id'])
        
        objednavka = Objednavka.objects.all().filter(objednavajici=self.request.user, vyrizena=False)
        if (objednavka.exists()):
            objednavka_obj = Objednavka.objects.get(pk=objednavka[0].id)
            mnoz=self.request.POST['mnozstvi']
            if(float(mnoz) > float(produktos.dostupne_mnozstvi) or float(mnoz) <= 0):
                messages.warning(self.request, f"Je dostupných pouze {produktos.dostupne_mnozstvi} kusů nebo číslo nesmí být menší jak 0.")
                return self.render_to_response(self.get_context_data(request=self.request, form=form))
            else:
                produktos.dostupne_mnozstvi=float(produktos.dostupne_mnozstvi)-float(mnoz)
                produkt_v_objednavce = Produkt_Objednavka.objects.create(mnozstvi=self.request.POST['mnozstvi'], \
                                        produkt=produktos, objednavka=objednavka_obj)
                produkt_v_objednavce.save()
                produktos.save()
        else:
            objednavka = Objednavka.objects.create(objednavajici=self.request.user, vyrizena=False)
            mnoz=self.request.POST['mnozstvi']
            if(float(mnoz) > float(produktos.dostupne_mnozstvi) or float(mnoz) <= 0):
                return self.form_invalid(form)
            else:
                produktos.dostupne_mnozstvi=float(produktos.dostupne_mnozstvi)-float(mnoz)
                produkt_v_objednavce = Produkt_Objednavka.objects.create(mnozstvi=self.request.POST['mnozstvi'], \
                                        produkt=produktos, objednavka=objednavka)
                produkt_v_objednavce.save()
                produktos.save()
            
        return super().form_valid(form)
    
class reg_to_samosber(ListView):
    template_name = "reg_to_samosber.html"
    model = User
    success_url = "/index"
    paginate_by = 9999
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prod_id = Produkt.objects.get(pk=self.kwargs['id'])
        samo_obj = Samosber.objects.all().filter(produkty=prod_id)
        samo_obj[0].uzivatele.add(self.request.user)
        samo_obj[0].save()
        
        uzivatel = Uzivatel.objects.get(user=self.request.user)
        uzivatel.is_customer = True
        uzivatel.save()
        
        context['info_o_samo'] = samo_obj[0]
        
        return context
    