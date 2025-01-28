from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from reviews.models import Review


@receiver([post_save, post_delete], sender=Review)
def auto_update_rating(sender, instance, **kwargs):
    instance.course.update_rating()