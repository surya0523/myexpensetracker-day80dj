from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.db.models import Sum
from datetime import date
import calendar
from django.contrib.admin.views.decorators import staff_member_required # For admin view

from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.models import User # Import User for admin view

# --- Authentication Views ---
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'expenses/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'expenses/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# --- Expense Management Views ---
@login_required
def dashboard_view(request):
    today = date.today()
    current_month_start = today.replace(day=1)
    last_day_of_month = calendar.monthrange(today.year, today.month)[1]
    current_month_end = today.replace(day=last_day_of_month)

    # Expenses for the current month for the logged-in user
    monthly_expenses = Expense.objects.filter(
        user=request.user,
        date__gte=current_month_start,
        date__lte=current_month_end
    ).order_by('-date') # Order for display on dashboard

    total_spent_this_month = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0.00

    # Category breakdown
    category_breakdown = list(monthly_expenses.values('category').annotate(total=Sum('amount')).order_by('-total'))

    context = {
        'total_spent_this_month': total_spent_this_month,
        'category_breakdown': category_breakdown,
        'monthly_expenses': monthly_expenses,
    }
    return render(request, 'expenses/dashboard.html', context)

@login_required
def expense_list_view(request): # This view is optional if dashboard shows all
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def add_expense_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user # Assign the logged-in user to the expense
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_edit_expense.html', {'form': form, 'page_title': 'Add Expense'})

@login_required
def edit_expense_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user) # Ensure user owns the expense
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/add_edit_expense.html', {'form': form, 'page_title': 'Edit Expense'})

@login_required
def delete_expense_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user) # Ensure user owns the expense
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    return render(request, 'expenses/confirm_delete.html', {'expense': expense})

# --- Admin View ---
@staff_member_required # Decorator to restrict access to staff members (is_staff=True)
def admin_dashboard_view(request):
    all_users = User.objects.all().order_by('username')
    all_expenses = Expense.objects.all().select_related('user').order_by('-date') # Fetch all expenses with related user data
    context = {
        'all_users': all_users,
        'all_expenses': all_expenses,
    }
    return render(request, 'expenses/admin_dashboard.html', context)