import re
import logging

from django.core.exceptions import PermissionDenied

logger = logging.getLogger(__name__)


def validate_password(password, confirm_password):
    if password != confirm_password:
        return {'status': False, 'message': 'Password does not match.'}

    if len(password) < 8:
        return {'status': False, 'message': 'Password length less than 8.'}

    if not re.search('[a-z]', password):
        return {'status': False, 'message': 'Lowercase missing from password!'}

    if not re.search('[A-Z]', password):
        return {'status': False, 'message': 'Uppercase missing from password!'}

    if not re.search('[0-9]', password):
        return {'status': False, 'message': 'Digit missing from password!'}

    if not re.search('[@#_]', password):
        return {'status': False, 'message': "Special character '@' , '#' , '_' missing from password!"}

    return {'status': True, 'message': 'Correct password format.'}


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def validate_username(username):
    if 8 <= len(username) <= 20:
        return {'status': True, 'message': 'Success'}
    return {'status': False, 'message': 'Username should be between 8-20 characters.'}


def validate_role(function):
    def wrapper(self, request):
        if request.user.user_type not in self.user_type:
            msg = 'The users does not have permission'
            logger.info(msg)
            raise PermissionDenied(msg)
        return function(self, request)

    return wrapper
