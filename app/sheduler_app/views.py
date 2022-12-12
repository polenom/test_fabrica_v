from django.contrib.auth import get_user_model
from rest_framework import mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from sheduler_app.serializer import UserSerializer, ClientSerializer

from sheduler_app.permissions import UserPermission

from sheduler_app.models import Client

User = get_user_model()


class RegisterUser(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission, ]
    lookup_field = 'username'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        refresh_token = RefreshToken.for_user(serializer.instance)
        return Response({**serializer.data,
                         'refresh': str(refresh_token),
                         'access': str(refresh_token.access_token)
                         },
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class ClientCRUD(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def update(self, request, *args, **kwargs):
        return super(ClientCRUD, self).update(request, *args, **kwargs)

