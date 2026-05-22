from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.models import Page

from core.models import BasePage


class HomePage(BasePage):
    """Startpagina van Techture Media."""

    # Hero sectie
    hero_titel = models.CharField(
        verbose_name="Hero titel",
        max_length=100,
        default="Wij bouwen digitale ervaringen",
    )
    hero_subtitel = models.CharField(
        verbose_name="Hero subtitel",
        max_length=250,
        blank=True,
        help_text="Kort en krachtig – één zin die samenvat wat Techture Media doet.",
    )
    hero_achtergrond = models.ForeignKey(
        get_image_model_string(),
        verbose_name="Hero achtergrondafbeelding",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hero_cta_tekst = models.CharField(
        verbose_name="Hero knoptekst",
        max_length=50,
        blank=True,
        default="Bekijk ons werk",
    )
    hero_cta_pagina = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name="Hero knop verwijst naar",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    # Introductie sectie
    intro_titel = models.CharField(
        verbose_name="Introductie titel",
        max_length=100,
        blank=True,
    )
    intro_tekst = RichTextField(
        verbose_name="Introductie tekst",
        blank=True,
        features=["bold", "italic", "link"],
    )

    # Diensten sectie op homepage
    diensten_sectie_titel = models.CharField(
        verbose_name="Diensten sectie titel",
        max_length=100,
        blank=True,
        default="Wat wij doen",
    )

    # Blog sectie op homepage
    blog_sectie_titel = models.CharField(
        verbose_name="Blog sectie titel",
        max_length=100,
        blank=True,
        default="Laatste artikelen",
    )

    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "diensten.DienstenOverzichtPagina",
        "over.OverOnsPagina",
        "blog.BlogOverzichtPagina",
        "contact.ContactPagina",
        "core.BlokkenTestPagina",
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_titel"),
                FieldPanel("hero_subtitel"),
                FieldPanel("hero_achtergrond"),
                FieldPanel("hero_cta_tekst"),
                FieldPanel("hero_cta_pagina"),
            ],
            heading="Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel("intro_titel"),
                FieldPanel("intro_tekst"),
            ],
            heading="Introductie",
        ),
        MultiFieldPanel(
            [FieldPanel("diensten_sectie_titel")],
            heading="Diensten sectie",
        ),
        MultiFieldPanel(
            [FieldPanel("blog_sectie_titel")],
            heading="Blog sectie",
        ),
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

        from diensten.models import DienstPagina
        from blog.models import BlogArtikelPagina

        context["uitgelichte_diensten"] = (
            DienstPagina.objects.live().order_by("volgorde")[:4]
        )
        context["recente_artikelen"] = (
            BlogArtikelPagina.objects.live().order_by("-datum")[:3]
        )
        return context

    class Meta:
        verbose_name = "Startpagina"
        verbose_name_plural = "Startpagina's"
