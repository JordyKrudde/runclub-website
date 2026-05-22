import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from core.models import BasePage


@register_snippet
class BlogCategorie(models.Model):
    """Categorie voor blogartikelen."""

    naam = models.CharField(verbose_name="Naam", max_length=100)
    slug = models.SlugField(verbose_name="URL-slug", unique=True)

    panels = [
        FieldRowPanel([FieldPanel("naam"), FieldPanel("slug")]),
    ]

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name = "Blogcategorie"
        verbose_name_plural = "Blogcategorieën"
        ordering = ["naam"]


class BlogOverzichtPagina(BasePage):
    """Overzichtspagina van alle blogartikelen."""

    intro = RichTextField(
        verbose_name="Introductietekst",
        blank=True,
        features=["bold", "italic"],
    )
    artikelen_per_pagina = models.PositiveSmallIntegerField(
        verbose_name="Artikelen per pagina",
        default=9,
    )

    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogArtikelPagina"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("artikelen_per_pagina"),
        FieldPanel("body"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Inhoud"),
            ObjectList(BasePage.seo_panels, heading="SEO"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        artikelen = BlogArtikelPagina.objects.child_of(self).live().order_by("-datum")

        # Filteren op categorie
        categorie_slug = request.GET.get("categorie")
        if categorie_slug:
            artikelen = artikelen.filter(categorie__slug=categorie_slug)
            try:
                context["actieve_categorie"] = BlogCategorie.objects.get(slug=categorie_slug)
            except BlogCategorie.DoesNotExist:
                pass

        # Paginering
        paginator = Paginator(artikelen, self.artikelen_per_pagina)
        pagina_nummer = request.GET.get("pagina", 1)
        try:
            context["artikelen"] = paginator.page(pagina_nummer)
        except PageNotAnInteger:
            context["artikelen"] = paginator.page(1)
        except EmptyPage:
            context["artikelen"] = paginator.page(paginator.num_pages)

        context["alle_categorieën"] = BlogCategorie.objects.all()
        return context

    class Meta:
        verbose_name = "Blog overzichtspagina"
        verbose_name_plural = "Blog overzichtspagina's"


class BlogArtikelPagina(BasePage):
    """Detailpagina voor één blogartikel."""

    datum = models.DateField(
        verbose_name="Publicatiedatum",
        default=datetime.date.today,
    )
    auteur = models.CharField(
        verbose_name="Auteur",
        max_length=100,
        blank=True,
    )
    intro = models.TextField(
        verbose_name="Inleiding",
        max_length=400,
        help_text="Wordt getoond in de overzichtskaart en bij zoekresultaten (max. 400 tekens).",
    )
    uitgelichte_afbeelding = models.ForeignKey(
        get_image_model_string(),
        verbose_name="Uitgelichte afbeelding",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    categorie = models.ForeignKey(
        BlogCategorie,
        verbose_name="Categorie",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="artikelen",
    )

    parent_page_types = ["blog.BlogOverzichtPagina"]
    subpage_types = []

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldRowPanel([FieldPanel("datum"), FieldPanel("auteur")]),
                FieldPanel("categorie"),
            ],
            heading="Meta",
        ),
        FieldPanel("uitgelichte_afbeelding"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Inhoud"),
            ObjectList(BasePage.seo_panels, heading="SEO"),
        ]
    )

    class Meta:
        verbose_name = "Blogartikel"
        verbose_name_plural = "Blogartikelen"
        ordering = ["-datum"]
