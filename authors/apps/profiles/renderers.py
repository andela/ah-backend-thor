import json
from rest_framework.renderers import JSONRenderer

class ProfileRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # error = data.get('errors', None)

        # if error is not None:
        #     return super(ProfileRenderer, self).render(data)

        return json.dumps({
            'profile': data
        })

