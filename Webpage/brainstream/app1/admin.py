from django.contrib import admin

# Register your models here.
from .models import ejemplo, Datos


@admin.register(ejemplo)
class RequestDemoAdmin(admin.ModelAdmin):
     list_display = [field.name for field in ejemplo._meta.get_fields()]


class DatosAdmin(admin.ModelAdmin):
    list_display = ('id', 'valores')  # Campos que deseas mostrar en la lista

# Registra el modelo y la clase personalizada en el administrador
admin.site.register(Datos, DatosAdmin)