from django.views.generic import FormView
from app.forms import RegisterForm
from django.contrib.auth import login
from app.models import Uzivatel

class RegisterListView(FormView):
    template_name = "sign_up.html"
    form_class = RegisterForm
    success_url = "/index"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        User = form.save()  
        uzivatel = Uzivatel(is_farmer=False, is_customer=False, phone_number=self.request.POST["phone_number"], user=User)
        uzivatel.save()
        User.save()
        
        login(self.request, User)
    
        return super().form_valid(form)
    
    