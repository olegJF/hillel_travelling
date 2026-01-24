from django import template

__all__ = (
    'format_duration',
)

register = template.Library()

@register.filter
def format_duration(td):
    seconds = int(td.total_seconds())
    days, seconds = divmod(seconds, 60 * 60 * 24)
    hours, seconds = divmod(seconds, 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    hours = str(hours).zfill(2)
    minutes = str(minutes).zfill(2)
    if days:
        days = str(days)
        if 5 < int(days) < 21:
            day_str = "днів"
        elif days[-1] == "1":
            day_str = "день"
        elif days[-1] in "234":
            day_str = "дні"
        else:
            day_str = "днів"
        return f'{days} {day_str} {hours}:{minutes}'
    return f'{hours}:{minutes}'
