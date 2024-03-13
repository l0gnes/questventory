# Generated by Django 5.0.2 on 2024-03-06 23:14

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')], max_length=12)),
                ('transaction_category', models.CharField(choices=[('food', 'Food'), ('recreation and entertainment', 'Recreation'), ('fuel', 'Fuel'), ('rent', 'Rent'), ('miscellaneous', 'Miscellaneous'), ('paycheck', 'Paycheck *For Deposits*'), ('other', 'Other *For Deposits*')], max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]