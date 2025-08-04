from django.db import models
from django.contrib.auth.models import User # Django's built-in User model

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100) # You could make this a ForeignKey to a separate Category model for better data consistency
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.user.username})"

    class Meta:
        ordering = ['-date'] # Order expenses by most recent first