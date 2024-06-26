from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Plan)
admin.site.register(Order)