from django.urls import path

from chat.views import UserChatView

urlpatterns = [
    path('', UserChatView.as_view(), name='chat'),
]
