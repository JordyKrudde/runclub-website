from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    EmailBlock,
    IntegerBlock,
    ListBlock,
    PageChooserBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    TextBlock,
    URLBlock,
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


# ─── Bestaande blokken ────────────────────────────────────────────────────────

class HeroBlock(StructBlock):
    badge_tekst = CharBlock(
        label="Badge-tekst",
        max_length=50,
        required=False,
        help_text="Optioneel label boven de titel, bv. 'Est. 2024 / Urban Athletics'.",
    )
    titel = CharBlock(label="Titel", max_length=100)
    subtitel = CharBlock(label="Subtitel", max_length=200, required=False)
    afbeelding = ImageChooserBlock(label="Afbeelding")
    cta_tekst = CharBlock(label="Knoptekst", max_length=50, required=False)
    cta_interne_link = PageChooserBlock(label="Interne link", required=False)
    cta_externe_link = URLBlock(label="Externe link", required=False)
    secundaire_cta_tekst = CharBlock(
        label="Secundaire knoptekst", max_length=50, required=False
    )
    secundaire_cta_interne_link = PageChooserBlock(
        label="Secundaire interne link", required=False
    )
    secundaire_cta_externe_link = URLBlock(
        label="Secundaire externe link", required=False
    )

    class Meta:
        template = "blocks/hero_block.html"
        icon = "image"
        label = "Hero"


class RichTextSectionBlock(StructBlock):
    inhoud = RichTextBlock(
        label="Tekst",
        features=["h2", "h3", "bold", "italic", "link", "ul", "ol", "blockquote"],
    )

    class Meta:
        template = "blocks/richtext_section_block.html"
        icon = "pilcrow"
        label = "Tekstblok"


class ImageBlock(StructBlock):
    afbeelding = ImageChooserBlock(label="Afbeelding")
    bijschrift = CharBlock(label="Bijschrift", max_length=200, required=False)
    alt_tekst = CharBlock(label="Alt-tekst", max_length=200, required=False)

    class Meta:
        template = "blocks/image_block.html"
        icon = "image"
        label = "Afbeelding"


class TwoColumnBlock(StructBlock):
    linker_kolom = RichTextBlock(
        label="Linker kolom",
        features=["h2", "h3", "bold", "italic", "link", "ul", "ol", "blockquote"],
    )
    rechter_kolom = RichTextBlock(
        label="Rechter kolom",
        features=["h2", "h3", "bold", "italic", "link", "ul", "ol", "blockquote"],
    )

    class Meta:
        template = "blocks/two_column_block.html"
        icon = "grip"
        label = "Twee kolommen"


class QuoteBlock(StructBlock):
    citaat = TextBlock(label="Citaat")
    auteur = CharBlock(label="Auteur", max_length=100, required=False)
    functie = CharBlock(label="Functie", max_length=100, required=False)

    class Meta:
        template = "blocks/quote_block.html"
        icon = "openquote"
        label = "Citaat"


class CallToActionBlock(StructBlock):
    titel = CharBlock(label="Titel", max_length=100)
    tekst = TextBlock(label="Tekst", required=False)
    knop_tekst = CharBlock(label="Knoptekst", max_length=50)
    knop_link = URLBlock(label="Knoplink")
    stijl = ChoiceBlock(
        label="Stijl",
        choices=[
            ("light", "Licht"),
            ("dark", "Donker"),
            ("accent", "Accent"),
        ],
        default="dark",
    )

    class Meta:
        template = "blocks/call_to_action_block.html"
        icon = "pick"
        label = "Call to action"


class VideoEmbedBlock(StructBlock):
    video = EmbedBlock(label="Video-URL (YouTube, Vimeo, etc.)")
    bijschrift = CharBlock(label="Bijschrift", max_length=200, required=False)

    class Meta:
        template = "blocks/video_embed_block.html"
        icon = "media"
        label = "Video"


# ─── Nieuwe blokken ───────────────────────────────────────────────────────────

class ProjectKaartBlock(StructBlock):
    """Eén projectkaart binnen een ProjectKaartRasterBlock."""

    titel = CharBlock(label="Titel", max_length=100)
    subtitel = CharBlock(label="Subtitel", max_length=200, required=False)
    thumbnail = ImageChooserBlock(label="Afbeelding")
    tags = ListBlock(
        CharBlock(max_length=50),
        label="Tags",
        help_text="Bv. 'Branding', 'Website', 'Strategie'",
    )
    link_pagina = PageChooserBlock(label="Interne link", required=False)
    link_url = URLBlock(label="Externe link", required=False)

    class Meta:
        icon = "image"
        label = "Projectkaart"


class ProjectKaartRasterBlock(StructBlock):
    """Raster van projectkaarten, 2–3 per rij."""

    titel = CharBlock(
        label="Sectietitel",
        max_length=100,
        required=False,
        help_text="Optionele koptitel boven het raster.",
    )
    projecten = ListBlock(ProjectKaartBlock(), label="Projecten")

    class Meta:
        template = "blocks/project_kaart_raster_block.html"
        icon = "grip"
        label = "Projecten raster"


class DienstKaartBlock(StructBlock):
    """Eén dienstkaart binnen een DienstenRasterBlock."""

    icoon = ImageChooserBlock(label="Icoon / illustratie")
    titel = CharBlock(label="Titel", max_length=100)
    beschrijving = TextBlock(label="Beschrijving")
    bullet_points = ListBlock(
        CharBlock(max_length=120),
        label="Bulletpoints",
        help_text="Wat je concreet doet voor deze dienst.",
    )
    link_pagina = PageChooserBlock(label="Link naar pagina", required=False)

    class Meta:
        icon = "pick"
        label = "Dienstkaart"


class DienstenRasterBlock(StructBlock):
    """Drie dienstkaarten naast elkaar."""

    titel = CharBlock(
        label="Sectietitel",
        max_length=100,
        required=False,
    )
    diensten = ListBlock(DienstKaartBlock(), label="Diensten")

    class Meta:
        template = "blocks/diensten_raster_block.html"
        icon = "pick"
        label = "Diensten raster"


class StatistiekItemBlock(StructBlock):
    """Eén statistiek met optioneel klantlogo."""

    klant_logo = ImageChooserBlock(label="Klantlogo", required=False)
    getal = CharBlock(
        label="Getal / waarde",
        max_length=30,
        help_text="Bv. '£15M', '#1', '200+'",
    )
    label = CharBlock(
        label="Label",
        max_length=100,
        help_text="Bv. 'in funding opgehaald'",
    )
    beschrijving = TextBlock(label="Toelichting", required=False)

    class Meta:
        icon = "order"
        label = "Statistiek"


class StatistiekenBlock(StructBlock):
    """Resultaten / social proof sectie met meerdere statistieken."""

    titel = CharBlock(label="Sectietitel", max_length=100, required=False)
    statistieken = ListBlock(StatistiekItemBlock(), label="Statistieken")

    class Meta:
        template = "blocks/statistieken_block.html"
        icon = "order"
        label = "Statistieken"


class TestimonialBlock(StructBlock):
    """Één uitgebreid klantcitaat met foto."""

    citaat = TextBlock(label="Citaat")
    naam_auteur = CharBlock(label="Naam auteur", max_length=100)
    rol_auteur = CharBlock(label="Rol / functie auteur", max_length=100)
    foto_auteur = ImageChooserBlock(label="Foto auteur", required=False)

    class Meta:
        template = "blocks/testimonial_block.html"
        icon = "openquote"
        label = "Testimonial"


class LogoItemBlock(StructBlock):
    """Eén logo binnen een LogoStripBlock."""

    afbeelding = ImageChooserBlock(label="Logo")
    alt_tekst = CharBlock(
        label="Alt-tekst",
        max_length=100,
        help_text="Naam van het bedrijf voor schermlezers.",
    )

    class Meta:
        icon = "image"
        label = "Logo"


class LogoStripBlock(StructBlock):
    """Horizontale rij van klantlogo's."""

    titel = CharBlock(
        label="Titel",
        max_length=100,
        required=False,
        help_text="Bv. 'Zij gingen je voor'",
    )
    logos = ListBlock(LogoItemBlock(), label="Logo's")

    class Meta:
        template = "blocks/logo_strip_block.html"
        icon = "image"
        label = "Logo strip"


class FAQItemBlock(StructBlock):
    """Eén vraag-en-antwoord item."""

    vraag = CharBlock(label="Vraag", max_length=200)
    antwoord = RichTextBlock(
        label="Antwoord",
        features=["bold", "italic", "link", "ul", "ol"],
    )

    class Meta:
        icon = "help"
        label = "FAQ item"


class FAQBlock(StructBlock):
    """Inklapbare FAQ-sectie (accordion)."""

    titel = CharBlock(label="Sectietitel", max_length=100)
    items = ListBlock(FAQItemBlock(), label="Vragen")

    class Meta:
        template = "blocks/faq_block.html"
        icon = "help"
        label = "FAQ"


class GenummerdKenmerkBlock(StructBlock):
    """Eén genummerd kenmerk of voordeel."""

    nummer = CharBlock(
        label="Nummer",
        max_length=4,
        help_text="Bv. '01', '02'",
    )
    titel = CharBlock(label="Titel", max_length=100)
    beschrijving = TextBlock(label="Beschrijving")

    class Meta:
        icon = "list-ol"
        label = "Kenmerk"


class GenummerdeFeaturesBlock(StructBlock):
    """2×2 raster van genummerde voordelen of kenmerken."""

    titel = CharBlock(label="Sectietitel", max_length=100)
    items = ListBlock(GenummerdKenmerkBlock(), label="Kenmerken")

    class Meta:
        template = "blocks/genummerde_features_block.html"
        icon = "list-ol"
        label = "Genummerde kenmerken"


class ContactCTABlock(StructBlock):
    """Persoonlijk contactblok onderaan een pagina."""

    koptekst = CharBlock(label="Koptekst", max_length=150)
    subtekst = TextBlock(label="Subtekst", required=False)
    contact_naam = CharBlock(label="Naam contactpersoon", max_length=100)
    contact_rol = CharBlock(
        label="Rol contactpersoon",
        max_length=100,
        required=False,
    )
    contact_foto = ImageChooserBlock(label="Foto contactpersoon")
    email = EmailBlock(label="E-mailadres", required=False)
    telefoon = CharBlock(
        label="Telefoonnummer",
        max_length=30,
        required=False,
    )

    class Meta:
        template = "blocks/contact_cta_block.html"
        icon = "mail"
        label = "Contact CTA"


class EventKaartBlock(StructBlock):
    """Eén evenement binnen een EventenRasterBlock."""

    afbeelding = ImageChooserBlock(label="Afbeelding")
    categorie_tag = CharBlock(
        label="Categorie",
        max_length=30,
        help_text="Bv. 'TEMPO RUN', 'TRAIL RUN', 'SOCIAL 5K'",
    )
    titel = CharBlock(label="Titel", max_length=100)
    locatie = CharBlock(label="Locatie", max_length=150)
    datum_maand = CharBlock(
        label="Maand",
        max_length=10,
        help_text="Bv. 'OCT'",
    )
    datum_dag = CharBlock(
        label="Dag",
        max_length=4,
        help_text="Bv. '12'",
    )
    tijd = CharBlock(label="Tijd", max_length=30, help_text="Bv. '7:00 PM'")
    niveau = CharBlock(
        label="Niveau",
        max_length=30,
        help_text="Bv. 'Intermediate', 'Difficult', 'All Levels'",
    )
    knop_tekst = CharBlock(
        label="Knoptekst", max_length=30, default="RSVP NOW"
    )
    knop_link = URLBlock(label="Knoplink", required=False)

    class Meta:
        icon = "date"
        label = "Event"


class EventenRasterBlock(StructBlock):
    """Raster van aankomende evenementen."""

    label = CharBlock(
        label="Eyebrow-label",
        max_length=50,
        required=False,
        help_text="Bv. 'Don't Miss Out'",
    )
    titel = CharBlock(
        label="Sectietitel",
        max_length=100,
        required=False,
        help_text="Bv. 'Upcoming Events'",
    )
    link_tekst = CharBlock(
        label="Linktekst",
        max_length=50,
        required=False,
        help_text="Bv. 'VIEW FULL CALENDAR'",
    )
    link_url = URLBlock(label="Linkadres", required=False)
    events = ListBlock(EventKaartBlock(), label="Evenementen")

    class Meta:
        template = "blocks/evenementen_raster_block.html"
        icon = "date"
        label = "Evenementen raster"


class RouteKaartBlock(StructBlock):
    """Eén routekaart binnen een RoutesRasterBlock."""

    afbeelding = ImageChooserBlock(label="Afbeelding")
    tag = CharBlock(
        label="Tag",
        max_length=30,
        help_text="Bv. 'FLAT & FAST', 'STAIR CLIMBS', 'SCENIC'",
    )
    titel = CharBlock(label="Titel", max_length=100)

    class Meta:
        icon = "site"
        label = "Route"


class RoutesRasterBlock(StructBlock):
    """Raster van routekaarten."""

    label = CharBlock(
        label="Eyebrow-label",
        max_length=50,
        required=False,
        help_text="Bv. 'The City is our Track'",
    )
    titel = CharBlock(label="Sectietitel", max_length=100, required=False)
    tekst = TextBlock(label="Introtekst", required=False)
    routes = ListBlock(RouteKaartBlock(), label="Routes")

    class Meta:
        template = "blocks/routes_raster_block.html"
        icon = "site"
        label = "Routes raster"


class DoelTrackerBlock(StructBlock):
    """Voortgangsbalk richting een doel."""

    titel = CharBlock(label="Titel", max_length=100)
    beschrijving = TextBlock(label="Beschrijving", required=False)
    voortgang_label = CharBlock(
        label="Voortgangslabel",
        max_length=50,
        required=False,
        default="Current Progress",
    )
    percentage = IntegerBlock(
        label="Percentage",
        default=0,
        help_text="Voortgang in procenten (0-100).",
    )
    huidige_label = CharBlock(
        label="Label huidige waarde",
        max_length=30,
        help_text="Bv. '0 MILES'",
    )
    doel_label = CharBlock(
        label="Label doelwaarde",
        max_length=30,
        help_text="Bv. '10,000 MILES'",
    )

    class Meta:
        template = "blocks/doel_tracker_block.html"
        icon = "tasks"
        label = "Doeltracker"


class NieuwsbriefCTABlock(StructBlock):
    """Nieuwsbrief-aanmeldsectie met afbeelding."""

    titel = CharBlock(label="Titel", max_length=150)
    tekst = TextBlock(label="Tekst", required=False)
    afbeelding = ImageChooserBlock(label="Afbeelding", required=False)
    placeholder_tekst = CharBlock(
        label="Placeholder e-mailveld",
        max_length=50,
        default="YOUR EMAIL ADDRESS",
    )
    knop_tekst = CharBlock(label="Knoptekst", max_length=30, default="SIGN UP")

    class Meta:
        template = "blocks/nieuwsbrief_cta_block.html"
        icon = "mail"
        label = "Nieuwsbrief CTA"


# ─── Exportlijst ──────────────────────────────────────────────────────────────

STANDARD_BLOCKS = StreamBlock(
    [
        # Bestaand
        ("hero", HeroBlock()),
        ("tekst", RichTextSectionBlock()),
        ("afbeelding", ImageBlock()),
        ("twee_kolommen", TwoColumnBlock()),
        ("citaat", QuoteBlock()),
        ("call_to_action", CallToActionBlock()),
        ("video", VideoEmbedBlock()),
        # Nieuw
        ("project_raster", ProjectKaartRasterBlock()),
        ("diensten_raster", DienstenRasterBlock()),
        ("statistieken", StatistiekenBlock()),
        ("testimonial", TestimonialBlock()),
        ("logo_strip", LogoStripBlock()),
        ("faq", FAQBlock()),
        ("genummerde_kenmerken", GenummerdeFeaturesBlock()),
        ("contact_cta", ContactCTABlock()),
        ("evenementen_raster", EventenRasterBlock()),
        ("routes_raster", RoutesRasterBlock()),
        ("doel_tracker", DoelTrackerBlock()),
        ("nieuwsbrief_cta", NieuwsbriefCTABlock()),
    ],
    use_json_field=True,
)
