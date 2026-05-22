"""
Management command: build_fixtures

Maakt een complete set demo-pagina's aan voor de Techture Media website,
inclusief een blokken-testpagina met één voorbeeld van elk StreamField blok.

Gebruik:
    python manage.py build_fixtures
    python manage.py build_fixtures --leeg   # verwijder bestaande inhoud eerst
"""

import io
import uuid

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from wagtail.images import get_image_model
from wagtail.models import Page, Site


def uid():
    """Genereer een uniek ID voor een StreamField blok."""
    return str(uuid.uuid4())


class Command(BaseCommand):
    help = "Maak demo-pagina's en blokken-testinhoud aan voor Techture Media."

    def add_arguments(self, parser):
        parser.add_argument(
            "--leeg",
            action="store_true",
            help="Verwijder alle bestaande pagina's en sites voor het aanmaken.",
        )

    def handle(self, *args, **options):
        if options["leeg"]:
            self._verwijder_bestaande_inhoud()

        self.stdout.write("⏳  Placeholder afbeelding aanmaken...")
        self.placeholder = self._maak_placeholder_afbeelding()

        self.stdout.write("⏳  Homepage aanmaken...")
        homepage = self._maak_homepage()

        self.stdout.write("⏳  Diensten aanmaken...")
        self._maak_diensten(homepage)

        self.stdout.write("⏳  Over ons pagina aanmaken...")
        self._maak_over_ons(homepage)

        self.stdout.write("⏳  Blog aanmaken...")
        self._maak_blog(homepage)

        self.stdout.write("⏳  Contactpagina aanmaken...")
        self._maak_contact(homepage)

        self.stdout.write("⏳  Blokken testpagina aanmaken...")
        self._maak_blokken_testpagina(homepage)

        self.stdout.write("⏳  Wagtail site instellen...")
        self._maak_site(homepage)

        self.stdout.write(self.style.SUCCESS("\n✅  Fixtures succesvol aangemaakt!"))
        self.stdout.write(f"    Startpagina ID : {homepage.pk}")
        self.stdout.write("    Open de Wagtail-admin om de pagina's te bekijken.\n")

    # ─── Hulpfuncties ─────────────────────────────────────────────────────────

    def _verwijder_bestaande_inhoud(self):
        self.stdout.write("🗑️   Bestaande inhoud verwijderen...")
        # Wagtail Site en pagina's
        Site.objects.all().delete()
        root = Page.objects.filter(depth=1).first()
        if root:
            root.get_children().delete()
        # Snippets (geen pagina's, dus niet meegenomen door page.delete())
        from blog.models import BlogCategorie
        from over.models import TeamLid
        BlogCategorie.objects.all().delete()
        TeamLid.objects.all().delete()
        # Placeholder afbeelding
        WagtailImage = get_image_model()
        WagtailImage.objects.filter(title="Fixture placeholder").delete()
        self.stdout.write("    Klaar.")

    def _maak_placeholder_afbeelding(self):
        from PIL import Image as PILImage, ImageDraw

        from django.core.files.storage import default_storage

        WagtailImage = get_image_model()
        existing = WagtailImage.objects.filter(title="Fixture placeholder").first()
        if existing:
            return existing

        # Maak een eenvoudig 800×600 grid-plaatje in de merkkleur
        img_width, img_height = 800, 600
        img = PILImage.new("RGB", (img_width, img_height), color=(26, 26, 26))
        draw = ImageDraw.Draw(img)
        for x in range(0, img_width, 80):
            draw.line([(x, 0), (x, img_height)], fill=(42, 42, 42), width=1)
        for y in range(0, img_height, 60):
            draw.line([(0, y), (img_width, y)], fill=(42, 42, 42), width=1)
        draw.rectangle([280, 220, 520, 380], fill=(200, 240, 77))
        draw.rectangle([300, 240, 500, 360], fill=(26, 26, 26))

        img_io = io.BytesIO()
        img.save(img_io, format="PNG")
        img_bytes = img_io.getvalue()

        # Sla het bestand op via default_storage (omzeilt Wagtail's pre_save chain)
        file_path = default_storage.save(
            "original_images/fixture-placeholder.png",
            ContentFile(img_bytes),
        )

        # bulk_create omzeilt Model.save() en de bijbehorende pre_save signalen
        # zodat width/height niet worden overschreven door update_dimension_fields
        placeholders = WagtailImage.objects.bulk_create([
            WagtailImage(
                title="Fixture placeholder",
                file=file_path,
                width=img_width,
                height=img_height,
                file_size=len(img_bytes),
            )
        ])
        return placeholders[0]

    def _maak_site(self, homepage):
        Site.objects.filter(is_default_site=True).delete()
        Site.objects.create(
            hostname="localhost",
            port=8000,
            root_page=homepage,
            is_default_site=True,
            site_name="Techture Media",
        )

    # ─── Pagina's ─────────────────────────────────────────────────────────────

    def _maak_homepage(self):
        from home.models import HomePage

        existing = HomePage.objects.first()
        if existing:
            self.stdout.write("    HomePage bestaat al — overgeslagen.")
            return existing

        root = Page.objects.filter(depth=1).first()
        homepage = HomePage(
            title="Techture Media",
            slug="home",
            hero_titel="Wij bouwen digitale ervaringen",
            hero_subtitel=(
                "Techture Media helpt ambitieuze bedrijven groeien met "
                "strategie, design en technologie."
            ),
            hero_cta_tekst="Bekijk ons werk",
            intro_titel="Wat wij doen",
            intro_tekst=(
                "<p>Wij zijn een full-service digital agency gespecialiseerd in "
                "webdesign, branding en online strategie. Van idee tot lancering — "
                "wij nemen je mee door het hele proces.</p>"
            ),
            diensten_sectie_titel="Onze diensten",
            blog_sectie_titel="Laatste artikelen",
            show_in_menus=False,
        )
        root.add_child(instance=homepage)
        return homepage

    def _maak_diensten(self, homepage):
        from diensten.models import DienstPagina, DienstenOverzichtPagina

        if DienstenOverzichtPagina.objects.exists():
            self.stdout.write("    Diensten bestaan al — overgeslagen.")
            return

        overzicht = DienstenOverzichtPagina(
            title="Diensten",
            slug="diensten",
            intro="<p>Ontdek wat Techture Media voor jouw bedrijf kan betekenen.</p>",
            show_in_menus=True,
        )
        homepage.add_child(instance=overzicht)

        diensten_data = [
            {
                "title": "Webdesign & Development",
                "slug": "webdesign",
                "korte_beschrijving": (
                    "Wij ontwerpen en bouwen websites die niet alleen mooi zijn, "
                    "maar ook écht converteren."
                ),
                "volgorde": 1,
            },
            {
                "title": "Branding & Identiteit",
                "slug": "branding",
                "korte_beschrijving": (
                    "Van logo tot merkstrategie — wij helpen je een sterk en "
                    "herkenbaar merk op te bouwen."
                ),
                "volgorde": 2,
            },
            {
                "title": "Online Strategie",
                "slug": "online-strategie",
                "korte_beschrijving": (
                    "SEO, content marketing en advertenties — een doordachte "
                    "online strategie zorgt voor duurzame groei."
                ),
                "volgorde": 3,
            },
        ]

        for data in diensten_data:
            dienst = DienstPagina(
                title=data["title"],
                slug=data["slug"],
                korte_beschrijving=data["korte_beschrijving"],
                volgorde=data["volgorde"],
                body=[
                    {
                        "type": "tekst",
                        "value": {
                            "inhoud": (
                                f"<h2>{data['title']}</h2>"
                                f"<p>{data['korte_beschrijving']}</p>"
                            )
                        },
                        "id": uid(),
                    }
                ],
            )
            overzicht.add_child(instance=dienst)

    def _maak_over_ons(self, homepage):
        from over.models import OverOnsPagina, TeamLid

        if OverOnsPagina.objects.exists():
            self.stdout.write("    Over ons pagina bestaat al — overgeslagen.")
            return

        over = OverOnsPagina(
            title="Over ons",
            slug="over-ons",
            intro=(
                "<p>Techture Media is opgericht met één doel: bedrijven helpen "
                "digitaal te groeien. Met een klein maar sterk team leveren wij "
                "werk van hoge kwaliteit.</p>"
            ),
            team_sectie_titel="Ons team",
            team_sectie_tonen=True,
            show_in_menus=True,
        )
        homepage.add_child(instance=over)

        teamleden = [
            {
                "naam": "Jordy Krudde",
                "functie": "Oprichter & Lead Developer",
                "bio": (
                    "<p>Jordy heeft meer dan 8 jaar ervaring in webdevelopment "
                    "en digitale strategie.</p>"
                ),
                "volgorde": 1,
            },
            {
                "naam": "Lisa van den Berg",
                "functie": "UX/UI Designer",
                "bio": (
                    "<p>Lisa combineert creativiteit met data-gedreven inzichten "
                    "om geweldige gebruikerservaringen te creëren.</p>"
                ),
                "volgorde": 2,
            },
        ]

        for data in teamleden:
            TeamLid.objects.create(
                naam=data["naam"],
                functie=data["functie"],
                bio=data["bio"],
                volgorde=data["volgorde"],
            )

    def _maak_blog(self, homepage):
        import datetime

        from blog.models import BlogArtikelPagina, BlogCategorie, BlogOverzichtPagina

        if BlogOverzichtPagina.objects.exists():
            self.stdout.write("    Blog pagina's bestaan al — overgeslagen.")
            return

        cat_design = BlogCategorie.objects.create(naam="Design", slug="design")
        cat_tech = BlogCategorie.objects.create(naam="Technologie", slug="technologie")

        overzicht = BlogOverzichtPagina(
            title="Blog",
            slug="blog",
            intro="<p>Tips, inzichten en nieuws vanuit Techture Media.</p>",
            artikelen_per_pagina=9,
            show_in_menus=True,
        )
        homepage.add_child(instance=overzicht)

        artikelen = [
            {
                "title": "5 redenen waarom dark mode populairder wordt",
                "slug": "dark-mode-populair",
                "datum": datetime.date(2025, 3, 15),
                "auteur": "Jordy Krudde",
                "intro": (
                    "Dark mode is niet langer een niche voorkeur — "
                    "het wordt de standaard. Maar waarom?"
                ),
                "categorie": cat_design,
            },
            {
                "title": "Waarom Wagtail de beste CMS-keuze is voor Django",
                "slug": "wagtail-beste-cms",
                "datum": datetime.date(2025, 2, 28),
                "auteur": "Jordy Krudde",
                "intro": (
                    "Na jaren werken met verschillende CMS-systemen zijn we "
                    "uitgekomen bij Wagtail. Dit is waarom."
                ),
                "categorie": cat_tech,
            },
            {
                "title": "Design tokens: de sleutel tot consistente UI",
                "slug": "design-tokens",
                "datum": datetime.date(2025, 1, 20),
                "auteur": "Lisa van den Berg",
                "intro": (
                    "Design tokens zorgen voor consistentie tussen ontwerp en code. "
                    "Zo zetten wij ze in."
                ),
                "categorie": cat_design,
            },
        ]

        for data in artikelen:
            artikel = BlogArtikelPagina(
                title=data["title"],
                slug=data["slug"],
                datum=data["datum"],
                auteur=data["auteur"],
                intro=data["intro"],
                categorie=data["categorie"],
                body=[
                    {
                        "type": "tekst",
                        "value": {
                            "inhoud": (
                                f"<p>{data['intro']}</p>"
                                "<p>Lees meer in het volledige artikel...</p>"
                            )
                        },
                        "id": uid(),
                    }
                ],
            )
            overzicht.add_child(instance=artikel)

    def _maak_contact(self, homepage):
        from contact.models import ContactFormulierVeld, ContactPagina

        if ContactPagina.objects.exists():
            self.stdout.write("    Contactpagina bestaat al — overgeslagen.")
            return

        contact = ContactPagina(
            title="Contact",
            slug="contact",
            intro="<p>Heb je een vraag of wil je samenwerken? Stuur ons een bericht.</p>",
            bedankt_tekst=(
                "<p>Bedankt voor je bericht! "
                "We nemen zo snel mogelijk contact op.</p>"
            ),
            to_address="hallo@techture.media",
            from_address="noreply@techture.media",
            subject="Nieuw bericht via techture.media",
            show_in_menus=True,
        )
        homepage.add_child(instance=contact)

        velden = [
            {"label": "Naam", "field_type": "singleline", "required": True},
            {"label": "E-mailadres", "field_type": "email", "required": True},
            {"label": "Telefoonnummer", "field_type": "singleline", "required": False},
            {"label": "Bericht", "field_type": "multiline", "required": True},
        ]
        for i, veld in enumerate(velden):
            ContactFormulierVeld.objects.create(
                page=contact,
                label=veld["label"],
                field_type=veld["field_type"],
                required=veld["required"],
                sort_order=i,
            )

    def _maak_blokken_testpagina(self, homepage):
        from core.models import BlokkenTestPagina

        if BlokkenTestPagina.objects.exists():
            self.stdout.write("    Blokken testpagina bestaat al — overgeslagen.")
            return

        img_pk = self.placeholder.pk

        body = [
            # ── 1. Hero ───────────────────────────────────────────────────────
            {
                "type": "hero",
                "value": {
                    "titel": "Hero blok demo",
                    "subtitel": "Een krachtige openingssectie met afbeelding en call-to-action",
                    "afbeelding": img_pk,
                    "cta_tekst": "Meer weten",
                    "cta_interne_link": None,
                    "cta_externe_link": "",
                },
                "id": uid(),
            },
            # ── 2. Richtext sectie ────────────────────────────────────────────
            {
                "type": "tekst",
                "value": {
                    "inhoud": (
                        "<h2>Tekstblok (RichText)</h2>"
                        "<p>Dit is een <strong>richtext</strong> sectieblok. "
                        "Je kunt hier <em>cursief</em>, koppen, "
                        "<a href='#'>links</a> en lijsten toevoegen.</p>"
                        "<ul>"
                        "<li>Eerste opsommingspunt</li>"
                        "<li>Tweede opsommingspunt</li>"
                        "<li>Derde opsommingspunt</li>"
                        "</ul>"
                    )
                },
                "id": uid(),
            },
            # ── 3. Afbeelding ─────────────────────────────────────────────────
            {
                "type": "afbeelding",
                "value": {
                    "afbeelding": img_pk,
                    "bijschrift": "Dit is het bijschrift van de afbeelding",
                    "alt_tekst": "Placeholder afbeelding voor demo",
                },
                "id": uid(),
            },
            # ── 4. Twee kolommen ──────────────────────────────────────────────
            {
                "type": "twee_kolommen",
                "value": {
                    "linker_kolom": (
                        "<h3>Linker kolom</h3>"
                        "<p>Tekst in de linker kolom. Hier kun je uitleg of "
                        "voordelen kwijt die naast de rechter kolom staan.</p>"
                    ),
                    "rechter_kolom": (
                        "<h3>Rechter kolom</h3>"
                        "<p>Tekst in de rechter kolom. Gebruik dit blok voor "
                        "vergelijkingen of twee gerelateerde onderwerpen.</p>"
                    ),
                },
                "id": uid(),
            },
            # ── 5. Citaat ─────────────────────────────────────────────────────
            {
                "type": "citaat",
                "value": {
                    "citaat": (
                        "Kwaliteit is geen toeval — het is altijd het resultaat "
                        "van slimme inspanning."
                    ),
                    "auteur": "Jordy Krudde",
                    "functie": "Oprichter, Techture Media",
                },
                "id": uid(),
            },
            # ── 6. Call to action ─────────────────────────────────────────────
            {
                "type": "call_to_action",
                "value": {
                    "titel": "Klaar om te starten?",
                    "tekst": (
                        "Neem contact op en ontdek wat Techture Media "
                        "voor jou kan betekenen."
                    ),
                    "knop_tekst": "Neem contact op",
                    "knop_link": "https://techture.media/contact/",
                    "stijl": "accent",
                },
                "id": uid(),
            },
            # ── 7. Video ──────────────────────────────────────────────────────
            {
                "type": "video",
                "value": {
                    "video": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    "bijschrift": "Demo video — vervang dit door een echte video-URL",
                },
                "id": uid(),
            },
            # ── 8. Projecten raster ───────────────────────────────────────────
            {
                "type": "project_raster",
                "value": {
                    "titel": "Recente projecten",
                    "projecten": [
                        {
                            "type": "item",
                            "value": {
                                "titel": "Project Alpha",
                                "subtitel": "Webdesign & Branding",
                                "thumbnail": img_pk,
                                "tags": ["Branding", "Website", "Strategie"],
                                "link_pagina": None,
                                "link_url": "",
                            },
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {
                                "titel": "Project Beta",
                                "subtitel": "E-commerce platform",
                                "thumbnail": img_pk,
                                "tags": ["Development", "UX/UI"],
                                "link_pagina": None,
                                "link_url": "",
                            },
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {
                                "titel": "Project Gamma",
                                "subtitel": "Online marketing campagne",
                                "thumbnail": img_pk,
                                "tags": ["Marketing", "SEO"],
                                "link_pagina": None,
                                "link_url": "",
                            },
                            "id": uid(),
                        },
                    ],
                },
                "id": uid(),
            },
            # ── 9. Diensten raster ────────────────────────────────────────────
            {
                "type": "diensten_raster",
                "value": {
                    "titel": "Onze diensten",
                    "diensten": [
                        {
                            "type": "item",
                            "value": {
                                "icoon": img_pk,
                                "titel": "Webdesign",
                                "beschrijving": (
                                    "Wij bouwen snelle, toegankelijke websites "
                                    "die converteren."
                                ),
                                "bullet_points": [
                                    "Responsive design",
                                    "SEO-geoptimaliseerd",
                                    "Snelle laadtijd",
                                ],
                                "link_pagina": None,
                            },
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {
                                "icoon": img_pk,
                                "titel": "Branding",
                                "beschrijving": (
                                    "Van logo tot complete merkidentiteit — "
                                    "wij bouwen sterke merken."
                                ),
                                "bullet_points": [
                                    "Logo design",
                                    "Huisstijl",
                                    "Merkstrategie",
                                ],
                                "link_pagina": None,
                            },
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {
                                "icoon": img_pk,
                                "titel": "Online Strategie",
                                "beschrijving": (
                                    "Doordachte digitale strategie voor "
                                    "duurzame online groei."
                                ),
                                "bullet_points": [
                                    "SEO & content",
                                    "Analytics",
                                    "Advertenties",
                                ],
                                "link_pagina": None,
                            },
                            "id": uid(),
                        },
                    ],
                },
                "id": uid(),
            },
            # ── 10. Statistieken ──────────────────────────────────────────────
            {
                "type": "statistieken",
                "value": {
                    "titel": "Onze resultaten",
                    "statistieken": [
                        {
                            "type": "item",
                            "value": {
                                "klant_logo": None,
                                "getal": "50+",
                                "label": "Afgeronde projecten",
                                "beschrijving": "Van kleine bedrijven tot grote merken.",
                            },
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {
                                "klant_logo": None,
                                "getal": "98%",
                                "label": "Tevreden klanten",
                                "beschrijving": "Op basis van klantbeoordelingen.",
                            },
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {
                                "klant_logo": None,
                                "getal": "8jr",
                                "label": "Ervaring",
                                "beschrijving": "Jarenlange expertise in digital.",
                            },
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {
                                "klant_logo": None,
                                "getal": "€2M+",
                                "label": "Omzet gegenereerd",
                                "beschrijving": "Voor onze klanten samen.",
                            },
                            "id": uid(),
                        },
                    ],
                },
                "id": uid(),
            },
            # ── 11. Testimonial ───────────────────────────────────────────────
            {
                "type": "testimonial",
                "value": {
                    "citaat": (
                        "Techture Media heeft onze online aanwezigheid volledig "
                        "getransformeerd. Van strategie tot uitvoering — een team "
                        "dat écht meedenkt."
                    ),
                    "naam_auteur": "Jan de Vries",
                    "rol_auteur": "CEO, Voorbeeld BV",
                    "foto_auteur": img_pk,
                },
                "id": uid(),
            },
            # ── 12. Logo strip ────────────────────────────────────────────────
            {
                "type": "logo_strip",
                "value": {
                    "titel": "Zij gingen je voor",
                    "logos": [
                        {
                            "type": "item",
                            "value": {"afbeelding": img_pk, "alt_tekst": "Klant A"},
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {"afbeelding": img_pk, "alt_tekst": "Klant B"},
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {"afbeelding": img_pk, "alt_tekst": "Klant C"},
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {"afbeelding": img_pk, "alt_tekst": "Klant D"},
                            "id": uid(),
                        },
                    ],
                },
                "id": uid(),
            },
            # ── 13. FAQ ───────────────────────────────────────────────────────
            {
                "type": "faq",
                "value": {
                    "titel": "Veelgestelde vragen",
                    "items": [
                        {
                            "type": "item",
                            "value": {
                                "vraag": "Wat zijn de kosten van een website?",
                                "antwoord": (
                                    "<p>De kosten variëren afhankelijk van de "
                                    "complexiteit en wensen. We maken graag een "
                                    "offerte op maat.</p>"
                                ),
                            },
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {
                                "vraag": "Hoe lang duurt het om een website te bouwen?",
                                "antwoord": (
                                    "<p>Een gemiddeld project neemt "
                                    "<strong>4 tot 8 weken</strong> in beslag, "
                                    "afhankelijk van omvang en beschikbaarheid "
                                    "voor feedback.</p>"
                                ),
                            },
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {
                                "vraag": "Bieden jullie ook onderhoud aan?",
                                "antwoord": (
                                    "<p>Ja! Na oplevering bieden we "
                                    "onderhoudscontracten aan zodat jouw website "
                                    "altijd up-to-date en veilig blijft.</p>"
                                ),
                            },
                            "id": uid(),
                        },
                    ],
                },
                "id": uid(),
            },
            # ── 14. Genummerde kenmerken ──────────────────────────────────────
            {
                "type": "genummerde_kenmerken",
                "value": {
                    "titel": "Waarom Techture Media?",
                    "items": [
                        {
                            "type": "item",
                            "value": {
                                "nummer": "01",
                                "titel": "Strategie eerst",
                                "beschrijving": (
                                    "We beginnen altijd met een doordachte "
                                    "strategie, niet met pixels."
                                ),
                            },
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {
                                "nummer": "02",
                                "titel": "Design dat converteert",
                                "beschrijving": (
                                    "Mooi is goed, maar functioneel en "
                                    "converterend is beter."
                                ),
                            },
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {
                                "nummer": "03",
                                "titel": "Schone code",
                                "beschrijving": (
                                    "Wij schrijven code die schaalbaar, "
                                    "onderhoudbaar en snel is."
                                ),
                            },
                            "id": uid(),
                        },
                        {
                            "type": "item",
                            "value": {
                                "nummer": "04",
                                "titel": "Langetermijnpartner",
                                "beschrijving": (
                                    "We zijn geen leverancier maar een partner "
                                    "in jouw digitale groei."
                                ),
                            },
                            "id": uid(),
                        },
                    ],
                },
                "id": uid(),
            },
            # ── 15. Contact CTA ───────────────────────────────────────────────
            {
                "type": "contact_cta",
                "value": {
                    "koptekst": "Laten we samenwerken",
                    "subtekst": "Heb je een project in gedachten? We horen het graag.",
                    "contact_naam": "Jordy Krudde",
                    "contact_rol": "Oprichter & Lead Developer",
                    "contact_foto": img_pk,
                    "email": "hallo@techture.media",
                    "telefoon": "+31 6 00 00 00 00",
                },
                "id": uid(),
            },
        ]

        testpagina = BlokkenTestPagina(
            title="Blokken testpagina",
            slug="blokken-test",
            body=body,
        )
        homepage.add_child(instance=testpagina)
