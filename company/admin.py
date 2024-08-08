from django.contrib import admin
from .models import Empresas, Documentos, Metricas

# Register your models here.
admin.site.register(Empresas)
admin.site.register(Documentos)
admin.site.register(Metricas)
