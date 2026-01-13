from django.db import models
from accounts.models import CustomUser


class Wallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wallets')
    name = models.CharField(max_length=50)  # Cash, Card
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    

    def __str__(self):
        return self.name


class Category(models.Model):
    EXPENSE = 'expense'
    INCOME = 'income'

    TYPE_CHOICES = (
        (EXPENSE, 'Expense'),
        (INCOME, 'Income'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=30)   # cafe, food, car
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name


class Transactions(models.Model):
    EXPENSE = 'expense'
    INCOME = 'income'

    TYPE_CHOICES = (
        (EXPENSE, 'Expense'),
        (INCOME, 'Income'),
    )

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)

    amount = models.DecimalField(max_digits=12,decimal_places=2)
    type = models.CharField(max_length=10,choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.amount} {self.type}'