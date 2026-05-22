from django.db import models
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from core.models import BasePage


@register_snippet
class TeamLid(models.Model):
    """Teamlid dat getoond wordt op de 'Over ons' pagina."""

    naam = models.CharField(verbose_name="Naam", max_length=100)
    functie = models.CharField(verbose_name="Functie", max_length=100)
    bio = RichTextField(
        verbose_name="Biografie",
        blank=True,
        features=["bold", "italic", "link"],
    )
    foto = models.ForeignKey(
        get_image_model_string(),
        verbose_name="Foto",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    volgorde = models.PositiveSmallIntegerField(
        verbose_name="Volgorde",
        default=0,
        help_text="Lagere nummers verschijnen eerder.",
    )

    panels = [
        MultiFieldPanel(
            [
                FieldRowPanel([FieldPanel("naam"), FieldPanel("functie")]),
                FieldPanel("bio"),
                FieldPanel("foto"),
                FieldPanel("volgorde"),
            ],
            heading="Teamlid",
        )
    ]

    def __str__(self):
        return f"{self.naam} – {self.functie}"

    class Meta:
        verbose_name = "Teamlid"
        verbose_name_plural = "Teamleden"
        ordering = ["volgorde", "naam"]


class OverOnsPagina(BasePage):
    """Over ons pagina van Techture Media."""

    intro = RichTextField(
        verbose_name="Introductietekst",
        blank=True,
        features=["h2", "h3", "bold", "italic", "link", "ul", "ol"],
    )
    team_sectie_titel = models.CharField(
        verbose_name="Team sectie titel",
        max_length=100,
        blank=True,
        default="Ons team",
    )
    team_sectie_tonen = models.BooleanField(
        verbose_name="Team sectie tonen",
        default=True,
    )

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("team_sectie_titel"),
                FieldPanel("team_sectie_tonen"),
            ],
            heading="Team",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Inhoud"),
            ObjectList(BasePage.seo_panels, heading="SEO"),
        ]
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["teamleden"] = TeamLid.objects.all()
        return context

    class Meta:
        verbose_name = "Over ons pagina"
        verbose_name_plural = "Over ons pagina's"
