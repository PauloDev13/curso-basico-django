from django.urls import path
from . import views

urlpatterns = [
    path('add_company/', views.add_company, name='add_company'),
    path('list_companies/', views.list_companies, name='list_companies'),
    path('company/<int:id>', views.company, name='company'),
    path('add_document/<int:id>', views.add_document, name='add_document'),
    path('remove_document/<int:id>', views.remove_document, name='remove_document'),
    path('add_metric/<int:id>', views.add_metric, name="add_metric"),
]
