from ....settings import DATABASES, TEST_RUNNER
from django.test import TestCase


class TestSettingsAndCore(TestCase):
    def test_database(self):
        checklist =['ENGINE', 'NAME','USER','PASSWORD','HOST', 'PORT']
        self.assertTrue('default' in DATABASES)
        self.assertIn([x for x in checklist][0], DATABASES['default'])

    def test_test_runner(self):
        self.assertTrue('django_nose.NoseTestSuiteRunner', TEST_RUNNER)
