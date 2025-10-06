from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('api/chat/', chatbot_agent, name='agent-graph'),
    path('api/news/', news, name='news'),

    # path('chatbot-response', chatbot_response, name='chatbot_response'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)