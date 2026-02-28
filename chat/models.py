from django.db import models
from django.conf import settings
from marketplace.models import Product


class ChatRoom(models.Model):
    """
    A conversation thread between a buyer and seller
    about a specific product listing.
    One room is created per (buyer + product) pair.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='chat_rooms'
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_rooms_as_buyer'
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_rooms_as_seller'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Each buyer can only have ONE chat room per product
        unique_together = ('product', 'buyer')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.buyer.username} ↔ {self.seller.username} | {self.product.title}"

    def get_other_user(self, current_user):
        """Returns the other participant in the conversation."""
        if current_user == self.buyer:
            return self.seller
        return self.buyer

    def get_last_message(self):
        """Returns the most recent message in this room."""
        return self.messages.order_by('-created_at').first()

    def get_unread_count(self, user):
        """Returns count of unread messages for the given user."""
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    """
    A single message within a ChatRoom.
    """
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.body[:50]}"