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
        "center={lat},{lon}"\
        "&zoom=16&size=800x300&maptype=roadmap"\
        "&markers=color:red%7Clabel:P%7C{lat},{lon}"\
        "&key={api_key}".format(
            lon=lon,
            lat=lat,
            api_key=settings.GOOGLE_MAP_API_KEY
        )
        if not obj.google_map_url:
            google_map_url = "https://www.google.com/maps/@{},{},zoom=16z".format(
                obj.point.y,
                obj.point.x
            )
        else:
            google_map_url = obj.google_map_url;
        return format_html(
                    (   '<span>Latitude: {}, Longitude: {}</span><br>'
                        '<a href="{}" '
                        'target="_blank"><img src="{}" alt="Open google maps"><br>Click to open google maps</a>'
                    ),
                    lat,
                    lon,
                    google_map_url,
                    google_statics_url,
               )
    lon_lat.short_description = "Lat/Lon on Google Map"

    readonly_fields = ("lon_lat","google_place_id")


admin.site.register(Place, PlaceAdmin)
