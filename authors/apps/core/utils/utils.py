import jwt
from rest_framework.exceptions import APIException
from django.conf import settings

class Utils:
    def get_token(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, 'utf-8')
            try:
                author_id = payload['id']
            except:
                author_id = payload['user_id']
        except Exception as exception:
            raise APIException({
                'error': f'Login Token required. System error: {str(exception)}'
            })
        else:
            return author_id
