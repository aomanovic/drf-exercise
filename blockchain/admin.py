from django.contrib import admin
from blockchain.models import SearchAddress, SearchTransaction, UserAddresses

admin.site.register(SearchAddress)
admin.site.register(SearchTransaction)
admin.site.register(UserAddresses)