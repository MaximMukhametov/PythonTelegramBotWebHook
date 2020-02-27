from django.urls import path
from .views import UpdateBot
app_name = 'bot'
urlpatterns = [

    path('telegram', UpdateBot.as_view(), name='update'),
]

