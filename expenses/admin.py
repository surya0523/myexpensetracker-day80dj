from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'date', 'user')
    list_filter = ('category', 'date', 'user')
    search_fields = ('title', 'notes', 'user__username', 'category')
    date_hierarchy = 'date' # Adds date drill-down navigation
    raw_id_fields = ('user',) # Useful if you have many users