from django import template
from django.db.models import Q, F
from reagents.models import Reagent
from auth_user.models import *
from .models import *

# "lte" : significa "less than or equal", ou seja, menor ou igual
# "lt"  : significa "less than", ou seja, menor.
# "gte" : significa "greater than or equal", ou seja, maior ou igual.
# "gt"  : significa "greater than", ou seja, maior.

register = template.Library()

@register.simple_tag
def get_reagents_alert(*args, **kwargs):
    reagents = Reagent.objects.filter(Q(amount__lte=F('limit'))).order_by('amount')
    return reagents

@register.simple_tag
def get_register_request(*args, **kwargs):
    users = User.objects.filter(is_active=False)
    return users

@register.simple_tag
def get_movement_request(*args, **kwargs):
    requests = Request.objects.filter(appoove=False).order_by('dt_request')
    return requests