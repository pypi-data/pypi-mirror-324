# Django Telegram Authentication

Simple Django app for authentication via Telegram.

## Installation

```bash
pip install django-tgauth
````
## Quick start

1. Add "auth_tg" to your INSTALLED_APPS setting:
```python
INSTALLED_APPS = [
    ...
    'auth_tg',
]
```
2. Add your Telegram Bot settings to settings.py:
```python
BOT_TOKEN = 'your-bot-token'
BOT_USERNAME = 'your-bot-username'
```
3. Include the auth_tg URLconf in your project urls.py:
```python
path('auth/', include('auth_tg.urls')),
```
4. Run migrations:
```bash
python manage.py migrate
```
5. If you want to use your own base.html then you need to add this into your html file.
```html
<script src="{% static 'auth_tg/js/telegramAuth.js' %}"></script>
```
6. You can add an additional checking on your telegram channels. Just add these without gap:
```python
CHANNELS = '12345678910,12345678911'
CHANNEL_NAMES = '@channel1,@channel2'
```
