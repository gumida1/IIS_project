from django.shortcuts import redirect
from app.models import Objednavka, Produkt_Objednavka, AtributHodnota, Uzivatel
from django_unicorn.components import UnicornView

class KosikView(UnicornView):
    template_name = "kosik.html"
    obj = None
         
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            obj = Objednavka.objects.get(vyrizena=False, objednavajici=self.request.user)
            produktObj = Produkt_Objednavka.objects.filter(objednavka=obj)
            self.obj = obj
        except:
            context["objednavky"] = []
            return context
            
        send = []
        celkova_cena = 0
        for objednavka in produktObj:
            for atri in AtributHodnota.objects.filter(produkt=objednavka.produkt):
                if atri.atribut.name == "_cena_":
                    cena = atri.floatHodnota if atri.floatHodnota != None else atri.intHodnota
                    typ = "kus" if type(cena) == int else "kg"
                    send.append((objednavka.produkt.name, objednavka.mnozstvi, cena, objednavka.mnozstvi * cena, objednavka.pk, typ))
                    celkova_cena += objednavka.mnozstvi * cena

        context["objednavky"] = send
        context["celkova_cena"] = celkova_cena
    
        return context
        
    def delete(self, objednavka_pk):
        prod=Produkt_Objednavka.objects.get(pk=objednavka_pk)
        prod.produkt.dostupne_mnozstvi+=prod.mnozstvi
        prod.produkt.save()
        Produkt_Objednavka.objects.get(pk=objednavka_pk).delete()
        
        return redirect("kosik")
        
    def sendObjednavka(self):
        objednavka = Objednavka.objects.get(objednavajici=self.request.user, pk=self.obj["pk"])
        objednavka.vyrizena = True
        objednavka.save()
        
        uzivatel = Uzivatel.objects.get(user=self.request.user)
        uzivatel.is_customer = True
        uzivatel.save()
        
        return redirect("index")
    