from django.contrib import admin

from .models import Address
from .models import Letting

admin.site.register(Address)
admin.site.register(Letting)
