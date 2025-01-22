from django.urls import path
from .views import DoorStatusView, AccessHistoryView, ScheduleView, UpdateDoorStatusView

urlpatterns = [
    path('status/', DoorStatusView.as_view(), name='door_status'),
    path('history/', AccessHistoryView.as_view(), name='access_history'),
    path('schedule/', ScheduleView.as_view(), name='door_schedule'),
    path('update-status/', UpdateDoorStatusView.as_view(), name='update_door_status'),
]
