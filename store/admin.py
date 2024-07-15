from django.contrib import admin
from .models import User,shipping,Review,Cart,Customer,Chat,Product,ColourCoding,outfit,Professionals
# Register your models here.

admin.site.register(shipping)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Chat)
admin.site.register(Product)
admin.site.register(ColourCoding)
admin.site.register(outfit)
admin.site.register(Professionals)