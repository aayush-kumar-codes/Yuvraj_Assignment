def normalize_validation_error(error) -> object:
    """normalizes validation error"""
    errors = error.__dict__.items()
    details = {}
    for key, value in errors:
        details[key] = value[0]
    return details


def normalize_serializer_error(error) -> object:
    """normalizes serializer errors"""
    errors = error.items()
    details = {}
    for key, value in errors:
        details[key] = value[0]
    return details
