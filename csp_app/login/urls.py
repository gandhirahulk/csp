from django.urls import path
from . import views

urlpatterns = [path('', views.csp_login, name='login'),
               path('logout/', views.csp_logout, name='csp_logout'),
               path('notlogin/', views.notlogin, name='notlogin'),
               path('csp_admin/', views.admin, name='admin'),
               path('confirm_otp/', views.check_otp, name='check_otp'),
               path('confirm_otp/resend/', views.resend_otp, name='resend_otp'),
               path('login/send_otp', views.send_otp, name='send_otp'), ]
