from django.contrib import admin

# Register your models here.
from .models import ejemplo, Datos


@admin.register(ejemplo)
class RequestDemoAdmin(admin.ModelAdmin):
     list_display = [field.name for field in ejemplo._meta.get_fields()]


class DatosAdmin(admin.ModelAdmin):
    list_display = ('id',
                     'valores0', "valores1", 'valores2', "valores3",
                     'valores4', "valores5", 'valores6', "valores7",
                     'valores8', "valores9", 'valores10', "valores11",
                     'valores12', "valores13", 'valores14', "valores15",)  # Campos que deseas mostrar en la lista

# Registra el modelo y la clase personalizada en el administrador
admin.site.register(Datos, DatosAdmin)