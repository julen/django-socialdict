from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed

from socialdict.models import Term

current_site = Site.objects.get_current()

class LatestEntriesFeed(Feed):
    author_name =  "hitzokei"
    copyright = "http://%s/about/" % current_site.domain
    description = "Azken hitzokeiak."
    feed_type = Atom1Feed
    item_copyright = "http://%s/about/" % current_site.domain
    link = "/feed/entries/"
    title = "%s: azken sarrerak" % current_site.name

    def items(self):
        return Term.objects.all().order_by('-date_added')[:15]

    def item_pubdate(self, item):
        return item.date_added

    def item_guid(self, item):
        return "tag:%s,%s:%s" % (current_site.domain,
                                 item.date_added.strftime('%Y-%m-%d'),
                                 item.get_term_url())

    def item_author_name(self, item):
        return item.social_user

    def item_link(self, item):
        return item.get_term_url()

    def item_description(self, item):
        return item.meaning
