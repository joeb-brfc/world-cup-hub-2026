from django.contrib import admin
from models import Stadium

# Register your models here.
admin.site.register(Stadium, StadiumAdmin)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'capacity')
    search_fields = ('name', 'city')