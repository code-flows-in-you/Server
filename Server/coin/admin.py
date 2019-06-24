from django.contrib import admin

# Register your models here.

from .models import UserCoin, CoinFlow

admin.site.register(UserCoin)
admin.site.register(CoinFlow)