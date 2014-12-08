blog_template
=============

Blog template with Twitter Bootstrap

-- SEO(Search Engine Optimization) --
```
Add to INSTALLED_APPS
'django.contrib.sites',             # Enable site framework
'django.contrib.redirects',         # URL redirecting
```

[settings.py]
```
SITE_ID = 1
```

Do migrate
```
python manage.py migrate
```

Add to MIDDLEWARE_CLASSES
```
'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
```

** Now can use redirecting with your site

Create [signals.py]
```python
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site

def create_redirect(sender, instance, **kwargs):
  if sender == BlogPost:
    try:
      o = sender.objects.get(id=instance.id)
      if o.slug != instance.slug:
        old_path = o.get_absolute_url()
        new_path = instance.get_absolute_url()
        # Update any existing redirects that are pointing to the old url
        for redirect in Redirect.objects.filter(new_path=old_path):
          redirect.new_path = new_path
          # If the updated redirect now points to itself, delete it
          # (i.e. slug = A -> slug = B -> slug = A again)
          if redirect.new_path == redirect.old_path:
            redirect.delete()
          else:
            redirect.save()
        # Now add the new redirect
        Redirect.objects.create(
          site=Site.objects.get_current(),
          old_path=old_path,
          new_path=new_path)
    except sender.DoesNotExist:
        pass
```
[models.py]
```python
class Entry(models.Model):
    ...
    slug = models.CharField(unique=True, blank=True, max_length=128)
    
    @models.permalink
    def get_absolute_url(def):
        return ('blog_entry', (),
                {
                    'year':self.publish_date.year,
                    'month':self.publish_date.month,
                    'day':self.publish_date.day,
                    'slug':self.slug,
                })

from django.db.models.signals import pre_save
from signals import create_redirect
pre_save.connect(create_redirect, sender=Entry, dispatch_uid="001")
```

=========================================
