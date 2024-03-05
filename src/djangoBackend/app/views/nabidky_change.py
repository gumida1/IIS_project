from django.views.generic import FormView
from django.contrib.auth.models import User
from app.forms import Create_offer_form, ProduktNameChange
from django.shortcuts import redirect
from app.models import Produkt
from django.contrib import messages

class NabidkyChange(FormView):
    form_class = Create_offer_form
    template_name = "nabidky_change.html"
    model = User
    success_url = "/nabidky"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = User.objects.get(pk=self.request.user.pk)
            forTest = Produkt.objects.get(owner=user, pk=self.kwargs["id"])
        except:
            forTest = None
            
        if forTest or self.request.user.is_staff or self.request.user.is_superuser:
            produkt = Produkt.objects.get(pk=self.kwargs["id"])
            context['form'] = Create_offer_form(instance=produkt)
        else:
            context['message'] = "Nemáte oprávnění vidět/upravovat tuhle plodinu."
        
        return context

    def post(self, request, **kwargs):
        self.produkt = Produkt.objects.get(pk=self.kwargs["id"])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if float(form["dostupne_mnozstvi"].value()) <= 0:
            messages.warning(self.request, "Číslo musí být kladné nebo větší jako 0.")
            return self.render_to_response(self.get_context_data(request=self.request, form=form))
        
        produktForm = ProduktNameChange(request.POST, instance=self.produkt)
        
        if produktForm.is_valid():
            produktForm.save()
            
            return redirect("/nabidky")
