VERSION = (0, 8, 7)


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    # Append 3rd digit if > 0
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])

    return version


default_app_config = 'django_classified.apps.DjangoClassifiedConfig'
name = "django_classified"
