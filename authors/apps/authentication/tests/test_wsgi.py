import os

from django.test import TestCase
from ....wsgi import application


class WsgiTestCase(TestCase):

    def test_default_env_settings(self):
        self.assertEqual(os.environ.get(
            "DJANGO_SETTINGS_MODULE"), "authors.settings")

    def test_aapplication_created(self):
        self.assertTrue(application != None)
