from django.views.generic import FormView
from django.contrib.auth.models import User
from app.forms import ChangePasswordForm
from django.shortcuts import redirect
from app.models import Kategorie
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

class ChangePasswordView(FormView):
    template_name = "change_password.html"
    form_class = ChangePasswordForm
    success_url = "index"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PasswordChangeForm(self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        
        messages.warning(self.request, "Špatně zadaná hodnota")
        return self.render_to_response(self.get_context_data(request=self.request, form=form))
