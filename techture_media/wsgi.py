import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techture_media.settings.production")

application = get_wsgi_application()
