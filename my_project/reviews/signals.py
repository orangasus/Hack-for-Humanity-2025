from ai_mod.views import check_review_for_nsfw
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Review, ReviewStatus


@receiver([post_save, post_delete], sender=Review)
def on_review_save_delete(sender, instance, **kwargs):
    recalc_prof_rating(instance)
    if kwargs['signal'] == post_save:
        instance.__class__.objects.filter(id=instance.id).update(
            review_status=ReviewStatus.UNDER_REVIEW
        )
        instance.refresh_from_db()
        get_nsfw_data(instance)
        instance.refresh_from_db()
        update_review_moderation_status(instance)


def recalc_prof_rating(instance):
    professors = instance.course.professors.all()
    for prof in professors:
        prof.update_rating()


def get_nsfw_data(instance):
    title_n_body = instance.title + "\n" + instance.body
    check_res = check_review_for_nsfw(title_n_body)
    passed = check_res['Passed']
    try:
        score = check_res['NSFW Score']
        update_nsfw_data(instance, passed, score)
    except Exception as e:
        update_nsfw_data(instance, passed)


def update_nsfw_data(instance, passed, score=-1):
    if score == -1:
        instance.__class__.objects.filter(id=instance.id).update(
            nsfw_passed=passed
        )
    else:
        instance.__class__.objects.filter(id=instance.id).update(
            nsfw_passed=passed, nsfw_score=score
        )


def update_review_moderation_status(instance):
    review_status = ReviewStatus.PASSED_REVIEW if instance.nsfw_passed else ReviewStatus.FAILED_REVIEW
    instance.__class__.objects.filter(id=instance.id).update(
        review_status=review_status
    )
