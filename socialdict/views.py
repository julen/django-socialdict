from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list import ListView

from socialdict.forms import TermForm
from socialdict.models import Term 


class LetterView(ListView):

    template_name = 'socialdict/letter_list.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.letter = kwargs['letter']
        return super(LetterView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(LetterView, self).get_context_data(**kwargs)
        ctx.update({
            'letter': self.letter,
        })
        return ctx

    def get_queryset(self):
        return Term.objects.filter(alphabet_letter=self.letter) \
                           .order_by('name')

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

