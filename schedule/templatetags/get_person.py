
from django import template

from users.models import Person

register = template.Library()


def is_following(value, show_id):
    person = Person.objects.get(pk=value.pk)
    return person.is_following(show_id=show_id)

register.filter('is_following', is_following)
