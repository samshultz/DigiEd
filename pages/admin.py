from django.contrib import admin

from .models import DiscountSection


@admin.register(DiscountSection)
class DiscountSectionAdmin(admin.ModelAdmin):
    '''Admin View for DiscountSection'''

    list_display = ('title', 'percent_discount', 'start_date', 'end_date', 'active')
    list_filter = ('active',)
    