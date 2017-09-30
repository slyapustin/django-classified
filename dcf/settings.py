"""
Default settings for dcf app.
"""

from django.conf import settings

# Site currency
DCF_CURRENCY = getattr(settings, 'DCF_CURRENCY', 'USD')

# Display credits in footer
DCF_DISPLAY_CREDITS = getattr(settings, 'DCF_DISPLAY_CREDITS', True)

# Max items per page
DCF_ITEM_PER_PAGE = getattr(settings, 'DCF_ITEM_PER_PAGE', 10)

# Max items per user
DCF_ITEM_PER_USER_LIMIT = getattr(settings, 'DCF_ITEM_PER_USER_LIMIT', 20)

# Hide contact details for unauthorized users
DCF_LOGIN_TO_CONTACT = getattr(settings, 'DCF_LOGIN_TO_CONTACT', True)

# Max related items displayed on page
DCF_RELATED_LIMIT = getattr(settings, 'DCF_RELATED_LIMIT', 6)

# Max items included to the RSS feed
DCF_RSS_LIMIT = getattr(settings, 'DCF_RSS_LIMIT', 100)

# Site default description
DCF_SITE_DESCRIPTION = getattr(settings, 'DCF_SITE_DESCRIPTION', 'Classified Advertisements Powered by Django DCF')

# Default site name
DCF_SITE_NAME = getattr(settings, 'DCF_SITE_NAME', 'Django DCF')

# Sitemap items limit
DCF_SITEMAP_LIMIT = getattr(settings, 'DCF_SITEMAP_LIMIT', 1000)
