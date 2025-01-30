from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('tg/auth/profile/', TgAuthProfileView.as_view()),
    path('tg/auth/home', TgAuthHomeView.as_view()),
    re_path(r'^profile/photo/(?P<file_path>photos/[^/]+)$', TgAuthProfilePhotoView.as_view(),
            name='profile_photo'),
    path('logout/', TgAuthLogoutView.as_view(), name='logout'),
    path('api/telegram/login/', TgAuthTelegramLoginView.as_view(), name='telegram_login'),
    path('api/telegram/check-auth-status/', check_auth_status, name='check_auth_status'),
    path('auth/telegram/complete/', TgAuthTelegramCompleteView.as_view(), name='telegram_complete'),
]