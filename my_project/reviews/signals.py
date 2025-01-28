from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review
from ai_mod.views import check_review_for_nsfw
import logging

logger = logging.getLogger(__name__)


@receiver([post_save, post_delete], sender=Review)
def on_review_save_delete(sender, instance, **kwargs):
    # Recalculating average rating for associated professors
    professors = instance.course.professors.all()
    for prof in professors:
        prof.update_rating()

    # Only check for NSFW if the signal is 'post_save'
    if kwargs.get('created', False):  # Ensures only on creation
        title_n_body = instance.title + "\n" + instance.body
        check_res = check_review_for_nsfw(title_n_body)
        instance.nsfw_passed = check_res.get('Passed', False)
        try:
            instance.nsfw_score = check_res['nsfw_likelihood_score']
            instance.save(update_fields=['nsfw_score',
                                         'nsfw_passed'])  # Update specific fields to avoid re-triggering other signals
            logger.info("Signal fired: NSFW score updated")
        except KeyError as e:
            logger.error(f"Error retrieving NSFW score for review: {e}")


# Optional: Adjust your Review model to avoid infinite loops and signal re-triggering
def update_review_fields(instance, fields):
    instance.save(update_fields=fields)


@receiver(post_save, sender=Review)
def update_review_post_save(sender, instance, created, **kwargs):
    if not created:
        update_review_fields(instance, ['nsfw_score', 'nsfw_passed'])
