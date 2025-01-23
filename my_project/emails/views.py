from base64 import urlsafe_b64decode
from email.message import EmailMessage

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode

from .token_gen import account_activation_token


def send_confirmation_email(request, user):
    # domain = get_current_site(request).domain
    mail_subject = 'Account Activation'
    message = render_to_string('confirmation_template.html',
                               {
                                   "user": user,
                                   "domain": '127.0.0.1:8000',
                                   # char/digit -> byte representation (8bit for each char) -> encode64 (6bit for each char) (url-safe) representation
                                   "uid": generate_uidb64(user.pk),
                                   "token": account_activation_token.make_token(user)
                               })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return HttpResponse('Confirmation email sent!')

def generate_uidb64(id):
    init_res = urlsafe_base64_encode(force_bytes(id))
    # check that res length is a multiple of 4
    res = init_res + '=' * ((4 - len(init_res) % 4) % 4)
    return res

def activate_account(request, uidb64, token):
    uid = force_str(urlsafe_b64decode(uidb64))
    user = User.objects.get(pk=uid)

    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Account Confirmed!')
    else:
        return HttpResponse('Verification Failed :(')
