from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from io import BytesIO
import qrcode
import base64
from .forms import SignupForm, UpdateProfileForm
from .models import CustomUser



class AccountsView(View):
    def get(self,request):
        return render(request,'accounts.html')


class ProfileView(View):
    def get(self,request,username):
        user = get_object_or_404(CustomUser, username=username)
        return render(request, 'profile.html',{'custom_user':user})
    

class ProfileEditView(View):
    def get(self,request,username):
        user = get_object_or_404(CustomUser, username=username)
        return render(request, 'profile_edit.html',{'custom_user':user})
    
    def post(self,request,username):
        form = UpdateProfileForm(instance=request.user,data=request.POST)
        user = get_object_or_404(CustomUser, username=username)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user)
        return render(request,'profile_edit.html',{'custom_user':user})


class LoginView(View):
    def get(self,request):
        return render(request,'registration/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("Вы успешно вошли в систему")
            login(request, user)
            messages.success(request, "Вы успешно вошли в систему.")
            return redirect('finance:dashboard')  # o‘zingizga kerakli sahifa
        else:
            messages.error(request, "Неверный логин или пароль.")
            return render(request, 'registration/login.html')


class SignupView(View):
    def get(self,request):
        form = SignupForm()
        return render(request,'registration/signup.html', {'form':form})
    
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect('accounts:login')
        
        return render(request, 'registration/signup.html', {"form":form})
    

class ForgotPasswordView(View):
    def get(self, request):
        return render(request,'registration/forgotpassword.html')
    


class Qr_codeView(View):
    def get(self, request, username=None):
        if username:
            url = request.build_absolute_uri(f'/profile/{username}/')
        else:
            url = request.build_absolute_uri('/')

        # QR code yaratish
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # BytesIO → base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        context = {
            'user_qr': img_base64,
            'username': username or request.user.username,
        }
        return render(request, 'qr_code.html', context)
    