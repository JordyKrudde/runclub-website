from django.db import models
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField
from wagtail.images import get_image_model_string
from modelcluster.fields import ParentalKey


class ContactFormulierVeld(AbstractFormField):
    """Formulierveld voor de contactpagina (beheerd via Wagtail admin)."""

    page = ParentalKey(
        "ContactPagina",
        on_delete=models.CASCADE,
        related_name="form_fields",
        verbose_name="Pagina",
    )


class ContactPagina(AbstractEmailForm):
    """Contactpagina met e-mailformulier via Wagtail FormBuilder."""

    template = "contact/contact_pagina.html"
    landing_page_template = "contact/contact_pagina_bedankt.html"

    intro = RichTextField(
        verbose_name="Introductietekst",
        blank=True,
        features=["bold", "italic", "link"],
    )
    bedankt_tekst = RichTextField(
        verbose_name="Bedankt-tekst",
        blank=True,
        help_text="Getoond nadat het formulier is verstuurd.",
        features=["bold", "italic"],
    )

    # SEO-velden (handmatig, omdat we AbstractEmailForm erven i.p.v. BasePage)
    seo_description = models.CharField(
        verbose_name="SEO-omschrijving",
        max_length=160,
        blank=True,
    )
    og_image = models.ForeignKey(
        get_image_model_string(),
        verbose_name="Deelafbeelding (OG)",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Formuliervelden"),
        MultiFieldPanel(
            [
                FieldPanel("to_address"),
                FieldPanel("from_address"),
                FieldPanel("subject"),
            ],
            heading="E-mailinstellingen",
        ),
        FieldPanel("bedankt_tekst"),
    ]

    seo_panels = [
        MultiFieldPanel(
            [
                FieldPanel("slug"),
                FieldPanel("seo_title"),
                FieldPanel("seo_description"),
                FieldPanel("og_image"),
                FieldPanel("search_description"),
                FieldPanel("show_in_menus"),
            ],
            heading="Zoekmachine-optimalisatie",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Inhoud"),
            ObjectList(seo_panels, heading="SEO"),
        ]
    )

    class Meta:
        verbose_name = "Contactpagina"
        verbose_name_plural = "Contactpagina's"
