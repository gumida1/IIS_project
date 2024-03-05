from django.views.generic import FormView
from app.forms import Create_offer_form, save_price_form, samosber_form
from app.models import Produkt, AtributHodnota, Atribut, Samosber, Uzivatel
from app.models import Kategorie
from django.urls import reverse
from django.contrib import messages

class Create_off(FormView):
    template_name = "create_offer.html"
    form_class = Create_offer_form

    def get_success_url(self):
        return reverse('create_offer_attrs', kwargs={'name_pk': self.request.POST["name"], 'category_pk': self.request.POST["kategorie"], \
        'dostupne_mnozstvi': self.request.POST["dostupne_mnozstvi"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if float(form["dostupne_mnozstvi"].value()) <= 0:
            messages.warning(self.request, "Číslo musí být kladné nebo větší jako 0.")
            return self.render_to_response(self.get_context_data(request=self.request, form=form))
        
        return self.form_valid(form)
    
class Create_samosber(FormView):
    template_name = "samosber.html"
    form_class = samosber_form

    success_url = "/index"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        catobj = Kategorie.objects.get(pk=self.kwargs['category_pk']) 
        print(self.kwargs['name_pk'])
        print(self.kwargs['dostupne_mnozstvi'])
        nabidka = Produkt(name=self.kwargs['name_pk'], kategorie=catobj, owner=self.request.user,dostupne_mnozstvi=self.kwargs['dostupne_mnozstvi']) 
        nabidka.save()
        attrs = Atribut.objects.all().filter(name="_cena_", datatype='F', is_price=True, kategorie=catobj)
        if (attrs.exists()):
            attribut_cena = Atribut.objects.get(name="_cena_", datatype='F', is_price=True, kategorie=catobj)
        else:
            attribut_cena = Atribut.objects.create(name="_cena_", datatype='F', is_price=True, kategorie=catobj)
        attribut_cena.save()
        nabidka_cena = Produkt.objects.get(owner=self.request.user, name=self.kwargs['name_pk'])
        if (self.kwargs['kgkus'] == "kg"):
            cena = AtributHodnota(floatHodnota=self.kwargs['cena'], atribut=attribut_cena, produkt=nabidka_cena)
            cena.save()
        elif (self.kwargs['kgkus'] == "kus"):
            kusy = int(self.kwargs['cena'])
            cena = AtributHodnota(intHodnota=kusy, atribut=attribut_cena, produkt=nabidka_cena)
            cena.save()
        
        samosber_var = Samosber(zacatek=self.request.POST["zacatek"], konec=self.request.POST["konec"], misto_konani=self.request.POST["misto_konani"], \
                                uzivatel=self.request.user, produkty=nabidka)
        samosber_var.save()
        
        uzivatel = Uzivatel.objects.get(user=self.request.user)
        uzivatel.is_farmer = True
        uzivatel.save()
        
        return super().form_valid(form)
    
class Create_off_attrs(FormView):
    template_name = "create_offer_attrs.html"
    form_class = save_price_form

    def get_success_url(self):
        check = self.request.POST.get('samosber')
        if (check == "samosber"):
            return reverse('create_samosber', kwargs={'name_pk': self.kwargs['name_pk'], 'cena': self.request.POST["floatHodnota"], \
                            'kgkus': self.request.POST.get('dropdown_menu_option'), 'category_pk': self.kwargs['category_pk'],'dostupne_mnozstvi': self.kwargs['dostupne_mnozstvi']})
        else:
            return reverse('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produkty = Produkt.objects.all()
        for produkt in produkty:
            if (produkt.name == self.kwargs['name_pk'] and produkt.owner == self.request.user):
                context['message'] = "Již jste vytvořil nabídku se stejným názvem. Akci prosím opakujte s jiným názvem!"
                
        attrs_arr=[]
        attrs = Atribut.objects.all()
        for attr in attrs:
            if (attr.is_price == False):
                if (int(attr.kategorie.pk) == int(self.kwargs['category_pk'])):
                    attrs_arr.append(attr)
        context['attrs'] = attrs_arr
        
        return context
    
    def post(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if self.request.user.is_authenticated:
            username = self.request.user.username
            
            check = self.request.POST.get('samosber')
            if(check == "samosber"):
                pass
            else:                
                if float(self.request.POST["floatHodnota"]) < 0:
                    messages.warning(self.request, "Cena nemůže být záporná.")
                    return self.render_to_response(self.get_context_data(request=self.request, form=form))
                
                catobj = Kategorie.objects.get(pk=self.kwargs['category_pk']) 
                nabidka = Produkt(name=self.kwargs['name_pk'], kategorie=catobj, owner=self.request.user,dostupne_mnozstvi=self.kwargs['dostupne_mnozstvi']) 
                nabidka.save()
                
                attrs = Atribut.objects.all().filter(name="_cena_", datatype='F', is_price=True, kategorie=catobj)
                if (attrs.exists()):
                    attribut_cena = Atribut.objects.get(name="_cena_", datatype='F', is_price=True, kategorie=catobj)
                else:
                    attribut_cena = Atribut.objects.create(name="_cena_", datatype='F', is_price=True, kategorie=catobj)
                attribut_cena.save()
                nabidka_cena = Produkt.objects.get(owner=self.request.user, name=self.kwargs['name_pk'])
                if self.request.method == 'POST':
                    answer = self.request.POST.get('dropdown_menu_option')
                    if (answer == "kg"):
                        cena = AtributHodnota(floatHodnota=self.request.POST["floatHodnota"], atribut=attribut_cena, produkt=nabidka_cena)
                        cena.save()
                    elif (answer == "kus"):
                        kusy_ = self.request.POST["floatHodnota"]
                        kusy = int(float(kusy_))
                        cena = AtributHodnota(intHodnota=kusy, atribut=attribut_cena, produkt=nabidka_cena)
                        cena.save()
            
                attrs = Atribut.objects.all()
                for attr in attrs:
                    if (attr.is_price == False):
                        if (int(attr.kategorie.pk) == int(self.kwargs['category_pk'])):      
                            atribut_next = Atribut.objects.get(name=attr, kategorie=self.kwargs["category_pk"])
                            try:
                                upd_atr = (attr.name).split(" ")[0]
                            except:
                                upd_atr = attr.name
                            input_atr = request.POST[upd_atr] 
                            hodnota_create = AtributHodnota.objects.create(strHodnota=input_atr, \
                                                produkt=nabidka, atribut=atribut_next)
                            hodnota_create.save()
                                        
                uzivatel = Uzivatel.objects.get(user=self.request.user)
                uzivatel.is_farmer = True
                uzivatel.save()
            
        return super().form_valid(form)
