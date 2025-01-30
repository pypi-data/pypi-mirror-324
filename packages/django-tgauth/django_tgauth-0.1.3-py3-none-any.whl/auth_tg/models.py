from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid
from auth_tg.user_manager import AuthTgUserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, null=True, blank=True, unique=True)
    tg_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    tg_username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Telegram Username")
    tg_firstname = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя")
    tg_lastname = models.CharField(max_length=255, blank=True, null=True, verbose_name="Фамилия")
    tg_photo = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL фото")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Время регистрации")

    is_staff = models.BooleanField(
        default=False,
        verbose_name="Staff status",
        help_text="Designates whether the user can log into this admin site."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Designates whether this user should be treated as active."
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Superuser status",
        help_text="Designates that this user has all permissions without explicitly assigning them."
    )

    objects = AuthTgUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Telegram пользователь"
        verbose_name_plural = "Telegram пользователи"
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return f"{self.tg_firstname} {self.tg_lastname} ({self.tg_username})"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.tg_username if self.tg_username else str(self.tg_id)
        super().save(*args, **kwargs)

    def get_photo_path(self):
        if not self.tg_photo:
            return None
        try:
            if '/photos/' in self.tg_photo:
                return 'photos/' + self.tg_photo.split('/photos/')[-1]
            return None
        except Exception:
            return None

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        if self.is_staff:
            return True
        return False

    def has_module_perms(self, app_label):
        return True if self.is_superuser else False

    def check_password(self, raw_password):
        return True

    def set_password(self, raw_password):
        pass


class TelegramAuthCode(models.Model):
    auth_code = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)