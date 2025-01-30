from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, TelegramAuthCode


class AuthTgUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'tg_id', 'tg_username', 'tg_firstname', 'tg_lastname')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password1', None)
        self.fields.pop('password2', None)


class AuthTgUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'tg_id', 'tg_username', 'tg_firstname', 'tg_lastname',
                  'tg_photo', 'is_active', 'is_staff', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)


class AuthTgUserAdmin(UserAdmin):
    form = AuthTgUserChangeForm
    add_form = AuthTgUserCreationForm

    list_display = ('username', 'tg_id', 'tg_username', 'tg_firstname',
                    'tg_lastname', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'created_at')
    search_fields = ('username', 'tg_username', 'tg_firstname', 'tg_lastname', 'tg_id')
    ordering = ('-created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'tg_id')
        }),
        ('Telegram информация', {
            'fields': ('tg_username', 'tg_firstname', 'tg_lastname', 'tg_photo')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {
            'fields': ('created_at', 'last_login'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'tg_id', 'tg_username', 'tg_firstname', 'tg_lastname',
                       'is_staff', 'is_superuser', 'is_active'),
        }),
    )

    readonly_fields = ('created_at', 'last_login',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('tg_id',)
        return self.readonly_fields


class TelegramAuthCodeAdmin(admin.ModelAdmin):
    list_display = ('auth_code', 'created_at', 'is_used', 'user')
    list_filter = ('is_used', 'created_at')
    search_fields = ('auth_code', 'user__username', 'user__tg_username')
    readonly_fields = ('auth_code', 'created_at')

    fieldsets = (
        (None, {
            'fields': ('auth_code', 'user', 'is_used', 'created_at')
        }),
    )


admin.site.register(User, AuthTgUserAdmin)
admin.site.register(TelegramAuthCode, TelegramAuthCodeAdmin)