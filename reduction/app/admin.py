from django.contrib import admin

# Register your models here.
from .models import URL


class TimeCachingAdmin(admin.ModelAdmin):
    model = URL
    list_display = ['url', 'reduction_url']
    fields = ['url', 'reduction_url']


admin.site.register(URL, TimeCachingAdmin)
