from django.contrib.auth.tokens import PasswordResetTokenGenerator 
import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user_obj, timestamp):
        return ( six.text_type(user_obj.pk))+six.text_type(timestamp)+six.text_type(user_obj.is_active)
generate_token = TokenGenerator()