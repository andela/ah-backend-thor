import os

from django.test import TestCase


class WsgiTestCase(TestCase):

    def test_default_env_settings(self):
        self.assertEqual(os.environ.get("DJANGO_SETTINGS_MODULE"), "authors.settings")