# Claude Code – Runclub website

Lees dit bestand altijd eerst voordat je wijzigingen aanbrengt in dit project.
Lees ook **DESIGN.md** voor het volledige design systeem, kleurpalet, typografie en overzicht van beschikbare blokken.

## Stack

| Onderdeel      | Versie/keuze                           |
|----------------|----------------------------------------|
| Python         | 3.12                                   |
| Django         | 5.x                                    |
| Wagtail        | 6.x                                    |
| Database       | SQLite (lokaal), PostgreSQL (productie)|
| Static files   | WhiteNoise (productie)                 |
| Containerisatie| Docker + docker-compose                |

## Apps en verantwoordelijkheden

| App        | Paginatype(s)                                    |
|------------|--------------------------------------------------|
| `home`     | `HomePage` – startpagina (root)                 |
| `core`     | Abstracte `BasePage`, alle StreamField blokken  |
| `search`   | Zoekview                                         |

## Paginahiërarchie (Wagtail page tree)

```
Root
└── HomePage
```

Nieuwe pagina's worden toegevoegd als `subpage_type` van `HomePage` (of van
elkaar) zodra er nieuwe paginatypen nodig zijn.

## Conventies

- Alle paginamodellen erven van `core.models.BasePage` (tenzij er een
  Django-beperking is, zoals bij formulieren via `AbstractEmailForm`).
- Nieuwe paginatypen: voeg toe als subpage_type bij de juiste ouder.
- Alle StreamField blokken staan in `core/blocks.py`.
- Nieuwe blokken: voeg toe aan `STANDARD_BLOCKS` én maak een template in `core/templates/blocks/`.
- Nieuwe code (labels, verbose_name, help_text, comments, identifiers) in het **Engels**.
  Bestaande Nederlandse namen hoeven niet meegenomen te worden, maar pas ze
  aan naar het Engels als je een blok/model toch al wijzigt.
- Git commit messages in het **Engels**.
- Geen logica in templates – alleen weergave.
- SEO-velden (`seo_description`, `og_image`) zitten op elke pagina via `BasePage`.

## Navigatie

De hoofdnavigatie gebruikt Wagtail's `show_in_menus` vlag. Zet dit aan per pagina in het SEO-tabblad. De template tag `{% get_navigatie %}` uit `navigatie_tags` verzorgt de rendering.

## Veelgebruikte make commando's

```bash
make install        # Afhankelijkheden installeren
make run            # Ontwikkelserver starten
make migrations     # Migraties aanmaken
make migrate        # Migraties uitvoeren
make superuser      # Beheerdersaccount aanmaken
make shell          # Django shell
make collectstatic  # Statische bestanden verzamelen
make up             # Docker containers starten
make down           # Docker containers stoppen
make fresh          # Installeer + migreer + start
```

Daarnaast: `python manage.py build_runclub_home` vult de homepage met de
content/blokken volgens het Bolt Run Club Stitch-ontwerp.

## Wat NIET te doen

- **Geen logica in templates** – queries en berekeningen horen in modellen of views.
- **Geen hardcoded instellingen** – gebruik `.env` + `os.environ` voor productiewaarden.
- **Niet rechtstreeks van `Page` erven** (tenzij noodzakelijk zoals bij `AbstractEmailForm`).
- **Geen nieuwe blokken buiten `core/blocks.py`**.
- **Nooit `DEBUG = True` in productie**.
- **Geen migraties handmatig bewerken**.
