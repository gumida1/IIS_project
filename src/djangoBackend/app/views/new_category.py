from django.views.generic import FormView
from app.forms import NewCategoryForm
from django.urls import reverse

class NewCategoryListView(FormView):
    template_name = "new_category.html"
    form_class = NewCategoryForm
    category_id = None

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        obj = form.save(False)
        obj.owner = self.request.user
        obj.save()
        self.category_id = obj.pk
        return super().form_valid(form)
    
    def get_success_url(self):
        
        return reverse('new_atribut', kwargs={'id': self.category_id})  