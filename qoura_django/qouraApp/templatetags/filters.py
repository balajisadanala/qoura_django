from django import template

register = template.Library()

@register.filter
def user_vote_status(question, user):
    return question.user_vote_status(user)