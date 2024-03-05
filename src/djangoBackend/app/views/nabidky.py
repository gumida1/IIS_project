from django.contrib.auth.models import User
from app.models import Produkt, AtributHodnota, Samosber
from django_unicorn.components import UnicornView

class Nabidky(UnicornView):
    template_name = "nabidky.html"
    model = User
    paginate_by = 9999
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.request.user.is_authenticated:
            context["message"] = "Nelze"
            return context
        produkty = Produkt.objects.filter(owner=self.request.user)
        send_obj = []
        send_samo = []
        cena=0
        for produkt in produkty:
            samos = Samosber.objects.filter(produkty=produkt)
            mnozstvi=produkt.dostupne_mnozstvi
            if(samos):
                for atri in AtributHodnota.objects.filter(produkt=produkt):
                    if atri.atribut.name == "_cena_":
                        cena = atri.floatHodnota if atri.floatHodnota != None else atri.intHodnota
                        typ = "kus" if type(cena) == int else "kg"
                        cena =str(cena) + " Kč/"+typ

                        send_samo.append((produkt,cena,samos[0]))
            else:
                for atri in AtributHodnota.objects.filter(produkt=produkt):
                    if atri.atribut.name == "_cena_":
                        cena = atri.floatHodnota if atri.floatHodnota != None else atri.intHodnota
                        typ = "kus" if type(cena) == int else "kg"
                        cena =str(cena) + " Kč/"+typ

                send_obj.append((produkt,cena,mnozstvi))
                
            context["offers"]=send_obj
            context["samosbers"]=send_samo
                
        return context
                
    def deleteNabidka(self, produkt_pk):
        Produkt.objects.get(pk=produkt_pk).delete()

    def deleteSamosber(self, samosber_pk):
        Samosber.objects.get(produkty=samosber_pk).delete()
        Produkt.objects.get(pk=samosber_pk).delete()