from rest_framework.serializers import ValidationError

def password_validator(password, confirm_password):
    """custom password validator"""
    if len(password) < 8:
        raise ValidationError('Password must be atleast 8 characters long.')
    if password != confirm_password:
        raise ValidationError('Both password must match.')