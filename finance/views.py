from django.shortcuts import render
from django.views import View
from .models import Wallet,Transactions,Category

# Create your views here.
class DashboardView(View):
    def get(self,request):
        wallets = Wallet.objects.all()
        transactions = Transactions.objects.all()
        categories = Category.objects.all()
        return render(request,'dashboard.html', {"wallets":wallets, 'transactions':transactions,'category':categories})
    

class AccountsView(View):
    def get(self,request):
        return render(request,'accounts.html')


class SettingsView(View):
    def get(self,request):
        return render(request,'settings.html')
    

class AnalyticsView(View):
    def get(self,request):
        return render(request,'analytics.html')
    

class OperationsView(View):
    def get(self,request):
        return render(request,'operations.html')


class Operation_createView(View):
    def get(self,request):
        return render(request,'operation_create.html')
    
