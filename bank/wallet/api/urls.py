from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import WalletApiView, UpdateWalletApiView

app_name = 'wallets'

router = DefaultRouter()

router.register(r'v1/wallets', WalletApiView, basename='wallets')

urlpatterns = [
    path('v1/wallets/<int:pk>/operation/', UpdateWalletApiView.as_view({'patch': 'update',}), name='wallet_operation'),
    path('', include(router.urls)),
]
