from django.contrib.sitemaps import ping_google
from django.db import models
from datetime import datetime
import string
import re

class PublishedEntryManager(models.Manager):
    def get_queryset(self):
        return super(PublishedEntryManager, self).get_queryset().filter(publish_date__lte=datetime.now())

def to_slug(text):
    text = re.sub(r'\s+',' ',text)
    for rep in string.whitespace:
        text = text.replace(rep,'-')
    return text

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(unique=True, blank=True, max_length=128)

    @models.permalink
    def get_absolute_url(self):
        return ('blog_tag', (), {'slug':self.slug})

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            # self.slug = slugify(unidecode(unicode(self.title)))       # Suppport only English and numbers
            self.slug = to_slug(self.name)                             # Suppport other language (Unicode)
        super(Tag, self).save(*args, **kwargs)
        try:
            ping_google('/sitemap.xml')
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass

class Entry(models.Model):
    MANGA = 'MNG'
    DAILY = 'DLY'
    PROGRAM = 'PRG'
    REVIEW = 'RVW'
    CATEGORIES = (
        (DAILY, 'Daily'),
        (MANGA, 'Manga'),
        (PROGRAM, 'Program'),
        (REVIEW, 'Review'),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.CharField(unique=True, blank=True, max_length=128)
    category = models.CharField(max_length=3,
                            choices=CATEGORIES,
                            default=DAILY)
    tags = models.ManyToManyField(Tag)
    publish_date = models.DateTimeField(verbose_name='date published')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='created on')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='last updated')
    objects = models.Manager()
    published = PublishedEntryManager()

    class Meta:
        ordering = ['-publish_date', '-updated_on', 'title']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog_entry', (),
                {
                    'year':self.publish_date.year,
                    'month':self.publish_date.month,
                    'day':self.publish_date.day,
                    'slug':self.slug,
                })

    def is_published(self):
        now = datetime.now()
        return self.publish_date <= now
    is_published.admin_order_field = 'publish_date'
    is_published.boolean = True
    is_published.short_description = 'Published recently?'

    def comment_counter(self):
        return self.comment_set.count()
    comment_counter.short_description = 'Comment Counter'

    def get_next_entry(self):
        try:
            return self.get_next_by_publish_date()
        except:
            return False

    def get_previous_entry(self):
        try:
            return self.get_previous_by_publish_date()
        except:
            return False

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            # self.slug = slugify(unidecode(unicode(self.title)))       # Suppport only English and numbers
            self.slug = to_slug(self.title)                             # Suppport other language (Unicode)
        super(Entry, self).save(*args, **kwargs)
        try:
            ping_google('/sitemap.xml')
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass

from django.db.models.signals import pre_save
from signals import create_redirect
pre_save.connect(create_redirect, sender=Entry, dispatch_uid="001")

class Comment(models.Model):
    name = models.CharField(max_length=42)
    email = models.EmailField(max_length=75, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    text = models.TextField()
    entry = models.ForeignKey(Entry)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text
