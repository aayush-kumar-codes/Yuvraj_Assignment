from rest_framework.serializers import ValidationError

import re

def password_validator(password, confirm_password):
    regex = ("^(?=.*[a-z])(?=." +
             "*[A-Z])(?=.*\\d)" +
             "(?=.*[-+_!@#$%^&*., ?]).+$")
             
    pattern = re.compile(pattern=regex)

    if len(password) < 8:
        raise ValidationError('Password must be atleast 8 characters long.')
    if not re.search(pattern, password):
        raise ValidationError('Password must contain small case letter, upper case letter, special chars and numbers.')
    if password != confirm_password:
        raise ValidationError('Both password must match.')