from django import template

register = template.Library()


@register.filter
def display_matches(matches):

    for match in matches:
        html += '<div class = "container" > \
            <div class = "card-groups" >\
            < div class = "card" >\
            <img class = "card-img-top" src = "' + match.profile.image.url + ' " alt = "Card image cap" >\
            < div class = "card-body" >\
            < h5 class = "card-title" >' + match.username + ' < /h5 >\
            < / div >\
            < p class = "card-text" >\
            < div > <b > Email: < /b > ' + match.profile.email + ' < /div >\
            < div > <b > Age: < /b > '+match.profile.age + ' < /div >\
            < div > <b > Gender: < /b > '+match.profile.gender + '< /div >\
            < div > <b > Hobbies: < /b > ' + match.hobbies + ' < /div >\
            < / p >\
            < / div >\
            < / div >\
            < / div >'

    return html
