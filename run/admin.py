from django.contrib import admin
from .models import RssiDataMore, RssiDataLess



class RssiDataLessAdmin(admin.ModelAdmin):
    list_display = ('host', 'time')


class RssiDataMoreAdmin(admin.ModelAdmin):
    list_display = ('host', 'time')


# Register your models here.
admin.site.register(RssiDataMore, RssiDataMoreAdmin)
admin.site.register(RssiDataLess, RssiDataLessAdmin)
