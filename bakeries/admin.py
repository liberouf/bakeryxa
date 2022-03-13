from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ghanadi,mahsool
from django.contrib.gis.admin import OSMGeoAdmin
from leaflet.admin import LeafletGeoAdmin






class ghanadiadmin(UserAdmin,LeafletGeoAdmin):
    list_display = ( 'name','owner','position')
    list_display_links = ('name',
    )
    #prepopulated_fields = {'slug': ('username',)}
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(ghanadi, ghanadiadmin)
admin.site.register(mahsool)