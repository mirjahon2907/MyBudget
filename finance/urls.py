from django.urls import path
from .views import HomeView, SettingsView, AnalyticsView, Operation_createView, OperationsView


app_name = 'finance'
urlpatterns = [
    path('', HomeView.as_view(), name='home' ),
    path('settings/', SettingsView.as_view(), name='settings' ),
    path('analytics/', AnalyticsView.as_view(), name='analytics' ),
    path('operations/', OperationsView.as_view(), name='operations' ),
    path('operation_create/', Operation_createView.as_view(), name='operation_create' ),
]