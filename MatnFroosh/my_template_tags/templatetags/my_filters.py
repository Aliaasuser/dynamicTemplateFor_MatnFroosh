from django import template
from django.utils.text import slugify
from datetime import datetime, date, time
import jdatetime

register = template.Library()

@register.filter
def limitText(value: str, num_of_words: int):
    words = value.split(maxsplit=num_of_words)
    limited_text = ''
    if num_of_words < len(words):
        limited_text = ' '.join(words[:num_of_words]) + '...'
    else:
        limited_text = ' '.join(words)
    return limited_text

@register.filter
def multiplicationBy(value: int | float, num: int | float):
    return value * num

@register.filter
def getAttr(value: object, attrname: str):
    return getattr(value, attrname)

@register.filter
def mySlugify(value: str):
    return slugify(value, True)

@register.filter
def split(value: str, sep: str):
    return value.split(sep=sep)

@register.filter
def convertToMyJDate(value: date):
    return '/'.join(str(jdatetime.date.fromgregorian(date=value)).split(sep='-'))

@register.filter
def convertToMyTime(value: time):
    return f'{"0" + str(value.hour) if value.hour < 10 else value.hour}:{"0" + str(value.minute) if value.minute < 10 else value.minute}:{"0" + str(value.second) if value.second < 10 else value.second}'

@register.filter
def convertToMyJDateTime(value: datetime):
    return f'{convertToMyJDate(value.date())} - {convertToMyTime(value.time())}'

convertToMyJDateTime.expects_localtime = True