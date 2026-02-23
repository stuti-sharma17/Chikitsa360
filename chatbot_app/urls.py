from django.urls import path

from .views import chatbot_page, chatbot_reply, chatbot_quick_book, ai_booking_converse

app_name = "chatbot"

urlpatterns = [
    path("", chatbot_page, name="chatbot_page"),
    path("get/", chatbot_reply, name="chatbot_reply"),
    path("quick-book/", chatbot_quick_book, name="chatbot_quick_book"),
    path("ai-booking/", ai_booking_converse, name="ai_booking_converse"),
]
