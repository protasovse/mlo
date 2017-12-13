from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.reverse import reverse

from apps.mlo_auth.models import ROLES_CHOICES

USER_MODEL = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    api_url = HyperlinkedIdentityField(
        view_name='users-api:user-detail',
        lookup_field='pk',
    )
    '''url = HyperlinkedIdentityField(
        view_name='users:user-detail',
        lookup_field='pk',
    )'''

    class Meta:
        model = USER_MODEL
        fields = (
            'api_url',
            # 'url',
            'id',
            'first_name',
            'last_name',
            'patronymic',
            'role'
        )

    @staticmethod
    def get_url(obj):
        return reverse('users-api:user-detail', kwargs={'pk': obj.pk})


class UserDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = USER_MODEL
        fields = ('email', 'first_name', 'last_name', 'patronymic', 'role')
