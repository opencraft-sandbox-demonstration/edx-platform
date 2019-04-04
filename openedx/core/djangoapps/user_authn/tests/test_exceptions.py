""" Test Auth related exception. """

from unittest import TestCase

from openedx.core.djangoapps.user_authn.exceptions import AuthFailedError


class AuthFailedErrorTests(TestCase):
    """ Tests for AuthFailedError exception."""

    def test_sanitize_message(self):
        """ Tests that AuthFailedError sanitize the message properly."""
        script_tag = '<script>alert("vulnerable")</script>'
        safe_tags = '<a href="/login">login</a><br>'
        message = '{safe_tags}{script_tag}'.format(safe_tags=safe_tags, script_tag=script_tag)
        exception = AuthFailedError(message)

        sanitized_script_tag = '&lt;script&gt;alert("vulnerable")&lt;/script&gt;'
        expected_value = u'{unsanitized_tags}{sanitized_script_tag}'.format(
            unsanitized_tags=safe_tags, sanitized_script_tag=sanitized_script_tag
        )
        self.assertEqual(exception.value, expected_value)
