from django.shortcuts import render
from django.views import View
from .models import Wallet,Transactions,Category

# Create your views here.
class HomeView(View):
    def get(self,request):
        wallets = Wallet.objects.all()
        transactions = Transactions.objects.all()
        categories = Category.objects.all()
        return render(request,'home.html', {"wallets":wallets, 'transactions':transactions,'category':categories})
    
class SettingsView(View):
    def get(self,request):
        return render(request,'settings.html')
    

class AnalyticsView(View):
    def get(self,request):
        return render(request,'analytics.html')
    

class Operation_createView(View):
    def get(self,request):
        return render(request,'operation_create.html')
    

class OperationsView(View):
    def get(self,request):
        return render(request,'operations.html')