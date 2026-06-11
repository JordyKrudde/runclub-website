# Runclub – Website

Website voor Runclub, gebouwd met Django 5 + Wagtail 6. Gebaseerd op het
Techture Media Wagtail-projecttemplate.

## Lokaal opstarten

```bash
# 1. Virtuele omgeving aanmaken en activeren
python -m venv .venv
source .venv/bin/activate

# 2. Afhankelijkheden installeren + migreren + starten
make fresh

# 3. Beheerdersaccount aanmaken
make superuser
```

Ga naar `http://localhost:8000/admin/` om in te loggen.

## Opstarten met Docker

```bash
make docker-up
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

## Eerste keer instellen in Wagtail admin

Na het aanmaken van een supergebruiker:

1. **Site instellen** → `/admin/sites/` → stel hostname en rootpagina in.
2. **Homepage**: `HomePage` is de rootpagina en bevat de StreamField `body`
   met alle secties.
3. **Navigatie**: zet *Toon in menu* aan bij de gewenste pagina's (SEO-tabblad).

## Projectstructuur

```
runclub/
├── core/           # BasePage (abstract) + STANDARD_BLOCKS + navigatietag
├── home/           # HomePage (rootpagina)
├── search/         # Zoekview
├── templates/      # base.html, 404.html, 500.html
├── static/
│   ├── css/main.css
│   └── js/main.js
└── runclub/        # Django projectconfiguratie + settings
```

## Beschikbare StreamField blokken

| Blok                  | Beschrijving                                       |
|-----------------------|------------------------------------------------------|
| `hero`                | Grote uitgelichte sectie met afbeelding + knop(pen)  |
| `tekst`               | Rich text (h2, h3, bold, italic, links, lijsten)     |
| `afbeelding`          | Afbeelding met bijschrift en alt-tekst               |
| `twee_kolommen`       | Twee rich text kolommen naast elkaar                 |
| `citaat`              | Citaatblok met auteur en functie                    |
| `call_to_action`      | CTA-sectie in light/dark/accent stijl               |
| `video`               | Ingesloten video (YouTube, Vimeo, etc.)              |
| `project_raster`      | Raster van projectkaarten                            |
| `diensten_raster`     | Raster van dienstkaarten                             |
| `statistieken`        | Statistieken-sectie / ticker                         |
| `testimonial`         | Uitgebreid klantcitaat met foto                      |
| `logo_strip`          | Horizontale rij van logo's                           |
| `faq`                 | Inklapbare FAQ-sectie                                |
| `genummerde_kenmerken`| Genummerd raster van voordelen                       |
| `contact_cta`         | Persoonlijk contactblok                              |
| `evenementen_raster`  | Raster van aankomende events met RSVP                |
| `routes_raster`       | Raster van routekaarten                              |
| `doel_tracker`        | Voortgangsbalk richting een doel                     |
| `nieuwsbrief_cta`      | Nieuwsbrief-aanmeldsectie met afbeelding             |

## Productie deployment

```bash
# Omgevingsvariabelen instellen
cp .env.example .env
# Vul .env in met productiewaarden

# Installeren, collectstatic en migreren
pip install -r requirements/production.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Starten via Gunicorn
gunicorn runclub.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### Livegang checklist

- [ ] `DJANGO_SECRET_KEY` is uniek en veilig
- [ ] `DEBUG=False` (geborgd via production.py)
- [ ] `DJANGO_ALLOWED_HOSTS` bevat het juiste domein
- [ ] PostgreSQL bereikbaar en gemigreerd
- [ ] HTTPS geconfigureerd op reverse proxy
- [ ] E-mailconfiguratie getest
- [ ] `collectstatic` uitgevoerd
- [ ] Siteconfiguratie ingesteld in Wagtail admin (`/admin/sites/`)
