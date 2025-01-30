from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.views.generic import TemplateView

from .forms import TelegramAuthenticationForm
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_protect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .models import TelegramAuthCode, User
import asyncio
import requests

SESSION_COOKIE_AGE = getattr(settings, 'SESSION_COOKIE_AGE', 60 * 60 * 24 * 7)
try:
    BOT_TOKEN = settings.BOT_TOKEN
    BOT_USERNAME = settings.BOT_USERNAME
except Exception:
    raise 'Необходимо указать в settings.py BOT_TOKEN и BOT_USERNAME'


class TgAuthProfilePhotoView(View):
    def get(self, request, file_path):
        try:
            if not request.session.get('user_id'):
                return HttpResponse(status=401)

            telegram_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            response = requests.get(telegram_url)

            if response.status_code == 200:
                return HttpResponse(
                    response.content,
                    content_type=response.headers.get('Content-Type', 'image/jpeg')
                )
            else:
                return HttpResponse(status=404)
        except Exception as e:
            print(f"Error fetching profile photo: {e}")
            return HttpResponse(status=500)


class TgAuthLogoutView(View):
    def get(self, request):
        request.session.flush()
        logout(request)
        return redirect('home')


class TgAuthTelegramLoginView(APIView):
    def get(self, request):
        auth_record = TelegramAuthCode.objects.create()
        bot_link = f"https://t.me/{BOT_USERNAME}?start={auth_record.auth_code}"
        return Response({
            'auth_url': bot_link,
            'auth_code': str(auth_record.auth_code)
        })


@csrf_protect
def check_auth_status(request):
    auth_code = request.GET.get('auth_code')
    if not auth_code:
        return JsonResponse({'authenticated': False})

    try:
        auth_record = TelegramAuthCode.objects.select_related('user').get(
            auth_code=auth_code,
            is_used=True,
            user__isnull=False
        )

        user = auth_record.user
        authenticated_user = authenticate(request, username=user.username)
        if authenticated_user:
            login(request, authenticated_user)

            request.session['user_id'] = auth_record.user.id
            request.session.set_expiry(SESSION_COOKIE_AGE)

            asyncio.run(delete_old_codes(user.id))

            return JsonResponse({
                'authenticated': True
            })

        return JsonResponse({'authenticated': False})

    except TelegramAuthCode.DoesNotExist:
        return JsonResponse({'authenticated': False})


async def delete_old_codes(user_id):
    try:
        await TelegramAuthCode.objects.filter(user_id=user_id).adelete()
        return True
    except Exception:
        return False


class TgAuthTelegramCompleteView(View):
    def get(self, request):
        if not request.session.get('user_id'):
            return redirect('home')
        return HttpResponseRedirect('/profile/')


def telegram_admin_login(request):
    if request.method == 'POST':
        form = TelegramAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = authenticate(request, username=username)
            if user and user.is_staff:
                login(request, user)
                request.session['user_id'] = user.id
                request.session['is_admin'] = True
                return redirect('admin:index')
    else:
        form = TelegramAuthenticationForm()

    return render(request, 'admin/login.html', {'form': form})


# class TgAuthHomeView(TemplateView):
#     template_name = 'auth_tg/home.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_authenticated'] = self.request.session.get('user_id') is not None
#         return context


# class TgAuthProfileView(TemplateView):
#     template_name = 'auth_tg/profile.html'
#
#     def get(self, request, *args, **kwargs):
#         if not request.session.get('user_id'):
#             return redirect('home')
#
#         try:
#             user = User.objects.get(id=request.session['user_id'])
#             photo_path = user.get_photo_path()
#
#             return render(request, self.template_name, {
#                 'user': user,
#                 'photo_path': photo_path,
#                 'is_authenticated': True
#             })
#         except User.DoesNotExist:
#             del request.session['user_id']
#             return redirect('home')


class BaseTgAuthHomeView(TemplateView):
    template_name = 'auth_tg/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.session.get('user_id') is not None
        return context


class BaseTgAuthProfileView(TemplateView):
    template_name = 'auth_tg/profile.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('home')

        try:
            user = User.objects.get(id=request.session['user_id'])
            photo_path = user.get_photo_path()

            return render(request, self.template_name, {
                'user': user,
                'photo_path': photo_path,
                'is_authenticated': True
            })
        except User.DoesNotExist:
            del request.session['user_id']
            return redirect('home')


class TgAuthHomeView(BaseTgAuthHomeView):
    pass


class TgAuthProfileView(BaseTgAuthProfileView):
    pass