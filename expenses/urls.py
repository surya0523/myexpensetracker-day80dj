from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'), # Default landing page after login
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('expenses/add/', views.add_expense_view, name='add_expense'),
    path('expenses/edit/<int:pk>/', views.edit_expense_view, name='edit_expense'),
    path('expenses/delete/<int:pk>/', views.delete_expense_view, name='delete_expense'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'), # Custom admin view
]