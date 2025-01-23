from django.urls import path, re_path

from .views import send_confirmation_email, activate_account

urlpatterns = [
    path('send_confirmation_email', send_confirmation_email, name='confirmation_email'),
    path('activate/<uidb64>/<token>', activate_account, name='activate')
]

