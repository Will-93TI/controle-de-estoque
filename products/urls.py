from django.urls import path
from . import views
from .views import product_output, stock_report

urlpatterns = [
    path('', views.menu, name='menu'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/output/', product_output, name='product_output'),
    path('stock/report/', stock_report, name='stock_report'),
]
