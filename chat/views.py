from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.http import Http404
from django.db.models import Q

from .models import ChatRoom, Message
from marketplace.models import Product


# ─────────────────────────────────────────────
# Start or Resume a Chat
# ─────────────────────────────────────────────

@login_required
def start_chat(request, product_pk):
    """
    Creates a new ChatRoom or retrieves an existing one
    when a buyer clicks 'Message Seller' on a product page.
    Prevents sellers from chatting with themselves.
    """
    product = get_object_or_404(Product, pk=product_pk, is_active=True)

    # Seller cannot initiate a chat on their own listing
    if request.user == product.seller:
        messages.warning(request, "You cannot message yourself on your own listing.")
        return redirect('marketplace:product_detail', pk=product_pk)

    # Get or create a unique chat room for this buyer + product pair
    room, created = ChatRoom.objects.get_or_create(
        product=product,
        buyer=request.user,
        defaults={'seller': product.seller}
    )

    if created:
        messages.info(request, f"Chat started with {product.seller.get_full_name()}!")

    return redirect('chat:chat_room', room_pk=room.pk)


# ─────────────────────────────────────────────
# Chat Room View
# ─────────────────────────────────────────────

@method_decorator(login_required, name='dispatch')
class ChatRoomView(View):
    """
    Displays all messages in a chat room and handles
    sending new messages. Only the buyer and seller
    of that specific room can access it.
    """
    template_name = 'chat/chat_room.html'

    def get_room(self, room_pk, user):
        """Fetch room and verify the user is a participant."""
        room = get_object_or_404(ChatRoom, pk=room_pk)
        if user != room.buyer and user != room.seller:
            raise Http404("You do not have access to this conversation.")
        return room

    def get(self, request, room_pk):
        room = self.get_room(room_pk, request.user)

        # Mark all messages from the OTHER user as read
        room.messages.filter(
            is_read=False
        ).exclude(sender=request.user).update(is_read=True)

        chat_messages = room.messages.select_related('sender').all()
        other_user = room.get_other_user(request.user)

        context = {
            'room': room,
            'chat_messages': chat_messages,
            'other_user': other_user,
            'product': room.product,
        }
        return render(request, self.template_name, context)

    def post(self, request, room_pk):
        room = self.get_room(room_pk, request.user)
        body = request.POST.get('body', '').strip()

        if body:
            Message.objects.create(
                room=room,
                sender=request.user,
                body=body
            )
            # Bump the room's updated_at so it appears at top of inbox
            room.save()
        else:
            messages.warning(request, "Cannot send an empty message.")

        return redirect('chat:chat_room', room_pk=room.pk)


# ─────────────────────────────────────────────
# Inbox View
# ─────────────────────────────────────────────

@method_decorator(login_required, name='dispatch')
class InboxView(View):
    """
    Shows all chat conversations for the logged-in user —
    both as a buyer and as a seller.
    """
    template_name = 'chat/inbox.html'

    def get(self, request):
        user = request.user

        # Get all rooms where the user is either buyer or seller
        rooms = ChatRoom.objects.filter(
            Q(buyer=user) | Q(seller=user)
        ).select_related(
            'buyer', 'seller', 'product'
        ).prefetch_related(
            'messages', 'product__images'
        ).order_by('-updated_at')

        # Annotate each room with unread count for template use
        rooms_data = []
        total_unread = 0
        for room in rooms:
            unread = room.get_unread_count(user)
            total_unread += unread
            rooms_data.append({
                'room': room,
                'other_user': room.get_other_user(user),
                'last_message': room.get_last_message(),
                'unread_count': unread,
            })

        context = {
            'rooms_data': rooms_data,
            'total_unread': total_unread,
            'has_conversations': len(rooms_data) > 0,
        }
        return render(request, self.template_name, context)