from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import *

from sheduler_app.services import UserDataClass, create_user
from sheduler_app.models import Client, OperatorCode

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user_dc = UserDataClass(**validated_data)
        return create_user(user_dc)

    def validate_password(self, attrs):
        if len(attrs) < 8:
            raise ValidationError("Password is less 8 letters")
        return attrs

class CodeKeyRelatedField(RelatedField):
    def to_internal_value(self, data):
        print(data)
        return OperatorCode.objects.all().first()

    def to_representation(self, value):
        return value.code

class ClientSerializer(ModelSerializer):

    code = CodeKeyRelatedField(many=False, queryset=OperatorCode.objects.all())

    class Meta:
        model = Client
        fields = ('phone_number', 'code', 'timezone')
