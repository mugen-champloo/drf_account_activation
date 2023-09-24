from django.urls import path

from applications.account.views import *

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationApiView.as_view()),
    path('users/', QuerysetAPI.as_view())
]