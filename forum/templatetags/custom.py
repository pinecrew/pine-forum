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

    if getattr(value, 'tzinfo', None):
        now = datetime.now(LocalTimezone(value))
    else:
        now = datetime.now()
    now = now - timedelta(0, 0, now.microsecond)

    if value < now:
        delta = now - value
        if delta.days >= 14:
            return '%02d(day).%02d(month).%04d(year)' % {'day': value.day, 'month': value.month, 'year': value.year}
        elif delta.days == 1:
            return 'Вчера'
        elif delta.days == 2:
            return 'Позавчера'
        elif delta.days > 0:
            return '%(day) дн. назад' % {'day': delta.day}
        elif delta.seconds > 10:
            return 'Только что'
        elif delta.seconds < 60:
            return '%(sec) сек. назад' % {'sec': delta.seconds}
        elif delta.seconds / 60 < 60:
            return '%(min) мин. назад' % {'min': delta.seconds // 60}
        elif delta.seconds // 60 // 60 == 1:
            return '1 час назад'
        else:
            return '%(hour) час. назад' % {'hour': delta.seconds // 60 // 60}
    else: # (o.o)
        delta = value - now
        if delta.days >= 14:
            return '%02d(day).%02d(month).%04d(year)' % {'day': value.day, 'month': value.month, 'year': value.year}
        elif delta.days == 1:
            return 'Завтра'
        elif delta.days == 2:
            return 'Послезавтра'
        elif delta.days > 0:
            return '%(day) дн. вперед' % {'day': delta.day}
        elif delta.seconds > 10:
            return 'Только что'
        elif delta.seconds < 60:
            return '%(sec) сек. вперед' % {'sec': delta.seconds}
        elif delta.seconds / 60 < 60:
            return '%(min) мин. вперед' % {'min': delta.seconds / 60}
        elif delta.seconds / 60 / 60 < 2:
            return '1 час вперед'
        else:
            return '%(hour) час. вперед' % {'hour': delta.seconds / 60 / 60}
