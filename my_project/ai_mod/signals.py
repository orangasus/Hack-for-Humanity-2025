from ai_mod.views import check_review_for_nsfw
from django.db.models.signals import post_save
from django.dispatch import receiver
from reviews.models import Review


@receiver(post_save, sender=Review)
def check_nsfw_review(sender, instance, **kwargs):
    title_n_body = instance.title + "\n" + instance.body

    check_res = check_review_for_nsfw(title_n_body)
    instance.nsfw_passed = check_res.get('Passed', False)
    try:
        instance.nsfw_score = check_res['nsfw_likelihood_score']
        print("Signal fired: NSFW score updated")  # For debugging
    except KeyError as e:
        print(f"Error retrieving nsfw score for review: {e}")  # Logging the error
