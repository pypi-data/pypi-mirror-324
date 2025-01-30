from django.core.management.base import BaseCommand
from auth_tg.tg_bot import DjangoTelegramBot

class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Бот запущен...'))
        bot = DjangoTelegramBot()
        bot.auth_bot()
        self.stdout.write(self.style.SUCCESS('Бот выключен'))

