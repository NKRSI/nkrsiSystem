from django.urls import path, include
from . import views

urlpatterns = [
    path('account/me/password/', views.change_password, name='user-password'),
    path('account/me/', views.view_user, name='user'),
    path('account/<int:user_id>/', views.view_user, name='user-by-id'),
    path('account/me/edit/', views.edit_user, name='user-edit'),
    path('accounts/', views.all_users, name='user-list'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
