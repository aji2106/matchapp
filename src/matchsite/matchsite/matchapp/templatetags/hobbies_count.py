from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_number_of_hobbies(context, string):
    string = str(string)