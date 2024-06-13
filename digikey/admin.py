from django.contrib import admin
from digikey.models import RawDataDigikey, DigikeyComponent, DigikeyBrand, DigikeyPrice, DigikeyStock


admin.site.register(RawDataDigikey)
admin.site.register(DigikeyComponent)
admin.site.register(DigikeyBrand)
admin.site.register(DigikeyPrice)
admin.site.register(DigikeyStock)