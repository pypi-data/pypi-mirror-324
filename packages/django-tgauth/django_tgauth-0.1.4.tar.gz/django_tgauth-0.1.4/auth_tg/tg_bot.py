import time
import uuid
from datetime import timedelta
from django.utils import timezone
import telebot
from telebot import types
from django.conf import settings
from auth_tg.models import TelegramAuthCode, User


channels = getattr(settings, 'CHANNELS', None)
channels = [int(channel) for channel in channels.split(',')] if channels else []

channel_links = getattr(settings, 'CHANNEL_NAMES', None)
channel_links = [channel for channel in channel_links.split(',')] if channel_links else []
try:
    BOT_TOKEN = settings.BOT_TOKEN
    BOT_USERNAME = settings.BOT_USERNAME
except Exception:
    raise 'Необходимо указать в settings.py BOT_TOKEN и BOT_USERNAME'
class DjangoTelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot(BOT_TOKEN)
        self.setup_handlers()

    def auth_bot(self):
        try:
            print("Бот запущен и ожидает сообщений...")
            self.bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(f"Ошибка в работе бота: {e}")
            time.sleep(15)
            self.auth_bot()

    def check_subscribe(self, user_id):
        if not channels or not channel_links:
            return True

        result = []
        for channel in channels:
            try:
                member_status = self.bot.get_chat_member(channel, user_id).status
                result.append(member_status in ['member', 'administrator', 'creator'])
            except telebot.apihelper.ApiException as e:
                print(f"Ошибка при проверке подписки: {e}")
                continue
        return all(result) if result else True

    def create_subscription_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        if channel_links:
            for link in channel_links:
                button = types.InlineKeyboardButton(
                    text=f"Подписаться на {link}",
                    url=f"https://t.me/{link[1:]}"
                )
                keyboard.add(button)
            check_button = types.InlineKeyboardButton(
                text="✅ Я подписался",
                callback_data="check_subscription"
            )
            keyboard.add(check_button)
        return keyboard

    def setup_handlers(self):
        @self.bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
        def callback_check_subscription(call):
            if self.check_subscribe(call.from_user.id):
                try:
                    auth_record = TelegramAuthCode.objects.filter(
                        user__tg_id=call.from_user.id,
                        is_used=False,
                        created_at__gte=timezone.now() - timedelta(minutes=30)
                    ).latest('created_at')

                    auth_record.is_used = True
                    auth_record.save()

                    self.bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                        text="✅ Авторизация успешна! Можете вернуться на сайт."
                    )
                except TelegramAuthCode.DoesNotExist:
                    self.bot.answer_callback_query(
                        call.id,
                        "Ошибка авторизации. Попробуйте начать сначала.",
                        show_alert=True
                    )
            else:
                self.bot.answer_callback_query(
                    call.id,
                    "Вы не подписались на все каналы!",
                    show_alert=True
                )

        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            try:
                command_args = message.text.split()
                if len(command_args) != 2:
                    self.bot.reply_to(
                        message,
                        "Для аутентификации используйте специальную ссылку с сайта."
                    )
                    return

                auth_uuid = command_args[1]
                try:
                    uuid_obj = uuid.UUID(auth_uuid)
                except ValueError:
                    self.bot.reply_to(
                        message,
                        "Неверный формат идентификатора аутентификации."
                    )
                    return

                try:
                    auth_record = TelegramAuthCode.objects.get(
                        auth_code=uuid_obj,
                        is_used=False,
                        created_at__gte=timezone.now() - timedelta(minutes=30)
                    )
                except TelegramAuthCode.DoesNotExist:
                    self.bot.reply_to(
                        message,
                        "Код аутентификации недействителен или устарел."
                    )
                    return

                user = message.from_user

                try:
                    photo_url = None
                    try:
                        user_profile_photos = self.bot.get_user_profile_photos(user.id)
                        if user_profile_photos.total_count > 0:
                            file_info = self.bot.get_file(user_profile_photos.photos[0][-1].file_id)
                            photo_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
                    except Exception as photo_error:
                        print(f"Ошибка при получении фото профиля: {photo_error}")

                    tg_user, created = User.objects.update_or_create(
                        tg_id=user.id,
                        defaults={
                            'tg_username': user.username or '',
                            'tg_firstname': user.first_name or '',
                            'tg_lastname': user.last_name or '',
                            'tg_photo': photo_url or '',
                            'username': user.username or str(user.id),
                            'is_active': True
                        }
                    )

                    auth_record.user = tg_user
                    auth_record.save()

                    if channels and channel_links and not self.check_subscribe(user.id):
                        keyboard = self.create_subscription_keyboard()
                        self.bot.reply_to(
                            message,
                            "Для продолжения необходимо подписаться на каналы:",
                            reply_markup=keyboard
                        )
                        return

                    auth_record.is_used = True
                    auth_record.save()

                    self.bot.reply_to(
                        message,
                        "✅ Авторизация успешна! Можете вернуться на сайт."
                    )

                except Exception as db_error:
                    print(f"Ошибка при работе с базой данных: {db_error}")
                    self.bot.reply_to(
                        message,
                        "❌ Произошла ошибка при сохранении данных. Пожалуйста, попробуйте позже."
                    )

            except Exception as e:
                print(f"Неожиданная ошибка: {e}")
                self.bot.reply_to(
                    message,
                    "❌ Произошла ошибка при аутентификации. Пожалуйста, попробуйте позже."
                )

        @self.bot.message_handler(func=lambda message: True)
        def handle_unknown(message):
            self.bot.reply_to(
                message,
                "Для аутентификации используйте специальную ссылку с сайта."
            )


def run_telegram_bot():
    try:
        bot = DjangoTelegramBot()
        bot.auth_bot()
    except Exception as e:
        print(f"Критическая ошибка при запуске бота: {e}")


if __name__ == '__main__':
    run_telegram_bot()