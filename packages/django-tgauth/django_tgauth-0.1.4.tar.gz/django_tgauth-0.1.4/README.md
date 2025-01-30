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
3. You can add an additional checking on your telegram channels. Just add these without gap:
```python
CHANNELS = '12345678910,12345678911'
CHANNEL_NAMES = '@channel1,@channel2'
```
4. Add backend and custom user model into settings.py as well:
```python
AUTH_USER_MODEL = 'auth_tg.User'

AUTHENTICATION_BACKENDS = [
    'auth_tg.authentication.TelegramAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```
5. Include the auth_tg URLconf to your project urls.py:
```python
path('auth/', include('auth_tg.urls')),
```
6. You can try out this functional:
    Add new app:
    ```bash
   cd yourproject-name
   ```
   ```bash
   python manage.py startapp yourapp_name
   ```
    Then you need to create urls.py and add this code:
    ```python
    from django.urls import path
    from .views import *
    
    urlpatterns = [
        path('', Home.as_view(), name='home'),
        path('profile/', Profile.as_view(), name='profile')
    ]
    ```
    And add simple views to views.py:
    ```python
    from auth_tg.views import TgAuthProfileView, TgAuthHomeView
    
    class Home(TgAuthHomeView):
        ...
    
    class Profile(TgAuthProfileView):
        ...
    ```
   Don't forget to add your new app to INSTALLED_APPS and URLconf:
    ```python
    INSTALLED_APPS = [
        ...
        'auth_tg',
        'yourapp_name',
    ]
    ```
    ```python
    path('', include('yourapp_name.urls')),
    ```
7. Run migrations:
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
8. If you want to use your own base.html then you need to add this to your html file.
```html
<script src="{% static 'auth_tg/js/telegramAuth.js' %}"></script>
```

