from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.models import Page

from core.models import BasePage


class DienstenOverzichtPagina(BasePage):
    """Overzichtspagina van alle diensten van Techture Media."""

    intro = RichTextField(
        verbose_name="Introductie",
        blank=True,
        features=["bold", "italic", "link"],
    )

    parent_page_types = ["home.HomePage"]
    subpage_types = ["diensten.DienstPagina"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
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
        context["diensten"] = self.get_children().live().specific().order_by(
            "dienstpagina__volgorde"
        )
        return context

    class Meta:
        verbose_name = "Diensten overzichtspagina"
        verbose_name_plural = "Diensten overzichtspagina's"


class DienstPagina(BasePage):
    """Detailpagina voor één dienst van Techture Media."""

    uitgelichte_afbeelding = models.ForeignKey(
        get_image_model_string(),
        verbose_name="Uitgelichte afbeelding",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    korte_beschrijving = models.TextField(
        verbose_name="Korte beschrijving",
        max_length=300,
        help_text="Wordt getoond op de overzichtspagina en de homepage (max. 300 tekens).",
    )
    volgorde = models.PositiveSmallIntegerField(
        verbose_name="Volgorde",
        default=0,
        help_text="Lagere nummers verschijnen eerder in de lijst.",
    )

    parent_page_types = ["diensten.DienstenOverzichtPagina"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("uitgelichte_afbeelding"),
        FieldPanel("korte_beschrijving"),
        FieldPanel("volgorde"),
        FieldPanel("body"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Inhoud"),
            ObjectList(BasePage.seo_panels, heading="SEO"),
        ]
    )

    class Meta:
        verbose_name = "Dienst"
        verbose_name_plural = "Diensten"
        ordering = ["volgorde"]
