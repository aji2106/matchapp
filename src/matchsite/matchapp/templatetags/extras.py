from django import template
from matchapp.models import Number, Like
import json

register = template.Library()


@register.filter
def check_relationship(user, like_user):
    return Like.objects.filter(from_user=like_user).filter(to_user=user).exists()


@register.filter
def check_likes(match, user):
    return Like.objects.filter(from_user=user).filter(to_user=match).exists()


@register.filter
def check_request(match, user):
    everyone = Number.objects.all()
    return everyone.filter(to_user=user).filter(from_user=match).exists()


@register.filter
def check_sent(match, user):
    everyone = Number.objects.all()
    return everyone.filter(to_user=match).filter(from_user=user).exists()


@register.filter
def display_matches(matches, user):
    html = []
    imgsrc = ""
    for match in matches:

        if check_likes(match, user):
            imgsrc = '/static/images/like_2.png'
        else:
            imgsrc = '/static/images/like_1.png'

        html.append('<div class=col-sm-4 my-4>\
            <div class=col-md-2 pt-3>\
            </div>\
            <img class=card-img-top src = ' + str(match.profile.image.url) + '  alt = Card image cap>\
            <div class=card-body text-center>\
            <h5 class = card-title>' + str(match.username) + ' \
            <input type = image id='+str(match.id)+' class = heart name = submit src = ' + imgsrc+'\
            border = 0 alt = Submit style = width:50px; border:0 none;/>\
            </h5>\
            </div>\
            <table>\
            <tr>\
            <td> Age: ' + str(match.profile.age) + '</td>\
            </tr>\
            <tr>\
            <td> Gender: ' + str(match.profile.gender) + '</td>\
            </tr>\
            </table>\
            </div>')

    return json.dumps(str(html)[1:-1])
