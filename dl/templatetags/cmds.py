from django import template
from django.template.defaultfilters import stringfilter
from dl.models import Task
from datetime import date
register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def give_img(url):
    if url.endswith('.pdf'):
        newUrl = "/static/images/pdf-file.png"
        return newUrl
    elif url.endswith('.doc') or url.endswith('.docx'):
        newUrl = "/static/images/doc-file.png"
        return str(newUrl)
    else:
        newUrl = "{% static 'images/boss-baby-movie-poster-870x600.png' %}"
        return str(newUrl)

@register.filter(is_safe=True)
@stringfilter
def get_letter(grade):
    try:
        if int(grade) >= 95 and int(grade) <= 100:
            return "A"
        elif int(grade) >= 90 and int(grade) <= 94:
            return "A-"
        elif int(grade) >= 85 and int(grade) <= 89:
            return "B+"
        elif int(grade) >= 80 and int(grade) <= 84:
            return "B"
        elif int(grade) >= 75 and int(grade) <= 79:
            return "B-"
        elif int(grade) >= 70 and int(grade) <= 74:
            return "C+"
        elif int(grade) >= 65 and int(grade) <= 69:
            return "C"
        elif int(grade) >= 60 and int(grade) <= 64:
            return "C-"
        elif int(grade) >= 55 and int(grade) <= 59:
            return "D+"
        elif int(grade) >= 50 and int(grade) <= 54:
            return "D"
        else:
            return "F"
    except:
        return "F"