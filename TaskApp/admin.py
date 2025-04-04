from django.contrib import admin
from .models import Employee,AddApps,Points,Role
# Register your models here.
admin.site.register(Employee)
admin.site.register(AddApps)
admin.site.register(Points)
admin.site.register(Role)