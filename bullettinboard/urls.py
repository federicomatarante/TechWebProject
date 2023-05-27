from django.urls import path

from bullettinboard.views import BullettinBoardView, message_delete

urlpatterns = [
    path('', BullettinBoardView.as_view(), name='bullettinboard'),
    path('/delete/<int:id>', message_delete, name='bullettinboard_delete')
]
