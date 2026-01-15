from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.views import View
from datetime import timedelta
from django.urls import reverse
from .models import Wallet,Transactions,Category
from .forms import TransactionsAddForm



class DashboardView(LoginRequiredMixin, View):
    def get(self,request):

        wallets = Wallet.objects.filter(user=request.user)
        operations = Transactions.objects.filter(user=request.user)
        categories = Category.objects.filter(user=request.user)

        income = operations.filter(type="income").aggregate(s=Sum("amount"))["s"] or 0
        expense = operations.filter(type="expense").aggregate(s=Sum("amount"))["s"] or 0
        profit = income - expense

        total_balance = sum(w.balance for w in wallets)

        period = request.GET.get('period','day')
        today = timezone.localdate()


        if period == 'week':
            start = today - timedelta(days=6)
        elif period == 'month':
            start = today - timedelta(days=30)
        else:
            period='day'
            start = today
        
        
        tx = Transactions.objects.filter(
            user=request.user,
            created_at__date__gte=start,
            created_at__date__lte=today,
        )

        analyze_income = tx.filter(type="income").aggregate(s=Sum("amount"))["s"] or 0
        analyze_expense = tx.filter(type="expense").aggregate(s=Sum("amount"))["s"] or 0
        analyze_profit = analyze_income - analyze_expense

        rows = (tx.filter(type="expense")
                  .values("category__name")
                  .annotate(total=Sum("amount"))
                  .order_by("-total"))

        total_sum = sum(r["total"] or 0 for r in rows) or 0

        segments = []
        offset = 0
        for r in rows:
            percent = (r["total"] / total_sum * 100) if total_sum else 0
            segments.append({
                "name": r["category__name"],
                "amount": r["total"],
                "percent": round(percent, 2),
                "dasharray": f"{round(percent, 2)} 100",
                "dashoffset": f"-{round(offset, 2)}",
            })
            offset += percent

        other_sum = total_sum - sum(s["amount"] for s in segments)

        return render(request,'dashboard.html', 
                        {
                            "wallets": wallets,
                            'categories':categories, 
                            "total_balance":total_balance, 

                            'profit':profit,
                            'income':income,
                            'expense':expense,

                            "segments": segments[:3],
                            "segments_full": segments,
                            "total_sum": total_sum,
                            "other_sum": other_sum,

                            "period": period,
                            "start": start,
                            "today": today,

                            'analyze_profit':analyze_expense,
                            'analyze_income':analyze_income,
                            'analyze_expense':analyze_profit,
                            }
                        )
    

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
        print("UTC now:", timezone.now())
        print("Local now:", timezone.localtime())

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



class NewWalletView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'new_wallet.html')
    
    def post(self, request):
        name = (request.POST.get("title") or "").strip()
        type_p = (request.POST.get("type") or "card").strip().lower()
        balance_raw = (request.POST.get("balance") or "0").strip()

        if not name:
            return render(request, "new_wallet.html", {
                "error": "Название счета обязательно."
            })

        allowed_types = {"cash", "card", "e-wallet",'Savings'}
        if type_p not in allowed_types:
            type_p = "card"

        try:
            balance = Decimal(balance_raw)
        except (InvalidOperation, ValueError):
            balance = Decimal("0.00")

        Wallet.objects.create(
            owner=request.user,
            name=name,
            type=type_p,
            balance=balance
        )

        return redirect(reverse("finance:accounts"))

    

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

            amount = Decimal(request.POST.get("amount", 0))
            if amount <= 0:
                messages.error(request, "Сумма должна быть больше нуля")
                return redirect("finance:add-expense")

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
                messages.warning(request, "Недостаточно средств.")
        
        return render(request, 'expense_add.html', {'accounts':accounts,'category':category})
        

class IncomeAddView(View):
    def get(self, request):
        accounts = Wallet.objects.filter(user=request.user)
        category = Category.objects.all()
        return render(request, 'income_add.html', {'accounts':accounts,'category':category})
    
    def post(self,request):
        accounts = Wallet.objects.filter(user=request.user)
        category = Category.objects.filter(user=request.user, type='income')

        form = TransactionsAddForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            amount = Decimal(request.POST.get("amount", 0))
            if amount <= 0:
                messages.error(request, "Сумма должна быть больше нуля")
                return redirect("finance:add-income")

            income = obj.amount
            this_wallet = obj.wallet

            if income < 100000000:
                this_wallet.balance+=income
                this_wallet.save()

                obj.user = request.user      
                obj.type = "income"         
                obj.save()
                return redirect('finance:dashboard')
            else:
                messages.warning(request, "Сумма не должна превышать 100 000 000 сум.")                
        
        return render(request, 'income_add.html', {'accounts':accounts,'category':category})   