from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Inbox — all conversations
    path('', views.InboxView.as_view(), name='inbox'),

    # Start or resume a chat from a product page
    path('start/<int:product_pk>/', views.start_chat, name='start_chat'),

    # Chat room — read and send messages
    path('room/<int:room_pk>/', views.ChatRoomView.as_view(), name='chat_room'),
]