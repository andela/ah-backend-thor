import json
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList


class CommentsRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, media_type=None, render_context=None):
        """
        Converts between list and dict to render the appropriate data type
        """
        if type(data) != ReturnList:
            errors = data.get("error", None)
            if errors != None:
                return super(CommentsRenderer, self).render(data)
            else:
                return json.dumps({"comment": data})
        else:
            return json.dumps({"comments": data, "commentsCount": len(data)})
