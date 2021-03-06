from base import *

from django.utils.translation import ugettext as _
import django.dispatch

class ActiveTagManager(models.Manager):
    def get_query_set(self):
        return super(ActiveTagManager, self).get_query_set().exclude(used_count__lt=1)


class Tag(BaseModel):
    name            = models.CharField(max_length=255, unique=True)
    created_by      = models.ForeignKey(User, related_name='created_tags')
    marked_by       = models.ManyToManyField(User, related_name="marked_tags", through="MarkedTag")
    # Denormalised data
    used_count = models.PositiveIntegerField(default=0)

    active = ActiveTagManager()


    class Meta:
        ordering = ('-used_count', 'name')
        app_label = 'forum'

    def __unicode__(self):
        return self.name

class MarkedTag(models.Model):
    TAG_MARK_REASONS = (('good',_('interesting')),('bad',_('ignored')))
    tag = models.ForeignKey(Tag, related_name='user_selections')
    user = models.ForeignKey(User, related_name='tag_selections')
    reason = models.CharField(max_length=16, choices=TAG_MARK_REASONS)

    class Meta:
        app_label = 'forum'

