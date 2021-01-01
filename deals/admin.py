from django.contrib import admin
from deals.models import Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['product', 'start_date', 'expiry_date']
