from django.contrib import admin
from .models import Wallet,Category,Transactions
from django.contrib.auth.models import Group


admin.site.unregister(Group)

admin.site.register(Wallet)
admin.site.register(Category)
admin.site.register(Transactions)
