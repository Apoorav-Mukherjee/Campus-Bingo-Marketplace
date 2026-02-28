from django.contrib import admin
from .models import ChatRoom, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['sender', 'body', 'is_read', 'created_at']


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['product', 'buyer', 'seller', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['buyer__email', 'seller__email', 'product__title']
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'sender', 'body', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__email', 'body']