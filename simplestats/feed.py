import simplestats.models

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed


# See https://github.com/django/django/blob/master/django/contrib/syndication/views.py
class CountdownFeed(Atom1Feed):
    def add_item_elements(self, handler, item):
        super(CountdownFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('embed:icon', str(item['icon']))


# See https://github.com/django/django/blob/master/django/utils/feedgenerator.py
class LatestEntriesFeed(Feed):
    description = 'Updates on changes and additions to police beat central.'
    description_template = 'simplestats/feeds/description.html'
    feed_type = CountdownFeed
    link = '/stats/feeds/'  # TODO: Fix hard coded link
    title = 'Dashboard'
    title_template = 'simplestats/feeds/title.html'

    def items(self):
        return simplestats.models.Countdown.objects.order_by('-created')

    def item_updateddate(self, item):
        return item.created

    def item_extra_kwargs(self, item):
        return {
            'public': item.public,
            'icon': item.icon,
        }

    def item_author_name(self, item):
        return item.owner.username
