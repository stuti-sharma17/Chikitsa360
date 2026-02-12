from django.urls import path

from .views import chatbot_page, chatbot_reply

app_name = "chatbot"

urlpatterns = [
    path("", chatbot_page, name="chatbot_page"),
    path("get/", chatbot_reply, name="chatbot_reply"),
]
