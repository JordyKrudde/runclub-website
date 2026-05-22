# Techture Media – Design Systeem

Dit bestand wordt automatisch geladen in elke Claude Code sessie. Gebruik het als referentie bij het bouwen of stylen van componenten.

---

## Kleurenpalet

| CSS Variable          | Hex       | Gebruik                                      |
|-----------------------|-----------|----------------------------------------------|
| `--color-bg`          | `#0f0f0f` | Basis achtergrond van de gehele site         |
| `--color-bg-alt`      | `#1a1a1a` | Kaarten, secties, afwisselende achtergrond   |
| `--color-bg-raised`   | `#222222` | Hover-states, actieve elementen              |
| `--color-text`        | `#f0ece4` | Primaire tekst — koppen, body                |
| `--color-text-muted`  | `#888888` | Secundaire tekst — meta, beschrijvingen      |
| `--color-text-faint`  | `#555555` | Placeholders, decoratieve getallen, dividers |
| `--color-accent`      | `#c8f04d` | Lime groen — CTAs, links, highlights, tags   |
| `--color-accent-dark` | `#a8cc38` | Hover-state van accent                       |
| `--color-border`      | `#2a2a2a` | Randen van kaarten en secties                |
| `--color-border-muted`| `#1e1e1e` | Subtielere randen, dividers                  |

**Regels:**
- Gebruik nooit hardcoded hex-waarden in CSS — altijd `var(--color-*)`.
- Primaire actiekleur is altijd `--color-accent` (lime groen op donker).
- Foutmeldingen mogen afwijken: gebruik `#f87171` (rood).

---

## Typografische schaal

| Variable        | Waarde     | Gebruik                                  |
|-----------------|------------|------------------------------------------|
| `--text-xs`     | 0.75rem    | Labels, badges, kleine meta              |
| `--text-sm`     | 0.875rem   | Body tekst, navigatielinks, knoppen      |
| `--text-base`   | 1rem       | Standaard alineatekst                    |
| `--text-lg`     | 1.25rem    | Kaarttitels, intro's                     |
| `--text-xl`     | 1.5rem     | Subtitels, sectie-intro's                |
| `--text-2xl`    | 2rem       | H3 koppen                                |
| `--text-3xl`    | 3rem       | H2 koppen, sectietitels                  |
| `--text-4xl`    | 4.5rem     | Hero subtitels, grote statistieken       |
| `--text-5xl`    | 6rem       | H1 paginatitels                          |

**Gewichten:**
- `--font-weight-normal` (400) — lopende tekst
- `--font-weight-medium` (500) — navigatielinks
- `--font-weight-bold`   (700) — knoppen, labels, kaarttitels
- `--font-weight-black`  (900) — H1/H2 koppen, logo, getallen

**Regels:**
- Koppen altijd `font-weight: var(--font-weight-black)` + `letter-spacing: -0.03em`.
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
| `--space-24` | 6rem    |
| `--space-32` | 8rem    |

Secties gebruiken `padding-block: var(--space-24)` als standaard verticale marge.

---

## Lay-out

| Variable              | Waarde    | Gebruik                          |
|-----------------------|-----------|----------------------------------|
| `--container-max`     | 1280px    | Max-breedte van alle containers  |
| `--container-padding` | 2rem      | Horizontale pagina-marge         |
| `--radius-sm`         | 4px       | Kleine elementen (tags, badges)  |
| `--radius-md`         | 12px      | Formuliervelden, kleine kaarten  |
| `--radius-lg`         | 24px      | Kaarten, blokken                 |
| `--radius-full`       | 9999px    | Knoppen (pill-vorm), foto's      |

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
.project-kaart           /* block */
.project-kaart__titel    /* element */
.project-kaart--groot    /* modifier */
```

**Regels:**
- Geen directe element-selectors in blokstijlen (`h2 { }` in een blok is verboden).
- Geen `!important`.
- Geen inline styles in templates.
- Klasse-namen zijn altijd in het **Nederlands**, net als `verbose_name` in Python.

---

## Beschikbare StreamField blokken

### Bestaande blokken

| Blok-key          | Python klasse          | Wanneer gebruiken                                   |
|-------------------|------------------------|-----------------------------------------------------|
| `hero`            | `HeroBlock`            | Bovenaan een pagina, grote uitgelichte sectie       |
| `tekst`           | `RichTextSectionBlock` | Lopende tekst, h2/h3, lijsten, blockquote           |
| `afbeelding`      | `ImageBlock`           | Losse afbeelding met optioneel bijschrift           |
| `twee_kolommen`   | `TwoColumnBlock`       | Twee rijke tekst-kolommen naast elkaar              |
| `citaat`          | `QuoteBlock`           | Klein klantcitaat of inspiratiequote               |
| `call_to_action`  | `CallToActionBlock`    | Enkelvoudige CTA in light / dark / accent stijl    |
| `video`           | `VideoEmbedBlock`      | YouTube of Vimeo ingesloten video                   |

### Nieuwe blokken

| Blok-key              | Python klasse              | Wanneer gebruiken                                         |
|-----------------------|----------------------------|-----------------------------------------------------------|
| `project_raster`      | `ProjectKaartRasterBlock`  | Portfolio/werk overzicht, 2–3 projecten per rij           |
| `diensten_raster`     | `DienstenRasterBlock`      | 3 diensten naast elkaar met icoon + bullets               |
| `statistieken`        | `StatistiekenBlock`        | Social proof — resultaten in grote getallen              |
| `testimonial`         | `TestimonialBlock`         | Uitgebreid klantcitaat met foto en functietitel          |
| `logo_strip`          | `LogoStripBlock`           | Horizontale rij klantlogo's (grijs/gedempt)              |
| `faq`                 | `FAQBlock`                 | Inklapbare vragen — accordion met inline JS toggle       |
| `genummerde_kenmerken`| `GenummerdeFeaturesBlock`  | 2×2 grid van voordelen met groot decoratief nummer       |
| `contact_cta`         | `ContactCTABlock`          | Persoonlijk contactblok met foto, e-mail en telefoon     |

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
