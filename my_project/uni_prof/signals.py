from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from reviews.models import Review


@receiver([post_save, post_delete], sender=Review)
def auto_update_rating(sender, instance, **kwargs):
    professors = instance.course.professors.all()
    for prof in professors:
        prof.update_rating()
