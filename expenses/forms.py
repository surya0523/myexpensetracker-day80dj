from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}), # HTML5 date input for better user experience
        }