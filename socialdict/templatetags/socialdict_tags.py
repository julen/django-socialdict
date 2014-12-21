import locale

from django import template
from django.db.models import Count

from socialdict.models import Term


locale.setlocale(locale.LC_ALL, 'eu_ES.UTF-8')

register = template.Library()


@register.inclusion_tag('socialdict/latest_terms_snippet.html')
def render_latest_socialdict_terms(num):
    terms = Term.objects.all().order_by('-date_added')[:num]
    return { 'terms': terms }


@register.inclusion_tag('socialdict/alphabet_snippet.html')
def render_socialdict_alphabet():
    alphabet = Term.objects.values_list('alphabet_letter', flat=True).distinct()
    alphabet_list = []
    for letter in alphabet:
        letter_count = Term.objects.filter(alphabet_letter=letter).count()
        alphabet_list.append({ 'letter': letter, 'count': letter_count })
    alphabet_list.sort(lambda x, y: locale.strcoll(x['letter'], y['letter']))
    return { 'alphabet': alphabet_list }


@register.inclusion_tag('socialdict/totals_snippet.html')
def render_socialdict_totals():
    term_count = Term.objects.all().count()
    author_count = Term.objects.values('social_user').distinct().count()
    return { 'term_count': term_count, 'author_count': author_count }


@register.inclusion_tag('socialdict/top_authors_snippet.html')
def render_socialdict_top_authors(num):
    top_authors = Term.objects.values('social_user')\
                      .annotate(contributions=Count('social_user'))\
                      .order_by('-contributions')[:num]
    return { 'top_authors': top_authors }
