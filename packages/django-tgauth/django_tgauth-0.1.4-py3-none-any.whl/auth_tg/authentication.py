from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class TelegramAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            return user
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(tg_id=username)
                return user
            except (UserModel.DoesNotExist, ValueError):
                return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None