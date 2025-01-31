from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import WalletApiView, UpdateWalletApiView

router = DefaultRouter()

router.register(r'v1/wallets', WalletApiView, basename='wallets-list')

urlpatterns = [
    path('v1/wallets/<int:pk>/operation/', UpdateWalletApiView.as_view({'patch': 'update',}), name='update_wallets'),
    path('', include(router.urls)),
]
