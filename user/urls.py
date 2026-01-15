from django.urls import path
from .views import ProfileView, LoginView, SignupView, ForgotPasswordView, ProfileEditView, Qr_codeView, TermsView, PrivacyView, logout_view


app_name = 'user'
urlpatterns = [
    path('login/', LoginView.as_view(),name='login'),
    path('logout/',logout_view, name='logout'),
    path('signup/', SignupView.as_view(),name='signup'),
    path('profile/<str:username>', ProfileView.as_view(),name='profile'),
    path('profile_edit/<str:username>', ProfileEditView.as_view(),name='profile_edit'),
    path('forgotpassword/', ForgotPasswordView.as_view(),name='forgotpassword'),
    path('qr_code/<str:username>', Qr_codeView.as_view(),name='qr_code'),
    path('terms/', TermsView.as_view(),name='terms'),
    path('privacy/', PrivacyView.as_view(),name='privacy'),
]