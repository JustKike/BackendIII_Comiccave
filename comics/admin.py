from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Comic, Categoria
# Register your models here.
# admin.site.register(Comic)

admin.site.register(Permission)

@admin.register(Categoria)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["user","descripcion", "updated_at"]

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ["titulo", "categoria", "imagen", "updated_at"]
