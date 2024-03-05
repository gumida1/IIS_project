from django_unicorn.components import UnicornView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def show(request):
    if request.user.is_superuser:
        obj = User.objects.all()
        return render(request, "edit_moderators.html", {"users": obj})
    else:
        return redirect('/index')

class EditModeratorsListView(UnicornView):
    template_name = "edit_moderators.html"
    count = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context["users"] = User.objects.order_by("username").all()
        else:
            context['message'] = "Nemáte oprávnění vidět tuhle stránku."
            
        return context
        
    def switchmod(self, user_pk):
        user = User.objects.get(pk=user_pk)
        user.is_staff = not user.is_staff
        user.save()
        
    def deleteUser(self, user_pk):
        User.objects.get(pk=user_pk).delete()
