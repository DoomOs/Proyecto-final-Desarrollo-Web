# board/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Board

@receiver(post_save, sender=User)
def create_user_board(sender, instance, created, **kwargs):
    if created:
        Board.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_board(sender, instance, **kwargs):
    instance.board.save()
