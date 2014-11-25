from django.db import models
from django.template.defaultfilters import slugify
from unidecode import unidecode

class PublishedEntryManager(models.Manager):
    def get_queryset(self):
        return super(PublishedEntryManager, self).get_queryset().filter(is_published=True)

class Entry(models.Model):
    MANGA = 'MNG'
    DAILY = 'DLY'
    PROGRAM = 'PRG'
    CATEGORIES = (
        (DAILY, 'Daily'),
        (MANGA, 'Manga'),
        (PROGRAM, 'Program'),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=3,
                            choices=CATEGORIES,
                            default=DAILY)
    is_published = models.BooleanField(default=False,
                                       verbose_name="Publish?")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    published = PublishedEntryManager()

    class Meta:
        ordering = ['-created_on']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog_entry', (),
                {
                    'year':self.created_on.year,
                    'month':self.created_on.month,
                    'day':self.created_on.day,
                    'slug':self.slug,
                })

    def get_next_entry(self):
        try:
            return self.get_next_by_create_date()
        except:
            return False

    def get_previous_entry(self):
        try:
            return self.get_previous_by_create_date()
        except:
            return False

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
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