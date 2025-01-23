from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    # just returning the baseline here - hashing will be performed by the parent class
    def _make_hash_value(self, user, timestamp):
        return (
                str(user.pk) + str(timestamp) +
                str(user.is_active)
        )


account_activation_token = TokenGenerator()
