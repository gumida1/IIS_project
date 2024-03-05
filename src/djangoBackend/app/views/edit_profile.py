from django.contrib.auth.models import User
from multi_form_view import MultiModelFormView
from app.forms import UpdateUserForm, UpdateUzivatelForm
from django.contrib import messages

class MyProfileListView(MultiModelFormView):
    id = None
    user = None
    template_name = "edit_profile.html"
    form_classes = {
        "user_form": UpdateUserForm,
        "uzivatel_form": UpdateUzivatelForm
        }
    success_url = "/index"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs["id"] == self.request.user.pk or self.request.user.is_superuser:
            self.user = User.objects.get(pk=self.kwargs["id"])
            context['forms']['user_form'] = UpdateUserForm(instance=self.user)
            context['forms']['uzivatel_form'] = UpdateUzivatelForm(instance=self.user.uzivatel)

        else:
            context['message'] = "Nemáte oprávnění vidět/upravovat tento profil."

        return context
        
    def post(self, request, **kwargs):
        self.user = User.objects.get(pk=self.kwargs["id"])
        userForm = UpdateUserForm(request.POST, instance=self.user)
        uzivatelForm = UpdateUzivatelForm(request.POST, request.FILES, instance=self.user.uzivatel)
        if userForm.is_valid() and uzivatelForm.is_valid():
            user_form = userForm.save()
            uzivatel_form = uzivatelForm.save(False)
            uzivatel_form.user = user_form
            uzivatel_form.save()
            
            context = super().post(request, **kwargs)
            messages.info(request, 'Údaje byly změněny.')
            return context
            
        else:
            context = super().post(request, **kwargs)
            messages.warning(request, 'Zadané uživatelské jméno je již obsazeno.')
            
            return context

        
    
   
   
   
   