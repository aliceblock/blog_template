from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime
from unidecode import unidecode

class PublishedEntryManager(models.Manager):
    def get_queryset(self):
        return super(PublishedEntryManager, self).get_queryset().filter(publish_date__lte=datetime.now())

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('blog_tag', (), {'slug':self.slug})

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(unidecode(unicode(self.name)))
        super(Tag, self).save(*args, **kwargs)

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
    slug = models.SlugField(unique=True)
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
            self.slug = slugify(unidecode(unicode(self.title)))
        super(Entry, self).save(*args, **kwargs)

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