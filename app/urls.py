from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('pessoas/', PeopleView.as_view(), name='people'),
    path('pessoas/adicionar/', PeopleAddView.as_view(), name='people_add'),
    path('pessoas/<int:pk>/editar/', PeopleEditView.as_view(), name='people_edit'),
    path('pessoas/<int:pk>/deletar/', PeopleDeleteView.as_view(), name='people_delete'),
]
