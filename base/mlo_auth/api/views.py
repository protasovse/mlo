from django.contrib.auth import get_user_model
from rest_framework import viewsets

from base.mlo_auth.api.permissions import IsStaffOrReadOnly
from base.mlo_auth.api.serializers import UserSerializer

USER_MODEL = get_user_model()


class UserViewSet(viewsets.ModelViewSet):

    queryset = USER_MODEL.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsStaffOrReadOnly, )
