"""
Management command: build_runclub_home

Vult de startpagina met de inhoud van het Stitch-ontwerp "BOLT RUN CLUB - Home":
hero, statistieken-ticker, evenementen, routes, doel-tracker en nieuwsbrief-CTA.

Gebruik:
    python manage.py build_runclub_home
    python manage.py build_runclub_home --leeg   # body eerst leegmaken
"""

import io
import uuid

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from wagtail.images import get_image_model
from wagtail.models import Page, Site


def uid():
    """Genereer een uniek ID voor een StreamField blok."""
    return str(uuid.uuid4())


class Command(BaseCommand):
    help = "Vul de startpagina met de Bolt Run Club homepage-inhoud."

    def add_arguments(self, parser):
        parser.add_argument(
            "--leeg",
            action="store_true",
            help="Maak de body van de startpagina eerst leeg.",
        )

    def handle(self, *args, **options):
        from home.models import HomePage

        bestaande_homepage = HomePage.objects.first()
        if bestaande_homepage and bestaande_homepage.body and not options["leeg"]:
            self.stdout.write(
                self.style.SUCCESS(
                    "Startpagina heeft al inhoud — build_runclub_home overgeslagen."
                )
            )
            return

        self.stdout.write("⏳  Placeholder afbeelding aanmaken...")
        self.placeholder = self._maak_placeholder_afbeelding()

        self.stdout.write("⏳  Startpagina ophalen of aanmaken...")
        homepage = self._maak_homepage()

        if options["leeg"]:
            homepage.body = []

        self.stdout.write("⏳  Inhoud opbouwen...")
        homepage.body = self._bouw_body()
        homepage.save_revision().publish()

        self.stdout.write("⏳  Wagtail site instellen...")
        self._maak_site(homepage)

        self.stdout.write(self.style.SUCCESS("\n✅  Bolt Run Club homepage succesvol opgebouwd!"))
        self.stdout.write(f"    Startpagina ID : {homepage.pk}")

    # ─── Hulpfuncties ─────────────────────────────────────────────────────────

    def _maak_placeholder_afbeelding(self):
        from PIL import Image as PILImage, ImageDraw

        WagtailImage = get_image_model()
        existing = WagtailImage.objects.filter(title="Bolt placeholder").first()
        if existing:
            return existing

        img_width, img_height = 1200, 1200
        img = PILImage.new("RGB", (img_width, img_height), color=(28, 27, 27))
        draw = ImageDraw.Draw(img)
        for x in range(0, img_width, 80):
            draw.line([(x, 0), (x, img_height)], fill=(60, 60, 60), width=1)
        for y in range(0, img_height, 80):
            draw.line([(0, y), (img_width, y)], fill=(60, 60, 60), width=1)
        margin = img_width // 4
        draw.rectangle(
            [margin, margin, img_width - margin, img_height - margin],
            fill=(204, 255, 0),
        )

        img_io = io.BytesIO()
        img.save(img_io, format="PNG")
        img_bytes = img_io.getvalue()

        file_path = default_storage.save(
            "original_images/bolt-placeholder.png",
            ContentFile(img_bytes),
        )

        placeholders = WagtailImage.objects.bulk_create([
            WagtailImage(
                title="Bolt placeholder",
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
            site_name="Bolt Run Club",
        )

    def _maak_homepage(self):
        from home.models import HomePage

        existing = HomePage.objects.first()
        if existing:
            self.stdout.write("    HomePage bestaat al — hergebruiken.")
            return existing

        root = Page.objects.filter(depth=1).first()

        # Verwijder Wagtail's standaard "Welcome to your new Wagtail site!"-pagina.
        for kind in root.get_children():
            if kind.slug == "home":
                kind.delete()
        root.refresh_from_db()

        homepage = HomePage(
            title="Bolt Run Club",
            slug="home",
            show_in_menus=False,
        )
        root.add_child(instance=homepage)
        return homepage

    # ─── Body opbouwen ────────────────────────────────────────────────────────

    def _bouw_body(self):
        return [
            self._hero(),
            self._statistieken(),
            self._evenementen_raster(),
            self._routes_raster(),
            self._doel_tracker(),
            self._nieuwsbrief_cta(),
        ]

    def _hero(self):
        return {
            "id": uid(),
            "type": "hero",
            "value": {
                "badge_tekst": "Est. 2024 / Urban Athletics",
                "titel": "RUN FASTER. TOGETHER.",
                "subtitel": (
                    "The ultimate endorphin-driven community for urban runners. "
                    "Whether you're chasing a PR or just the post-run pizza, "
                    "there's a pace for you here."
                ),
                "afbeelding": self.placeholder.pk,
                "cta_tekst": "Join the Pack",
                "cta_interne_link": None,
                "cta_externe_link": "#",
                "secundaire_cta_tekst": "View Calendar",
                "secundaire_cta_interne_link": None,
                "secundaire_cta_externe_link": "#",
            },
        }

    def _statistieken(self):
        statistieken = [
            ("5,240", "Miles Run This Year"),
            ("42", "Active Members"),
            ("12", "Weekly Pizza Runs"),
        ]
        return {
            "id": uid(),
            "type": "statistieken",
            "value": {
                "titel": "",
                "statistieken": [
                    {
                        "id": uid(),
                        "type": "item",
                        "value": {
                            "klant_logo": None,
                            "getal": getal,
                            "label": label,
                            "beschrijving": "",
                        },
                    }
                    for getal, label in statistieken
                ],
            },
        }

    def _evenementen_raster(self):
        events = [
            {
                "categorie_tag": "TEMPO RUN",
                "titel": "Tempo Tuesday",
                "locatie": "Westside Pier 42",
                "datum_maand": "OCT",
                "datum_dag": "12",
                "tijd": "7:00 PM",
                "niveau": "Intermediate",
            },
            {
                "categorie_tag": "TRAIL RUN",
                "titel": "Canyon Loop",
                "locatie": "Griffith Park South",
                "datum_maand": "OCT",
                "datum_dag": "14",
                "tijd": "6:30 AM",
                "niveau": "Difficult",
            },
            {
                "categorie_tag": "SOCIAL 5K",
                "titel": "Sunday Slice",
                "locatie": "Bolt Clubhouse",
                "datum_maand": "OCT",
                "datum_dag": "17",
                "tijd": "10:00 AM",
                "niveau": "All Levels",
            },
        ]
        return {
            "id": uid(),
            "type": "evenementen_raster",
            "value": {
                "label": "Don't Miss Out",
                "titel": "Upcoming Events",
                "link_tekst": "View Full Calendar",
                "link_url": "",
                "events": [
                    {
                        "id": uid(),
                        "type": "item",
                        "value": {
                            "afbeelding": self.placeholder.pk,
                            "categorie_tag": event["categorie_tag"],
                            "titel": event["titel"],
                            "locatie": event["locatie"],
                            "datum_maand": event["datum_maand"],
                            "datum_dag": event["datum_dag"],
                            "tijd": event["tijd"],
                            "niveau": event["niveau"],
                            "knop_tekst": "RSVP NOW",
                            "knop_link": "",
                        },
                    }
                    for event in events
                ],
            },
        }

    def _routes_raster(self):
        routes = [
            ("FLAT & FAST", "The Riverside 5K"),
            ("STAIR CLIMBS", "Urban Peak 8K"),
            ("SCENIC", "Park Perimeter"),
        ]
        return {
            "id": uid(),
            "type": "routes_raster",
            "value": {
                "label": "The City is our Track",
                "titel": "Our Top Routes",
                "tekst": (
                    "We've mapped out the best urban circuits, elevation "
                    "challenges, and scenic paths in the neighborhood. "
                    "High performance, zero boredom."
                ),
                "routes": [
                    {
                        "id": uid(),
                        "type": "item",
                        "value": {
                            "afbeelding": self.placeholder.pk,
                            "tag": tag,
                            "titel": titel,
                        },
                    }
                    for tag, titel in routes
                ],
            },
        }

    def _doel_tracker(self):
        return {
            "id": uid(),
            "type": "doel_tracker",
            "value": {
                "titel": "Club Goal Tracker",
                "beschrijving": "We're aiming for 10,000 miles by year-end. Every stride counts!",
                "voortgang_label": "Current Progress",
                "percentage": 52,
                "huidige_label": "0 MILES",
                "doel_label": "10,000 MILES",
            },
        }

    def _nieuwsbrief_cta(self):
        return {
            "id": uid(),
            "type": "nieuwsbrief_cta",
            "value": {
                "titel": "READY TO\nFIND YOUR PACE?",
                "tekst": (
                    "Membership is free. The vibes are unmatched. Sign up for "
                    "our newsletter to get weekly route updates and event invites."
                ),
                "afbeelding": self.placeholder.pk,
                "placeholder_tekst": "YOUR EMAIL ADDRESS",
                "knop_tekst": "SIGN UP",
            },
        }
