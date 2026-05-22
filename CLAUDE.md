# Claude Code – Techture Media website

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
| `home`     | `HomePage` – startpagina                        |
| `diensten` | `DienstenOverzichtPagina`, `DienstPagina`       |
| `over`     | `OverOnsPagina` + `TeamLid` snippet             |
| `blog`     | `BlogOverzichtPagina`, `BlogArtikelPagina`      |
| `contact`  | `ContactPagina` (Wagtail FormBuilder)           |
| `core`     | Abstracte `BasePage`, alle StreamField blokken  |
| `search`   | Zoekview                                         |

## Paginahiërarchie (Wagtail page tree)

```
Root
└── HomePage
    ├── DienstenOverzichtPagina
    │   └── DienstPagina (meerdere)
    ├── OverOnsPagina
    ├── BlogOverzichtPagina
    │   └── BlogArtikelPagina (meerdere)
    ├── ContactPagina
    └── BlokkenTestPagina  (aangemaakt via make fixtures)
```

## Conventies

- Alle paginamodellen erven van `core.models.BasePage` (behalve `ContactPagina` → `AbstractEmailForm`).
- Nieuwe paginatypen: voeg toe als subpage_type bij de juiste ouder.
- Alle StreamField blokken staan in `core/blocks.py`.
- Nieuwe blokken: voeg toe aan `STANDARD_BLOCKS` én maak een template in `core/templates/blocks/`.
- Alle labels, verbose_name en help_text in het **Nederlands**.
- Geen logica in templates – alleen weergave.
- SEO-velden (`seo_description`, `og_image`) zitten op elke pagina via `BasePage` of handmatig op `ContactPagina`.

## Snippets

| Snippet         | App    | Beheerd via          |
|-----------------|--------|----------------------|
| `TeamLid`       | over   | Wagtail Snippets     |
| `BlogCategorie` | blog   | Wagtail Snippets     |

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
make fixtures       # Demo-pagina's en blokken-testinhoud aanmaken
make fixtures-leeg  # Bestaande inhoud verwijderen en opnieuw aanmaken
make up             # Docker containers starten
make down           # Docker containers stoppen
make fresh          # Installeer + migreer + start
make dfixtures      # Fixtures in Docker container aanmaken
```

## Wat NIET te doen

- **Geen logica in templates** – queries en berekeningen horen in modellen of views.
- **Geen hardcoded instellingen** – gebruik `.env` + `os.environ` voor productiewaarden.
- **Niet rechtstreeks van `Page` erven** (tenzij noodzakelijk zoals bij `AbstractEmailForm`).
- **Geen nieuwe blokken buiten `core/blocks.py`**.
- **Nooit `DEBUG = True` in productie**.
- **Geen migraties handmatig bewerken**.
