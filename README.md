# Techture Media – Website

Portfolio/agency website gebouwd met Django 5 + Wagtail 6.

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
2. **Paginastructuur aanmaken** (in volgorde):
   - Maak `HomePage` aan als rootpagina
   - Voeg `DienstenOverzichtPagina` toe als kind
   - Voeg `OverOnsPagina` toe als kind
   - Voeg `BlogOverzichtPagina` toe als kind
   - Voeg `ContactPagina` toe als kind (incl. formuliervelden + e-mailinstellingen)
3. **Navigatie**: zet *Toon in menu* aan bij de gewenste pagina's (SEO-tabblad).
4. **Blog**: voeg categorieën toe via Snippets → Blogcategorieën.
5. **Team**: voeg teamleden toe via Snippets → Teamleden.

## Projectstructuur

```
techture_media/
├── blog/           # BlogOverzichtPagina + BlogArtikelPagina + BlogCategorie snippet
├── contact/        # ContactPagina met Wagtail FormBuilder
├── core/           # BasePage (abstract) + STANDARD_BLOCKS + navigatietag
├── diensten/       # DienstenOverzichtPagina + DienstPagina
├── home/           # HomePage
├── over/           # OverOnsPagina + TeamLid snippet
├── search/         # Zoekview
├── templates/      # base.html, 404.html, 500.html
├── static/
│   ├── css/main.css
│   └── js/main.js
└── techture_media/ # Django projectconfiguratie + settings
```

## Beschikbare StreamField blokken

| Blok             | Beschrijving                                    |
|------------------|-------------------------------------------------|
| `hero`           | Grote uitgelichte sectie met afbeelding + knop  |
| `tekst`          | Rich text (h2, h3, bold, italic, links, lijsten)|
| `afbeelding`     | Afbeelding met bijschrift en alt-tekst          |
| `twee_kolommen`  | Twee rich text kolommen naast elkaar            |
| `citaat`         | Citaatblok met auteur en functie               |
| `call_to_action` | CTA-sectie in light/dark/accent stijl          |
| `video`          | Ingesloten video (YouTube, Vimeo, etc.)         |

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
gunicorn techture_media.wsgi:application --bind 0.0.0.0:8000 --workers 3
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
- [ ] Formuliervelden aangemaakt op de ContactPagina
- [ ] `to_address` ingevuld op de ContactPagina
