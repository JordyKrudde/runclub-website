# Bolt Run Club – Design Systeem

Dit bestand wordt automatisch geladen in elke Claude Code sessie. Gebruik het als referentie bij het bouwen of stylen van componenten.

Stijl: neo-brutalist, energiek, gebaseerd op het Stitch-ontwerp "BOLT RUN CLUB - Home"
(harde randen, "hard shadow"-effecten, skew-boxes, felle limoenkleur).

---

## Kleurenpalet

| CSS Variable          | Hex       | Gebruik                                      |
|-----------------------|-----------|------------------------------------------------|
| `--color-bg`          | `#fcf9f8` | Basis achtergrond (lichte surface)            |
| `--color-bg-alt`      | `#f0edec` | Kaarten, secties, afwisselende achtergrond    |
| `--color-bg-raised`   | `#ebe7e7` | Hover-states, balken, actieve elementen       |
| `--color-text`        | `#1c1b1b` | Primaire tekst, harde randen — bijna zwart    |
| `--color-text-muted`  | `#444933` | Secundaire tekst — meta, beschrijvingen       |
| `--color-text-faint`  | `#747a60` | Placeholders, decoratieve labels              |
| `--color-accent`      | `#ccff00` | Fel limoen — CTAs, badges, highlights         |
| `--color-accent-dark` | `#abd600` | Hover-state van accent                        |
| `--color-on-accent`   | `#5b7300` | Tekst/iconen op een limoen achtergrond        |
| `--color-secondary`   | `#bacfff` | Lichtblauw — secundaire badges (niveau)       |
| `--color-on-secondary`| `#435881` | Tekst op secundaire badges                    |
| `--color-border`      | `#1c1b1b` | Harde 2px randen rond kaarten en knoppen      |

**Regels:**
- Gebruik nooit hardcoded hex-waarden in CSS — altijd `var(--color-*)`.
- Primaire actiekleur is altijd `--color-accent` (fel limoen op donkere/lichte achtergrond).
- Randen zijn standaard `2px solid var(--color-border)`, gecombineerd met `--shadow-hard`.

---

## Typografie

| Font            | CSS Variable     | Gebruik                                   |
|-----------------|------------------|---------------------------------------------|
| Anton           | `--font-display` | Koppen (h1–h3), knoppen, grote getallen     |
| Archivo Narrow  | `--font-label`   | Uppercase labels, navigatie, badges (bold)  |
| Lexend          | `--font-body`    | Lopende tekst                               |

Laad deze fonts via Google Fonts in `templates/base.html` (Anton, Archivo Narrow 700, Lexend 400/700)
plus Material Symbols Outlined voor iconen.

| Variable        | Waarde     | Gebruik                                  |
|-----------------|------------|--------------------------------------------|
| `--text-xs`     | 0.75rem    | Labels, badges, kleine meta              |
| `--text-sm`     | 0.875rem   | Label-caps, navigatielinks, knoppen      |
| `--text-base`   | 1rem       | Standaard alineatekst (body-md)          |
| `--text-lg`     | 1.125rem   | Intro's, grotere body-tekst (body-lg)    |
| `--text-xl`     | 1.5rem     | Kaarttitels (headline-md)                |
| `--text-2xl`    | 2rem       | Grote statistieken (stats-number)        |
| `--text-3xl`    | 2.5rem     | H2 koppen, sectietitels (headline-lg)    |
| `--text-4xl`    | 3rem       | Hero-titel mobiel (display-xl-mobile)    |
| `--text-5xl`    | 5.25rem    | Hero-titel desktop (display-xl)          |

**Regels:**
- Koppen (`h1`–`h3`) zijn altijd `font-family: var(--font-display)`, `text-transform: uppercase`, `line-height: 1`.
- Labels/badges/navigatie gebruiken `var(--font-label)`, `font-weight: 700`, `letter-spacing: var(--letter-spacing-caps)`, `text-transform: uppercase`.
- Gebruik `clamp()` voor vloeiende responsieve koppen (zie `main.css`).

---

## Spacing systeem

Gebruik altijd een spacing-token uit `design-system.css`. Schrijf nooit `margin: 24px` — schrijf `var(--space-6)`.

| Variable     | Waarde  |
|--------------|---------|
| `--space-1`  | 0.25rem |
| `--space-2`  | 0.5rem  |
| `--space-3`  | 0.75rem |
| `--space-4`  | 1rem    |
| `--space-6`  | 1.5rem  |
| `--space-8`  | 2rem    |
| `--space-12` | 3rem    |
| `--space-16` | 4rem    |
| `--space-20` | 5rem    |
| `--space-24` | 6rem    |
| `--space-32` | 8rem    |

Secties gebruiken `padding-block: var(--space-20)` als standaard verticale marge.

---

## Lay-out & neo-brutalist utilities

| Variable                | Waarde                          | Gebruik                          |
|-------------------------|----------------------------------|------------------------------------|
| `--container-max`       | 1280px                           | Max-breedte van alle containers   |
| `--container-padding`   | 1.5rem                           | Horizontale pagina-marge          |
| `--radius-sm`           | 2px                              | Knoppen, badges                   |
| `--radius-md`           | 4px                              | Kleine elementen                  |
| `--radius-lg`           | 8px                              | -                                  |
| `--radius-full`         | 12px                             | -                                  |
| `--shadow-hard`         | `6px 6px 0 0 var(--color-border)`| Standaard "hard shadow" op kaarten/knoppen |
| `--shadow-hard-hover`   | `10px 10px 0 0 var(--color-border)` | Hover-state van hard shadow    |
| `--shadow-hard-primary` | `6px 6px 0 0 var(--color-accent)`| Hard shadow in accentkleur (CTA-blokken) |
| `--skew-angle`          | `-3deg`                          | Gebruikt door `.skew-box`/`.unskew` |

**Utility classes** (gedefinieerd in `main.css`):
- `.skew-box` / `.unskew` — schuine "neo-brutalist" kaders; binnenste content krijgt `.unskew` om weer recht te staan.
- `.hard-shadow` / `.hard-shadow-primary` — harde slagschaduw zonder blur.
- `.card-hover` — verschuift de kaart bij hover en vergroot de slagschaduw.

**Responsieve breekpunten:**
- `768px` — mobiel (hamburger menu, éénkoloms layout)
- `1024px` — tablet (enkele grid-aanpassingen)

---

## CSS-naamgeving (BEM)

```
.blok-naam               → block
.blok-naam__element      → element
.blok-naam--modifier     → modifier
```

**Voorbeelden:**
```css
.event-kaart             /* block */
.event-kaart__titel      /* element */
.event-kaart__badge--niveau  /* modifier */
```

**Regels:**
- Geen directe element-selectors in blokstijlen (`h2 { }` in een blok is verboden).
- Geen `!important`.
- Geen inline styles in templates (uitzondering: `width: {{ value.percentage }}%` voor de voortgangsbalk).
- Klasse-namen zijn altijd in het **Nederlands**, net als `verbose_name` in Python.

---

## Beschikbare StreamField blokken

### Algemene blokken

| Blok-key              | Python klasse              | Wanneer gebruiken                                         |
|-----------------------|-----------------------------|-------------------------------------------------------------|
| `hero`                | `HeroBlock`                  | Bovenaan een pagina; titel, badge, subtitel, 2 CTA's, afbeelding |
| `tekst`               | `RichTextSectionBlock`       | Lopende tekst, h2/h3, lijsten, blockquote                   |
| `afbeelding`          | `ImageBlock`                 | Losse afbeelding met optioneel bijschrift                   |
| `twee_kolommen`       | `TwoColumnBlock`             | Twee rijke tekst-kolommen naast elkaar                      |
| `citaat`              | `QuoteBlock`                 | Klein citaat of inspiratiequote                             |
| `call_to_action`      | `CallToActionBlock`          | Enkelvoudige CTA in light / dark / accent stijl             |
| `video`               | `VideoEmbedBlock`            | YouTube of Vimeo ingesloten video                           |
| `project_raster`      | `ProjectKaartRasterBlock`    | Overzicht van projecten/cases, 2–3 per rij                  |
| `diensten_raster`     | `DienstenRasterBlock`        | 3 diensten naast elkaar met icoon + bullets                 |
| `statistieken`        | `StatistiekenBlock`          | Marquee-ticker met statistieken (donkere balk)              |
| `testimonial`         | `TestimonialBlock`           | Uitgebreid citaat met foto en functietitel                  |
| `logo_strip`          | `LogoStripBlock`             | Horizontale rij logo's                                      |
| `faq`                 | `FAQBlock`                   | Inklapbare vragen — accordion met inline JS toggle          |
| `genummerde_kenmerken`| `GenummerdeFeaturesBlock`    | 2×2 grid van voordelen met groot decoratief nummer          |
| `contact_cta`         | `ContactCTABlock`            | Persoonlijk contactblok met foto, e-mail en telefoon        |

### Bolt Run Club-specifieke blokken

| Blok-key              | Python klasse              | Wanneer gebruiken                                         |
|-----------------------|-----------------------------|-------------------------------------------------------------|
| `evenementen_raster`  | `EventenRasterBlock`        | "Upcoming Events" — 3 event-kaarten met datum, tijd, niveau, RSVP |
| `routes_raster`       | `RoutesRasterBlock`         | "Our Routes" — route-kaarten met afbeelding, tag en titel   |
| `doel_tracker`        | `DoelTrackerBlock`          | "Club Goal Tracker" — voortgangsbalk met percentage          |
| `nieuwsbrief_cta`     | `NieuwsbriefCTABlock`        | "Join the Pack" — nieuwsbrief-form met afbeelding            |

---

## Bestanden

| Bestand                       | Rol                                              |
|-------------------------------|--------------------------------------------------|
| `static/css/design-system.css`| CSS custom properties (tokens) — hier beginnen  |
| `static/css/main.css`         | Importeert design-system, alle component-stijlen |
| `static/js/main.js`           | Scroll-gedrag header, mobiel menu, geen deps     |
| `core/blocks.py`              | Alle StreamField blokken + `STANDARD_BLOCKS`     |
| `core/templates/blocks/`      | HTML template per blok                           |
| `templates/base.html`         | Hoofd-HTML, laadt design-system + main.css       |
