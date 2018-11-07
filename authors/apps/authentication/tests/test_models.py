from django.test import TestCase
from authors.apps.authentication.models import User

class ModelTesCase(TestCase):
    """Test suite for the api models."""
      
    def test_username_is_none(self):
        """Test whether username is None"""
        with self.assertRaises(TypeError):
            self.res = User.objects.create_user(username=None ,email="kjin@gmail.com", password=None)

    def test_email_is_None(self):
        """Test whether email is None"""
        with self.assertRaises(TypeError):
            self.res = User.objects.create_user(username='kalyango' ,email=None, password=None)
    
    def test_create_user(self):
        """Test for create user"""
        self.res = User.objects.create_user(username = 'kalyango', email='john@gmail.com', password=None)
        self.assertEqual(self.res.username, 'kalyango')
        self.assertEqual(self.res.email, 'john@gmail.com')

    def test_create_super_user(self):
        """Test for creating super user"""
        with self.assertRaises(TypeError):
            self.res = User.objects.create_superuser(username = 'kalyango', email='john@gmail.com', password=None)
        self.res = User.objects.create_superuser(username = 'kalyango', email='john@gmail.com', password='None')
        self.assertEqual(self.res.username, 'kalyango')
        self.assertEqual(self.res.email, 'john@gmail.com')    
        
    def test_property(self):
        self.assertTrue(User.get_full_name != None)
        self.assertTrue(User.token != None)

