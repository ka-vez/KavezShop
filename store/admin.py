from django.contrib import admin
from .models import Order, Product, Customer, Category, Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Profile)

#mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

#extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]

#Unregister the old way
admin.site.unregister(User)

#Reregister the new way
admin.site.register(User, UserAdmin)






