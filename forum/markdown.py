import re
import markdown

from django.contrib.auth import get_user_model

User = get_user_model()


def render_html(text):
    mentions = set(re.findall(r'\B@.+?\b', text))
    usernames = User.objects.filter(username__in=[i[1:] for m in mentions]).values_list('username', flat=True)
    for username in usernames:
        mention = f'@{username}'
        text = text.replace(mention, f'<a href="/user/{username}/">{mention}</a>')
    return markdown.markdown(text, extensions=['markdown.extensions.extra'])
