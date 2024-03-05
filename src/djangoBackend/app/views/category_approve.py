from django_unicorn.components import UnicornView
from app.models import Kategorie, Atribut

class CategoryApproveListView(UnicornView):
    template_name = "category_approve.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser or self.request.user.is_staff:
            cotegories = Kategorie.objects.order_by("name").all()
            array = {}
            for category in cotegories:
                array[category.name] = {}
                array[category.name]["category"] = category
                
                Atributes = Atribut.objects.all().filter(kategorie=category.pk).exclude(name="_cena_")
                array[category.name]["atributes"] = Atributes

            context["categories"] = array
        else:
            context['message'] = "Nemáte oprávnění vidět tuhle stránku."
            
        return context
            
    def switchmod(self, category_pk):
        kategorie = Kategorie.objects.get(pk=category_pk)
        kategorie.validated = not kategorie.validated
        kategorie.save()
        
    def deleteCategory(self, category_pk):
        Kategorie.objects.get(pk=category_pk).delete()
        
    def deleteAtribute(self, category_pk):
        Atribut.objects.get(pk=category_pk).delete()
    
