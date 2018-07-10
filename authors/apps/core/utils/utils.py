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

    def article_read_time(self, article_body, article_image_url):
        
        WPM = 267
        WORD_LENGTH = 3
        IMAGE_WEIGHT = 0.05
        NUMBER_OF_IMAGES = 1
        total_words = 0
        for article_text in article_body:
            total_words += len(article_text) / WORD_LENGTH
        if len(article_image_url) > 5:
            read_time = int((total_words / WPM)) + \
                int(IMAGE_WEIGHT * NUMBER_OF_IMAGES)
        else:
            read_time = int((total_words / WPM))
        return str(read_time)
