from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer





def validated(serializer, raise_exception=True):
    """
    Decorator for validation of view methods of rest-framework.
    """
    serializer = BaseSerializer if (serializer is None) else serializer

    def decorator(func):
        assert (issubclass(serializer, BaseSerializer)), \
            '@The decorator takes a Serializer instance as parameter.'
        def wrapper(*args, **kwargs):
            assert (isinstance(args[1], Request)), \
                '@The second argument should be a Request.'
            request = args[1]
            ser = serializer(data=request.data)
            if ser.is_valid(raise_exception=raise_exception):
                if hasattr(ser, 'post_validation'):
                    ser.post_validation()
                setattr(request, 'validation_serializer', ser)
                setattr(request, 'validated_object', ser.save(validated_data=ser.validated_data))
            return func(*args, **kwargs)
        return wrapper
    return decorator