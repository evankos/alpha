from ast import literal_eval

from rest_framework.fields import Field, empty
from django.contrib.gis.db.models import PointField as GisPointField
from django.contrib.gis.geos import Point
import six
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import ungettext_lazy



@deconstructible
class CoordValidator(BaseValidator):
    message = ungettext_lazy(
        'Ensure this value has at most %(limit_value)d character (it has %(show_value)d).',
        'Ensure this value has at most %(limit_value)d characters (it has %(show_value)d).',
        'limit_value')
    code = 'coord_length'

    def compare(self, a, b):
        print("COMPARING!!!")
        return False  #TODO do an actual validation of coordinates

    def clean(self, x):
        return 1


class PointField(Field):
    default_error_messages = {
        'invalid': ('Not a valid string.!!!'),
        'blank': ('This field may not be blank.'),
        'max_length': ('Ensure this field has no more than {max_length} characters.'),
        'min_length': ('Ensure this field has at least {min_length} characters.')
    }
    initial = ''

    def __init__(self, **kwargs):
        self.allow_blank = kwargs.pop('allow_blank', False)
        self.trim_whitespace = kwargs.pop('trim_whitespace', True)
        super(PointField, self).__init__(**kwargs)
        # self.max_length = 5 #TODO make an actual check at some point
        # message = self.error_messages['max_length'].format(max_length=self.max_length)
        # self.validators = [CoordValidator(self.max_length, message=message)]


    def run_validation(self, data=empty):
        # Test for the empty string here so that it does not get validated,
        # and so that subclasses do not need to handle it explicitly
        # inside the `to_internal_value()` method.
        if data == '':
            if not self.allow_blank:
                self.fail('blank')
            return ''
        point = super(PointField, self).run_validation(data)
        return point


    def to_internal_value(self, data):
        # We're lenient with allowing basic numerics to be coerced into strings,
        # but other types should fail. Eg. unclear if booleans should represent as `true` or `True`,
        # and composites such as lists are likely user error.
        if isinstance(data, Point):
            return Point(data)
        elif type(data) is str:
            tup = literal_eval(data)
            return Point(tup)
        else:
            self.fail('invalid')


    def to_representation(self, value):
        return value.coords