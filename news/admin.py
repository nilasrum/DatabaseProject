from django.contrib import admin
from .models import AdminPost, Contest, Teams

# Register your models here.
admin.site.register(AdminPost)
admin.site.register(Contest)
admin.site.register(Teams)
