from django.urls import path, include
from rest_framework.routers import SimpleRouter
from sheduler_app.views import RegisterUser, ClientCRUD
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

router = SimpleRouter()
router.register(r'user', RegisterUser)
router.register(r'client', ClientCRUD)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
]