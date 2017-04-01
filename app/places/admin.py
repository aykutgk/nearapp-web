from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Place

class PlaceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Info', {
            'classes': ('extrapretty',),
            'fields': ('owner', 'name')
        }),
        ('Location', {
            'fields': ('lon_lat', 'google_place_id')
        }),
        ('Management', {
            'fields': ('active',)
        }),
    )

    def lon_lat(self, obj):
        lon = obj.point.x
        lat = obj.point.y
        google_statics_url = "https://maps.googleapis.com/maps/api/staticmap?"\
        "center={lon},{lat}"\
        "&zoom=12&size=800x300&maptype=roadmap"\
        "&markers=color:red%7Clabel:P%7C{lon},{lat}"\
        "&key={api_key}".format(
            lon=lon,
            lat=lat,
            api_key=settings.GOOGLE_MAP_API_KEY
        )
        return format_html(
                    (   '<span>Longitude: {}, Latitude: {}</span><br>'
                        '<a href="https://www.google.com/maps?q=loc:{},{}&zoom=8" '
                        'target="_blank"><img src="{}" alt="Open google maps"><br>Click to open google maps</a>'
                    ),
                    lon,
                    lat,
                    lon,
                    lat,
                    google_statics_url,
               )
    lon_lat.short_description = "Lon/Lat on Google Map"

    readonly_fields = ("lon_lat","google_place_id")


admin.site.register(Place, PlaceAdmin)
