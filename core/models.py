from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.fields import StreamField
from wagtail.images import get_image_model_string
from wagtail.models import Page

from .blocks import STANDARD_BLOCKS


class BasePage(Page):
    """Abstracte basisklasse voor alle paginatypen van Techture Media."""

    seo_description = models.CharField(
        verbose_name="SEO-omschrijving",
        max_length=160,
        blank=True,
        help_text="Korte omschrijving voor zoekmachines (max. 160 tekens).",
    )
    og_image = models.ForeignKey(
        get_image_model_string(),
        verbose_name="Deelafbeelding (OG)",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Afbeelding voor sociale media (aanbevolen: 1200×630 px).",
    )
    body = StreamField(
        STANDARD_BLOCKS,
        verbose_name="Inhoud",
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    seo_panels = [
        MultiFieldPanel(
            [
                FieldPanel("slug"),
                FieldPanel("seo_title"),
                FieldPanel("seo_description"),
                FieldPanel("og_image"),
                FieldPanel("search_description"),
            ],
            heading="Zoekmachine-optimalisatie",
        ),
        MultiFieldPanel(
            [FieldPanel("show_in_menus")],
            heading="Navigatie",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Inhoud"),
            ObjectList(seo_panels, heading="SEO"),
        ]
    )

    class Meta:
        abstract = True


class BlokkenTestPagina(BasePage):
    """Testpagina met één demo-instantie van elk beschikbaar StreamField blok."""

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    class Meta:
        verbose_name = "Blokken testpagina"
        verbose_name_plural = "Blokken testpagina's"
