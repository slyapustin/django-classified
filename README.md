# Django Classified

## Features

- Item groups, categories and areas (for ex. Cities or Locations)
- Image
  - upload multiple images per item
  - generating preview (via [sorl-thumbnail](https://github.com/mariocesar/sorl-thumbnail))
  - display in a Bootstrap 5 modal with a carousel
- Search ability
- SEO
  - SEO-friendly URLs, including non-Latin characters (Arabic, Cyrillic, etc.)
  - `sitemap.xml` covering both item and category pages
  - Self-referencing canonical URLs
  - Per-page meta descriptions, including category pages
  - [JSON-LD](https://schema.org/Product) structured data (`Product`, `BreadcrumbList`) on item pages
  - [Open Graph](http://ogp.me/) and Twitter card tags
  - `robots.txt`, and `noindex` on search, profile and form pages
  - `<html lang>` follows the active translation
  - RSS feed
  - Google Analytics 4 (GA4) integration
- Caching of `robots.txt` and the RSS feed
- Translation
  - Arabic
  - Azerbaijani
  - English
  - French (thanks to [Teolemon](https://github.com/teolemon))
  - German
  - Polish
  - Portuguese
  - Russian
  - Spanish (thanks to [4bimcad](https://github.com/4bimcad))
  - Turkish (thanks to [Mirat Can Bayrak](https://github.com/miratcan))
  - Help translate to other languages at [Transifex](https://www.transifex.com/inoks/django-classified/)

## Requirements

- Python >=3.10
- Django >=5.2, <6.1

## Design

- [Bootstrap 5.3](https://getbootstrap.com/docs/5.3/)
- No external requests: no jQuery, no CDN, no webfonts. The only script is
  Bootstrap's own bundle, and typography uses system font stacks.
- Light and dark themes via Bootstrap's `data-bs-theme` attribute
- Accessible defaults: visible focus styles, `prefers-reduced-motion` respected,
  and a print stylesheet

All templates live under `django_classified/templates/django_classified/` and can
be overridden by placing a file of the same name earlier on the template path.

## Demo project

Demo project with user registration (via Email/Facebook) available [here](https://github.com/slyapustin/django-classified-demo).

## Installation

- Install app `pip install django-classified`
- Add `django_classified` to the `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # Default Django applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

     # Required by Django Classified
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

     # External applications required by Django Classified
    'sorl.thumbnail',

    # Django Classified
    'django_classified',
]
```

- Add `SITE_ID` to `settings.py` file:

```python
SITE_ID = 1
```

- Import `include` in addition to `path` and add `path('', include('django_classified.urls', namespace='django_classified')),` to the project `urls.py` file:

```python
from django.urls import path, include

urlpatterns = [
    path('', include('django_classified.urls', namespace='django_classified')),
]
```

- Add `'django_classified.context_processors.common_values'` to the settings `TEMPLATES` `context_processors` list:

```python
TEMPLATES[0]['OPTIONS']['context_processors'].append('django_classified.context_processors.common_values')
```

## Customization:

You can provide additional customization in settings.py

- `DCF_SITE_NAME` - Site title
- `DCF_SITE_DESCRIPTION` - Site description
- `DCF_ITEM_PER_USER_LIMIT` - Max Items allowed per user
- `DCF_SITEMAP_LIMIT` - Sitemap items limit
- `DCF_RSS_LIMIT` - RSS feed items limit
- `DCF_RELATED_LIMIT` - Number of related items displayed
- `DCF_ITEM_PER_PAGE` - Number of items per page
- `DCF_LOGIN_TO_CONTACT` - Hide contact information for unauthorized requests
- `DCF_DISPLAY_EMPTY_GROUPS` - Display groups without items in the groups list
- `DCF_DISPLAY_CREDITS` - Show the "Powered by Django Classified" footer credit (default: `True`)
- `DCF_CURRENCY` - Site currency (default: 'USD')

### Optional integrations

- `GOOGLE_ANALYTICS_PROPERTY_ID` - Google Analytics 4 measurement ID (e.g. 'G-XXXXXXXXXX')
- `GOOGLE_SITE_VERIFICATION_ID` - Google Search Console verification code
- `FACEBOOK_APP_ID` - Facebook App ID for Open Graph integration

## Upgrading to 1.3

1.3 migrates the bundled templates from Bootstrap 3 to Bootstrap 5 and removes
several dependencies. If you use the templates as shipped, upgrading with
`pip install -U django-classified` is all you need. Otherwise:

- **Remove `'bootstrapform'` from `INSTALLED_APPS`.** `django-bootstrap-form` is
  no longer a dependency, so leaving it listed raises `ModuleNotFoundError`. The
  `bootstrap` template filter is now provided by this package and keeps its name,
  so `{% load i18n bootstrap %}` still works.
- **If you override any bundled template**, it is now Bootstrap 5 markup. The old
  Bootstrap 3 classes (`form-group`, `control-label`, `help-block`, `pull-right`,
  `btn-default`, glyphicons) are gone.
- **These static files were removed**: jQuery, lightbox2, the Glyphicons fonts,
  `jumbotron-narrow.css`, and `bootstrap.min.css.map`. Reference them from your
  own project if you still need them.
- Item images now open in a Bootstrap modal with a carousel instead of lightbox2.

See `changelog.txt` for the full list.

## Current Version

The current version is 1.3 (July 2026).
