from django.urls import path
from .views import index, notification_list,signup,user_login,mark_notification_as_read,notification_details


urlpatterns = [
    path('', index, name='index'),
    path('notifications/', notification_list, name='notifications'),
    path('mark_notification_as_read/', mark_notification_as_read, name='mark_notification_as_read'),
    path('notification/<int:notification_id>/', notification_details, name='notification_details'),
    path('signup/', signup, name='signup'),
    path('login/',user_login, name='login'),
]
