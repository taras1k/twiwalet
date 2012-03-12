from django import template

register = template.Library()

@register.inclusion_tag('users/login_widget.html')
def login_widget(user):
    return { 'user': user }