from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    # just returning the baseline here - hashing will be performed by the parent class
    def _make_hash_value(self, ex_user, timestamp):
        return (
                str(ex_user.pk) + str(timestamp) +
                str(ex_user.user.is_active)
        )


token_generator = TokenGenerator()
