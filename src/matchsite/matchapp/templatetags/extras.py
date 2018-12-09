from django import template
import json

register = template.Library()


@register.filter
def display_matches(matches):
    html = []
    for match in matches:
        html.append('<div class=col-sm-4 my-4>\
            <div class = card-groups >\
            <div class = card>\
            <img class=card-img-top src = ' + str(match.profile.image.url) + '  alt = Card image cap >\
            <div class =card-body>\
            <h5 class = card-title>' + str(match.username) + ' </h5>\
            </ div >\
            <p class = card-text >\
            <div > <b > Email: </b> ' + str(match.profile.email) + ' </div>\
            <div > <b > Age: </b>' + str(match.profile.age) + ' </div>\
            <div > <b > Gender: </b> ' + str(match.profile.gender) + '</div>\
            </ p >\
            </ div >\
            </ div >\
            </ div >')
    return json.dumps(str(html)[1:-1])
