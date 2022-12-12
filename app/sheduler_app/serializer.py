from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import *

from sheduler_app.services import UserDataClass, create_user
from sheduler_app.models import Client, OperatorCode, TagForClient

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
    default_error_messages = {
        'required': 'This field is required.',
        'does_not_exist': 'Invalid code "{code}" - object does not exist.',
        'incorrect_type': 'Incorrect type. Expected code value, received {data_type}.',
    }

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            if not isinstance(data, int):
                raise TypeError
            return queryset.get(code=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', code=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, value):
        return value.code


class ClientTagSerializer(ModelSerializer):
    class Meta:
        model = TagForClient
        fields = ('id', 'name')

    def to_internal_value(self, data):
        errors = OrderedDict()
        validate_method = getattr(self, 'validate_tag', None)
        if validate_method is not None:
            validated_value = validate_method(data)
        return data

    def to_representation(self, instance):
        return instance.name

    def validate_tag(self, attr: str):
        if not isinstance(attr, str) or not attr.startswith('#') or len(attr) == 1:
            raise ValidationError("invalid value")
        return attr


class ClientSerializer(ModelSerializer):
    code = CodeKeyRelatedField(many=False, queryset=OperatorCode.objects.all(), read_only=False)
    tags = ClientTagSerializer(many=True)

    class Meta:
        model = Client
        fields = ('id', 'phone_number', 'code', 'timezone', 'tags')

    def save(self, **kwargs):
        return super().save(**kwargs)

    def is_valid(self, *, raise_exception=False):
        try:
            return super().is_valid(raise_exception=raise_exception)
        except ValidationError as exc:
            if 'tags' in exc.detail:
                exc.detail['tags'] = 'invalid value or values'
            raise ValidationError(exc.detail)

    def validate_tags(self, attr):
        if len(set(attr)) != len(attr):
            raise ValidationError('Non unicue value')
        return attr

    def update(self, instance, validated_data: dict):
        tags = validated_data.pop('tags', None)
        save_instance = super().update(instance, validated_data)
        if tags:

            all_tags_create = []
            all_tags = {i.name: i.id for i in save_instance.tags.all()}
            for tag in tags:
                get_tag = all_tags.pop(tag, None)
                if not get_tag:
                    all_tags_create.append(
                        TagForClient(
                            name=tag,
                            client=save_instance,
                        )
                    )

            TagForClient.objects.bulk_create(all_tags_create)
            TagForClient.objects.filter(pk__in=all_tags.values()).delete()

        return save_instance
