from django import template
from django.db.models import Q, F
from .models import *
from .forms import *

register = template.Library()

@register.simple_tag
def reagent_form(*args, **kwargs):
    return ReagentForm()
