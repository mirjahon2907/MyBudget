from django.shortcuts import render
from django.views import View
# Create your views here.

class AccountView(View):
    def get(self,request):
        return render(request,'accounts.html')

class ProfileView(View):
    def get(self,request):
        return render(request,'profile.html')
