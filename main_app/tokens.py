from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountOauthLinkTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{user.password}{timestamp}{user.email}"

  
account_oauth_link_token_generator = AccountOauthLinkTokenGenerator()