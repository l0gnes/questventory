from django.db import models
from django.utils import timezone
from django.utils.timezone import now
import datetime

# Model for how transactions are recorded in the database.
class Transaction(models.Model):
    TRANSACTION_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]

    TRANSACTION_CATEGORIES = [
        ('food', 'Food'),
        ('recreation and entertainment', 'Recreation'),
        ('fuel', 'Fuel'),
        ('rent', 'Rent'),
        ('miscellaneous', 'Miscellaneous'),
        ('paycheck', 'Paycheck *For Deposits*'),
        ('other', 'Other *For Deposits*'),
    ]
    
    transaction_type = models.CharField(max_length=12, choices=TRANSACTION_CHOICES)
    transaction_category = models.CharField(max_length=30, choices=TRANSACTION_CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)