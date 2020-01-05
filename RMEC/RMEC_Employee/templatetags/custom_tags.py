from django import template
from random import randint
register = template.Library()
@register.simple_tag

def url_replace(request, field, value):

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()
@register.simple_tag
def random_number(request):
    x= request.GET.get("num1")
    y= request.GET.get("num2")
    
    return x