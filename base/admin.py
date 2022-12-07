from django.contrib import admin

# Register your models here.
from base.models import Account
from base.forms import UserForm

class AccountAdmin(admin.ModelAdmin):
    form = UserForm
    fields = ('first_name', 'last_name', 'username', 'email', 'role', 'password1', 'password2')
    

admin.site.register(Account, AccountAdmin)