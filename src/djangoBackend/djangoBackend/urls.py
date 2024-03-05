from django.contrib import admin
from django.urls import path, include, register_converter, re_path
from app.views.edit_moderators import EditModeratorsListView 
from app.views.index import IndexListView
from app.views.register import RegisterListView
from app.views.edit_profile import MyProfileListView
from app.views.new_category import NewCategoryListView
from app.views.category_approve import CategoryApproveListView
from app.views.edit_category import EditCategoryListView
from app.views.nabidky import Nabidky
from app.views.objednavky import Objednavky
from app.views.create_offer import Create_off, Create_off_attrs, Create_samosber
from app.views.nabidky_change import NabidkyChange
from app.views.edit_atribute import EditAtributListView
from app.views.new_atribut import AddAtributeListView
from app.views.index import add_to_kosik, reg_to_samosber
from app.views.kosik import KosikView
from app.views.objednavky import recenze, pomocna
from app.views.change_password import ChangePasswordView

class FloatUrlParameterConverter:
    regex = '[0-9]+\.?[0-9]+'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

register_converter(FloatUrlParameterConverter, 'float')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', IndexListView.as_view(), name="index"),
    path('index/produkt=<str:produkt>', IndexListView.as_view(), name="index_args"),
    path('index/kategorie=<str:kategorie>', IndexListView.as_view(), name="index_args"),
    path('index/farmar=<str:farmar>', IndexListView.as_view(), name="index_args"),
    path('', include('django.contrib.auth.urls')),
    path('register', RegisterListView.as_view(), name="register"),
    path('edit_profile/<int:id>/', MyProfileListView.as_view(), name="edit_profile"),
    path('edit_moderators', EditModeratorsListView.as_view(), name="edit_moderators"),
    path("unicorn/", include("django_unicorn.urls")),
    path("new_category", NewCategoryListView.as_view(), name="new_category"),
    path("category_approve", CategoryApproveListView.as_view(), name="category_approve"),
    path("edit_category/<int:id>/", EditCategoryListView.as_view(), name="edit_category"),
    path('nabidky',Nabidky.as_view(),name="nabidky"),
    path('objednavky',Objednavky.as_view(),name="objednavky"),
    path('create_offer/', Create_off.as_view(), name="create_offer"),
    path('create_offer_attrs/<str:name_pk>/<str:category_pk>/<int:dostupne_mnozstvi>/', Create_off_attrs.as_view(), name="create_offer_attrs"),
    path("new_atribut/<int:id>/", AddAtributeListView.as_view(), name="new_atribut"),
    path("edit_atribute/<int:id>/", EditAtributListView.as_view(), name="edit_atribute"),
    path("samosber/<str:name_pk>/<float:cena>/<str:kgkus>/<str:category_pk>/<int:dostupne_mnozstvi>/", Create_samosber.as_view(), name="create_samosber"),
    path("nabidky_change/<int:id>/",NabidkyChange.as_view(),name="nabidky_change"),
    path("add/<int:id>/", add_to_kosik.as_view(), name="add"),
    path("kosik", KosikView.as_view(), name="kosik"),
    path("reg_to_samosber/<int:id>/", reg_to_samosber.as_view(), name="reg"),
    path("recenze/<int:id>/", recenze.as_view(), name="recenze"),
    path("pomocna/<int:id>/<int:rec>/", pomocna.as_view(), name="pomocna"),
    path("", IndexListView.as_view(), name="nothing"),
    path("change_password", ChangePasswordView.as_view(), name="change_password"),
]