from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('dang-ky/', views.register_view, name='register'),
    path('dang-nhap/', views.login_view, name='login'),
    path('dang-xuat/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    # path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    # path('profile/delete/', views.delete_account_view, name='delete_account'),
    
    path('ajax/password-reset/', views.ajax_password_reset_view, name='ajax_password_reset'),
    path('ajax/update-avatar/', views.ajax_update_avatar, name='ajax_update_avatar'),
    path('ajax/update-profile/', views.ajax_update_profile, name='ajax_update_profile'),
    path('ajax/delete-account/', views.ajax_delete_account, name='ajax_delete_account'),
    
    # Thêm reset password
    path(
        'reset-password/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            success_url=reverse_lazy('users:password_reset_done')  # ✅ fix lỗi
        ),
        name='password_reset'
    ),
    path(
        'reset-password-confirm/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path(
        'reset-password-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

   # ✅ QUẢN LÝ USER (staff)
    path('control/users/', views.manage_users_view, name='manage_users'),
    path('control/users/<int:user_id>/toggle-active/', views.toggle_active, name='toggle_active'),
    path('control/users/<int:user_id>/set_premium/', views.set_premium, name='set_premium'),
    path('control/users/<int:user_id>/remove_premium/', views.remove_premium, name='remove_premium'),
]
