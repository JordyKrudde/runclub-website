from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("", include(wagtail_urls)),
]

if settings.DEBUG:
    # Lokale ontwikkeling: Django serveert media-bestanden
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif not getattr(settings, "AWS_STORAGE_BUCKET_NAME", None):
    # Productie zonder S3: Django serveert /media/ als tijdelijke fallback.
    # Bestanden zijn niet persistent — configureer S3/R2 voor permanente opslag.
    from django.views.static import serve as _media_serve
    urlpatterns += [
        path("media/<path:path>", _media_serve, {"document_root": settings.MEDIA_ROOT}),
    ]
