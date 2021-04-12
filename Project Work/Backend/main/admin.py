from django.contrib import admin
from main .models import Account

class AccountA(admin.ModelAdmin):
    model=Account
    list_display=['id','username','email','batch','is_prof','is_superuser']

admin.site.register(Account,AccountA)