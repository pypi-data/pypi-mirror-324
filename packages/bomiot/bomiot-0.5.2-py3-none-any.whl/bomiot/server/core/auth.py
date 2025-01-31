from rest_framework.exceptions import APIException
from .jwt_auth import parse_payload
from django.contrib.auth import get_user_model
from .message import login_message_return

User = get_user_model()

class CoreAuthentication(object):
    def authenticate(self, request) -> tuple[bool, User]:
        if request.path in ['/', '/api/docs/', '/api/debug/', '/api/']:
            return (False, None)
        else:
            token = request.META.get('HTTP_TOKEN', '')
            result = parse_payload(token)
            if token:
                try:
                    user_data = User.objects.filter(id=int(result.get('data').get('id'))).first()
                    if user_data.is_active is True:
                        if sorted(user_data.permission.items()) == sorted(result.get('data').get('permission').items()):
                            return (True, user_data)
                        else:
                            raise APIException(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'Please Login Again'))
                    else:
                        raise APIException(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'User is not active'))
                except:
                    raise APIException(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'User Does Not Exists'))
            else:
                raise APIException(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'Please Login First'))

    def authenticate_header(self, request):
        pass
