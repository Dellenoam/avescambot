from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('addBot', add_bot),
    path('checkBots', check_bots),
    path('getCommand', get_command),
    path('addCommand', add_command),
    path('delCommand', del_command),
    path('addOtherData', add_other_data),
    path('getOtherData', get_other_data),
]
