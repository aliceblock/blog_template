blog_template
=============

Blog template with Twitter Bootstrap

-- SEO(Search Engine Optimization) --
Add to INSTALLED_APPS
'django.contrib.sites',             # Enable site framework
'django.contrib.redirects',         # URL redirecting

[settings.py]
SITE_ID = 1

python manage.py migrate

Add to MIDDLEWARE_CLASSES
'django.contrib.redirects.middleware.RedirectFallbackMiddleware',

** Now can use redirecting with your site 

---------------------------------------------
