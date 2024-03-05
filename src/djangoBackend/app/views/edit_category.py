from django.views.generic import FormView
from django.contrib.auth.models import User
from app.forms import NewCategoryForm
from django.shortcuts import redirect
from app.models import Kategorie

class EditCategoryListView(FormView):
    template_name = "edit_category.html"
    form_class = NewCategoryForm
    success_url = "/category_approve"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = User.objects.get(pk=self.request.user.pk)
            forTest = Kategorie.objects.get(owner=user, pk=self.kwargs["id"])
        except:
            forTest = None
            
        if forTest or self.request.user.is_staff or self.request.user.is_superuser:
            kategorie = Kategorie.objects.get(pk=self.kwargs["id"])
            context['form'] = NewCategoryForm(instance=kategorie)
        else:
            context['message'] = "Nemáte oprávnění vidět/upravovat tuhle kategorii."
        
        return context
            
    def post(self, request, **kwargs):
        self.category = Kategorie.objects.get(pk=self.kwargs["id"])
        categoryForm = NewCategoryForm(request.POST, instance=self.category)
        if categoryForm.is_valid():
            categoryForm.save()
            
            return redirect('/category_approve')