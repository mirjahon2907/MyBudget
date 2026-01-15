from django.urls import path
from .views import (DashboardView, SettingsView, AnalyticsView, 
                    Operation_createView, OperationsView, AccountsView,
                    NewWalletView, ExpensesAddView)


app_name = 'finance'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard' ),
    path('settings/', SettingsView.as_view(), name='settings' ),
    path('analytics/', AnalyticsView.as_view(), name='analytics' ),
    path('accounts/', AccountsView.as_view(),name='accounts'),
    path('accounts/new_wallet/', NewWalletView.as_view(),name='new_wallet'),
    path('operations/', OperationsView.as_view(), name='operations' ),
    path('operation_create/', Operation_createView.as_view(), name='operation_create' ),
    path('expences/add', ExpensesAddView.as_view(), name='add-expense' ),
]