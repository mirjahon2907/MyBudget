from django.urls import path
from .views import AccountsView,ProfileView, LoginView, SignupView, ForgotPasswordView, ProfileEditView, Qr_codeView


app_name = 'accounts'
urlpatterns = [
    path('', AccountsView.as_view(),name='accounts'),
    path('login/', LoginView.as_view(),name='login'),
    path('signup/', SignupView.as_view(),name='signup'),
    path('profile/<str:username>', ProfileView.as_view(),name='profile'),
    path('profile_edit/<str:username>', ProfileEditView.as_view(),name='profile_edit'),
    path('forgotpassword/', ForgotPasswordView.as_view(),name='forgotpassword'),
    path('qr_code/<str:username>', Qr_codeView.as_view(),name='qr_code'),
]