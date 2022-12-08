from dataclasses import dataclass

from django.contrib.auth import get_user_model

User = get_user_model()


@dataclass
class UserDataClass:
    username: str
    email: str
    id: str = None
    password: str = None

    @classmethod
    def from_instance(cls, user: 'User') -> 'UserDataClass':
        return cls(
            username=user.username,
            email=user.email,
            id=user.pk,
        )


def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    instance = User(username=user_dc.username, email=user_dc.email)
    if user_dc.password is not None:
        instance.set_password(user_dc.password)
    instance.save()
    return UserDataClass.from_instance(instance)
