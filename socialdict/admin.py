from django.contrib import admin

from socialdict.models import Term 

class TermAdmin(admin.ModelAdmin):
    pass

admin.site.register(Term, TermAdmin)
