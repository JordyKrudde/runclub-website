from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse

from wagtail.models import Page
from wagtail.search.backends import get_search_backend


def search(request):
    zoekterm = request.GET.get("zoeken", "")
    pagina_nummer = request.GET.get("pagina", 1)

    zoekresultaten = Page.objects.none()

    if zoekterm:
        backend = get_search_backend()
        zoekresultaten = backend.search(zoekterm, Page.objects.live())

    paginator = Paginator(zoekresultaten, 10)
    try:
        zoekresultaten = paginator.page(pagina_nummer)
    except PageNotAnInteger:
        zoekresultaten = paginator.page(1)
    except EmptyPage:
        zoekresultaten = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "zoekterm": zoekterm,
            "zoekresultaten": zoekresultaten,
        },
    )
