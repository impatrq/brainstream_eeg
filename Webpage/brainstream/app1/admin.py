from django.contrib import admin

# Register your models here.
from .models import ejemplo


@admin.register(ejemplo)
class RequestDemoAdmin(admin.ModelAdmin):
     list_display = [field.name for field in
ejemplo._meta.get_fields()]
