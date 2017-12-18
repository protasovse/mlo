import binascii
import os
import requests
import logging

from django import http
from django.views.generic.base import View
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from apps.svem_system.exceptions import BackendPublicException


logger = logging.getLogger(__name__)


class SocialNetworkLogin(View):
    provider = ''

    def get_email(self, request):
        pass

    def get(self, request):
        try:
            email = self.get_email(request)
            try:
                user = get_user_model().objects.get(email=email)
            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_user(email, binascii.hexlify(os.urandom(6)).decode())
            user.activate()
            login(request, user)
            return http.HttpResponseRedirect('/')
        except Exception as e:
            logger.error(format(e))
            messages.add_message(request, messages.ERROR, 'Не удалось авторизироваться через {0}'.format(self.provider))
            return http.HttpResponseRedirect('/auth/login')


class VK(SocialNetworkLogin):
    provider = 'VK'

    def get_email(self, request):
        res = requests.get('https://oauth.vk.com/access_token', params={
            'client_id': settings.VK_CLIENT_ID,
            'client_secret': settings.VK_CLIENT_SECRET,
            'redirect_uri': settings.VK_REDIRECT_URL,
            'code': request.GET.get('code')
        }).json()
        if 'error' in res.keys():
            raise BackendPublicException(res['error'])
        return res['email']


class FB(SocialNetworkLogin):
    provider = 'Facebook'

    def get_email(self, request):
        if request.GET.get('error_code'):
            raise BackendPublicException(request.GET.get('error_message'))

        res = requests.get('https://graph.facebook.com/v2.11/oauth/access_token', params={
            'client_id': settings.FB_CLIENT_ID,
            'client_secret': settings.FB_CLIENT_SECRET,
            'redirect_uri': settings.FB_REDIRECT_URL,
            'code': request.GET.get('code')
        }).json()

        if 'error' in res.keys():
            raise BackendPublicException(res['error']['message'])

        access_token = res['access_token']
        res = requests.get(
            'https://graph.facebook.com/v2.11/me',
            headers={"Authorization": "Bearer {}".format(access_token)},
            params={'fields': 'email,first_name,last_name'}
        ).json()
        if 'error' in res.keys():
            raise BackendPublicException(res['error']['message'])
        return res['email']
