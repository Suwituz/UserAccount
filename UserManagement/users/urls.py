from django.urls import path
from .views import signup
from .views import user_list
from .views import login_view
from .views import home
# from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm
from .views import CustomPasswordResetDoneView,reset_password,CustomPasswordResetDoneView,MyPasswordResetConfirmView,account_verification,verification_success
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'users'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('user-list/', user_list, name='user_list'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('password-reset/', reset_password, name='password_reset'),
    path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('account-verification/', account_verification, name='account_verification'),
    path('verification_success/', verification_success, name='verification_success'),
]