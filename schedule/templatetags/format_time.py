
import datetime
from django import template

register = template.Library()


def time_12(value):
    """formats time to 12 hour"""
    try:
        time = datetime.datetime.strptime(value, '%H:%M')
        new_time = datetime.datetime.strftime(time, '%I:%M%p')
        return new_time
    except ValueError:
        return value

register.filter('time_12', time_12)
