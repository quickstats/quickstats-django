import simplestats.models

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed


# See https://github.com/django/django/blob/master/django/contrib/syndication/views.py
class CountdownFeed(Atom1Feed):
    def add_item_elements(self, handler, item):
        pass
        super(CountdownFeed, self).add_item_elements(handler, item)
        # print('item', item)
        # handler.addQuickElement('itunes:explicit', 'clean')


# See https://github.com/django/django/blob/master/django/utils/feedgenerator.py
class LatestEntriesFeed(Feed):
    title = "Dashboard"
    # TODO: Fix hard coded link
    link = '/stats/feeds/'
    description = "Updates on changes and additions to police beat central."
    feed_type = CountdownFeed

    def items(self):
        return simplestats.models.Countdown.objects.order_by('-created')

    def item_title(self, item):
        return item.label

    def item_description(self, item):
        return '{}\n{}'.format(item.created, item.description)

    def item_updateddate(self, item):
        return item.created

    def item_extra_kwargs(self, item):
        return {
            'public': item.public,
            'icon': item.icon,
        }

    def item_author_name(self, item):
        return item.owner.username
