from django.contrib import admin
from .models import Sex, Type, PeriodsAndMovements, Artist, Artwork

admin.site.register(Sex)
admin.site.register(Type)
admin.site.register(PeriodsAndMovements)
admin.site.register(Artist)
admin.site.register(Artwork)

# Register your models here.
