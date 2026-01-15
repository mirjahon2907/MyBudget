from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.contrib import messages
from .models import Wallet,Transactions,Category
from .forms import TransactionsAddForm

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    def get(self,request):
        wallets = Wallet.objects.all()
        transactions = Transactions.objects.all()
        categories = Category.objects.all()

        total_money = 0
        for wallet in wallets:
            total_money+=wallet.balance

        return render(request,'dashboard.html', {"wallets":wallets, 'transactions':transactions,'category':categories, "total_money":total_money})
    

class AccountsView(LoginRequiredMixin,View):
    def get(self,request):
        accounts = Wallet.objects.filter(user=request.user)
        return render(request,'accounts.html',{'accounts':accounts})


class SettingsView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'settings.html')


class AnalyticsView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'analytics.html')
    

class OperationsView(LoginRequiredMixin, View):
    def get(self, request):
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)

        cat_id = request.GET.get("cat")  # URLdan keladi

        operations = Transactions.objects.filter(user=request.user).select_related("category", "wallet").order_by("-created_at")

        if cat_id:
            operations = operations.filter(category_id=cat_id)

        income = operations.filter(type="income").aggregate(s=Sum("amount"))["s"] or 0
        expense = operations.filter(type="expense").aggregate(s=Sum("amount"))["s"] or 0
        profit = income - expense

        categories = Category.objects.filter(user=request.user)

        return render(request, "operations.html", {
            "operations": operations,
            "categories": categories,
            "today": today,
            "yesterday": yesterday,
            "income": income,
            "expense": expense,
            "profit": profit,
            "active_cat": int(cat_id) if cat_id else None,
        })


class Operation_createView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'operation_create.html')
    


class NewWalletView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'new_wallet.html')
    

class ExpensesAddView(View):
    def get(self, request):
        accounts = Wallet.objects.filter(user=request.user)
        category = Category.objects.all()
        return render(request, 'expense_add.html', {'accounts':accounts,'category':category})
    
    def post(self,request):
        accounts = Wallet.objects.filter(user=request.user)
        category = Category.objects.filter(user=request.user, type='expense')

        form = TransactionsAddForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            expense = obj.amount
            this_wallet = obj.wallet

            if expense < this_wallet.balance:
                this_wallet.balance-=expense
                this_wallet.save()

                obj.user = request.user      
                obj.type = "expense"         
                obj.save()
                return redirect('finance:dashboard')
            else:
                messages.warning(request, "Maglag' yetarli emas")
                print("Maglag' yetarli emas!!!!!!!!!!!!!")
        
        return render(request, 'expense_add.html', {'accounts':accounts,'category':category})
        