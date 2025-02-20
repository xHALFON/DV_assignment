"""
URL configuration for ATM_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from ATM_server import settings
from atm.views import welcome, get_balance, deposit, withdraw
from django.conf.urls.static import static

urlpatterns = [
    path('', welcome),
    path('balance/<str:user_id>/', get_balance, name='get_balance'),
    path('deposit/<str:user_id>/', deposit, name='deposit'),
    path('withdraw/<str:user_id>/', withdraw, name='withdraw'),
]
