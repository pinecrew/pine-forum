from datetime import datetime, timedelta

from django import template
register = template.Library()

# this things should be translated ...
# https://docs.djangoproject.com/en/1.10/topics/i18n/translation/

# splits value by delimiter
@register.filter
def split(value, arg):
    return value.split(arg)

# returns simple value for timesince
@register.filter
def datesince(value):
    try:
        value = datetime(value.year, value.month, value.day, value.hour, value.minute, value.second)
    except:
        return value

    now = datetime.utcnow() # some magic with timezones
    now = now - timedelta(0, 0, now.microsecond)

    if value < now:
        delta = now - value
        if delta.days >= 14:
            return '{day:02d}.{month:02d}.{year:04d}'.format(day=value.day, month=value.month, year=value.year)
        elif delta.days == 1:
            return 'Вчера'
        elif delta.days == 2:
            return 'Позавчера'
        elif delta.days > 0:
            return '{} дн. назад'.format(delta.days)
        elif delta.seconds < 10:
            return 'Только что'
        elif delta.seconds < 60:
            return '{} сек. назад'.format(delta.seconds)
        elif delta.seconds // 60 < 60:
            return '{} мин. назад'.format(delta.seconds // 60)
        elif delta.seconds // 3600 == 1:
            return '1 час назад'
        else:
            return '{} час. назад'.format(delta.seconds // 3600)
    else: # (o.o)
        delta = value - now
        if delta.days >= 14:
            return '{day:02d}.{month:02d}.{year:04d}'.format(day=value.day, month=value.month, year=value.year)
        elif delta.days == 1:
            return 'Завтра'
        elif delta.days == 2:
            return 'Послезавтра'
        elif delta.days > 0:
            return 'Через {} дн.'.format(delta.days)
        elif delta.seconds < 5:
            return 'Только что'
        elif delta.seconds < 60:
            return 'Через {} сек.'.format(delta.seconds)
        elif delta.seconds // 60 < 60:
            return 'Через {} мин.'.format(delta.seconds // 60)
        elif delta.seconds // 3600 == 1:
            return 'Через 1 час'
        else:
            return 'Через {} час.'.format(delta.seconds // 3600)
