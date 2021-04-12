from django.contrib import admin
from main .models import Account,Notes

class AccountA(admin.ModelAdmin):
    model=Account
    list_display=['id','username','email','batch','is_prof','is_superuser']

admin.site.register(Account,AccountA)


class NotesA(admin.ModelAdmin):
    model=Notes
    list_display=['userid','slotid','notes']

admin.site.register(Notes,NotesA)