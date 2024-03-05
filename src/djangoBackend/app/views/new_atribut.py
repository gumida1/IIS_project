from django.views.generic import FormView
from app.forms import NewAtributeForm
from django.urls import reverse

class AddAtributeListView(FormView):
    template_name = "new_atribut.html"
    form_class = NewAtributeForm
    category_id = None

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        form.save()
        self.category_id = self.kwargs["id"]
        return super().form_valid(form)

    def get_success_url(self):
        
        return reverse('new_atribut', kwargs={'id': self.category_id})

