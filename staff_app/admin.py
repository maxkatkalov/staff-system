from django.contrib import admin
from .models import Company, Office, Department, Position, StaffUser

admin.site.register(Company)
admin.site.register(Office)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(StaffUser)
