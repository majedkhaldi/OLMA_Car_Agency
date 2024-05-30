from django.contrib import admin
from .models import Car, Cart, User, Order, Appointment, CarImage

# Registering other models
admin.site.register(Cart)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Appointment)

# Inline admin descriptor for CarImage model
class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

# Admin descriptor for Car model with CarImage inline
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]

# Register Car model with CarAdmin
admin.site.register(Car, CarAdmin)

# CarImage does not need to be registered separately since it's handled as an inline
# admin.site.register(CarImage)
