from django.db.models import Q


def unread_messages_count(request):
    """
    Global context processor — injects unread message count
    into every template so the navbar badge always stays updated.
    """
    if request.user.is_authenticated:
        try:
            from chat.models import Message
            count = Message.objects.filter(
                room__buyer=request.user,
                is_read=False
            ).exclude(sender=request.user).count()

            count += Message.objects.filter(
                room__seller=request.user,
                is_read=False
            ).exclude(sender=request.user).count()

            return {'unread_messages_count': count}
        except Exception:
            pass
    return {'unread_messages_count': 0}