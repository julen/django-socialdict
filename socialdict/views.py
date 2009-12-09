from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list

from socialdict.forms import TermForm
from socialdict.models import Term 

def letter(request, letter, page):
    """
    Returns an object_list with Term objects matching 'letter' as the
    starting letter for the term.
    """
    terms = Term.objects.filter(alphabet_letter=letter).order_by('name')
    return object_list(request, queryset=terms,
                       paginate_by=10, page=page,
                       extra_context={'letter': letter},
                       template_name='socialdict/letter_list.html')

def add(request):
    """
    Returns a form to add new terms.
    """
    if request.method == 'POST':
        form = TermForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TermForm()
    return render_to_response('socialdict/add_term.html', {'form': form},
                              context_instance=RequestContext(request))

