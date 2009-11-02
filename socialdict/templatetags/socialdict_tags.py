from django import template
from socialdict.models import Term

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
    return { 'alphabet': alphabet_list }

@register.inclusion_tag('socialdict/totals_snippet.html')
def render_socialdict_totals():
    term_count = Term.objects.all().count()
    author_count = Term.objects.values('social_user').distinct().count()
    return { 'term_count': term_count, 'author_count': author_count }
