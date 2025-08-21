from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings
from django.apps import apps
from .models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

User = settings.AUTH_USER_MODEL
Post = apps.get_model('posts', 'Post')
Comment = apps.get_model('posts', 'Comment')
Profile = apps.get_model('accounts', 'Profile')

channel_layer = get_channel_layer()

def send_real_time_notification(recipient_pk, payload):
    """
    Helper to send WS notification to recipient group.
    """
    if channel_layer is None:
        return
    group_name = f'notifications_{recipient_pk}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'notify',
            'payload': payload
        }
    )

@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if not created:
        return
    post = instance.post
    actor = instance.author
    recipient = post.author
    # don't notify if author commented on own post
    if actor.pk == recipient.pk:
        return
    notif = Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb='comment',
        post_id=post.pk,
        comment_id=instance.pk
    )
    payload = {
        'id': notif.pk,
        'actor': actor.username,
        'verb': 'comment',
        'post_id': post.pk,
        'comment_id': instance.pk,
        'timestamp': notif.timestamp.isoformat(),
        'is_read': notif.is_read,
        'message': f"{actor.username} commented on your post."
    }
    send_real_time_notification(recipient.pk, payload)

@receiver(m2m_changed, sender=Post.likes.through)
def post_liked(sender, instance, action, pk_set, **kwargs):
    
    if action not in ('post_add', 'post_remove'):
        return
    post = instance
    if action == 'post_add':
        for user_pk in pk_set:
            if user_pk == post.author.pk:
                continue
            actor = apps.get_model(settings.AUTH_USER_MODEL).objects.get(pk=user_pk)
            recipient = post.author
            notif = Notification.objects.create(
                recipient=recipient,
                actor=actor,
                verb='like',
                post_id=post.pk
            )
            payload = {
                'id': notif.pk,
                'actor': actor.username,
                'verb': 'like',
                'post_id': post.pk,
                'timestamp': notif.timestamp.isoformat(),
                'is_read': notif.is_read,
                'message': f"{actor.username} liked your post."
            }
            send_real_time_notification(recipient.pk, payload)
    

@receiver(m2m_changed, sender=Profile.following.through)
def profile_followed(sender, instance, action, pk_set, **kwargs):
    
    if action != 'post_add':
        return
    follower_profile = instance
    follower_user = follower_profile.user
    for target_profile_pk in pk_set:
        try:
            target_profile = Profile.objects.get(pk=target_profile_pk)
        except Profile.DoesNotExist:
            continue
        target_user = target_profile.user
        
        if target_user.pk == follower_user.pk:
            continue
        notif = Notification.objects.create(
            recipient=target_user,
            actor=follower_user,
            verb='follow'
        )
        payload = {
            'id': notif.pk,
            'actor': follower_user.username,
            'verb': 'follow',
            'timestamp': notif.timestamp.isoformat(),
            'is_read': notif.is_read,
            'message': f"{follower_user.username} started following you."
        }
        send_real_time_notification(target_user.pk, payload)
