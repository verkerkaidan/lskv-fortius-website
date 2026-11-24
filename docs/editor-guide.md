# Editor guide – building pages on lskvfortius.nl

Everything below is chosen from the WordPress editor. You never need to write CSS or copy colours.

## 1. Start from a pattern
Add block (+) → **Patterns** → **My patterns** (or search "Sectie", "hero", "kaarten"). Patterns are inserted as plain blocks you can edit freely.

| Pattern | Use for |
|---|---|
| Pagina-hero (donkere banner) | Top of every inner page |
| Home-hero met foto | Home page opening |
| Sectie – Stijl 1…5 | Generic section: label, heading, text, button. Pick the colour by pattern |
| Drie kaarten | Three highlights in a row |
| Quote-strook (marquee) | Scrolling member quotes |
| Samenwerkingen met logo's | Partner logo row |
| Contactgegevens + kaart | Contact page body |
| Contact – donkere sectie | Closing contact band |
| Lid worden – uitleg / licht | Membership explanation sections |
| Bestuur & Commissies – foto links | Same as the Bestuur section but photo left, text right |
| Tekst + foto rechts / links | Generic two-column section with placeholder label, slogan, text and image. Set the colour with Styles 1–5; photo-left keeps text on top on mobile |
| Prijzen, FAQ, Kernwaarden, Bestuur & Commissies, TrainingsTijden, Aanmeldformulier, Foto & Tekst Wit | Existing content patterns |

## 2. Change the look of a section (block Styles)
Select a **Group** → sidebar → **Styles**:

| Style | Look |
|---|---|
| Style 1 – Donker | Black background, white text |
| Style 2 – Rood | Red background, white text, inverted buttons |
| Style 3 – Wit | White background |
| Style 4 – Donkergrijs | Dark grey background |
| Style 5 – Licht | Off-white (#F0F0F0) background |

Headings, text and button colours follow the section automatically. Sections get the standard side padding by themselves.

- **Annotation** (Paragraph → Styles): the small red uppercase label above a heading.
- **Buttons**: *Fill* (red) or *Outline* (border in text colour). Nothing else is needed.
- **Headings**: just use H1/H2/H3; fonts and sizes are global.

## 3. Colours
Only use the palette (Zwart, Licht, Grijs, Donkerrood, Rood, Wit, Donkergrijs, Lichtgrijs). Avoid the custom colour picker; otherwise a later palette change will miss that block. Change palette values once in **Appearance → Editor → Styles → Colors**.

## 4. Things that are deliberately fixed
- Header and footer are edited under **Appearance → Editor → Patterns → Template parts**.
- Class names starting with `fortius-` (Advanced → Additional CSS class) drive layout of specific components (hero, quote strip, steps, price table, partners). Keep them when you copy a section; delete the block, not the class.

## 5. Troubleshooting a new page
- **Black gap between sections**: an empty paragraph (or spacer) sits between two sections. Select it in List View and delete it. Sections should touch each other.
- **Alternating look**: set the sections to Style 3 (white) and Style 5 (light) in turn; the hero is Style 1.
- **Page title**: pages that start with the *Pagina-hero* pattern hide the automatic title. Pages that do not start with a hero show the title above the content, which is meant for plain text pages (e.g. privacy).

## 6. Accessibility
- Give every meaningful photo **alt text** (select the image → sidebar → *Alternative text*). Decorative images can stay empty.
- Small red text on a black background uses the lighter red (*Rood (licht)*) automatically in Style 1, Style 4, the page hero and the dark card band. Do not use the normal red for small text on black.

## 7. Merch page
- **Countdown**: pattern *Merch – countdown naar volgende ronde*. To change the date, click the block, open the Custom HTML editor and change `data-date="2026-11-22T23:59:59+01:00"` (year-month-day, then time). The countdown now runs to the closing time of the current order round. The visible date and the countdown follow automatically; when the date has passed it shows "De merch-ronde is nu open!".
- **Products**: duplicate a product card inside the grid, or insert *Merch – product (kleuren + maten)*, *(alleen kleuren)* or *(geen varianten)* (bags). Edit name, price and sizes as normal text. The grid wraps by itself (3 columns on desktop).
- **Colour variants**: each colour is one image inside the card's image group. Click an image, replace it (Replace → Media Library) and **type the colour name in the caption under the image** (for example "Zwart"). On the live page the caption is hidden and becomes the text of a colour button; clicking a button switches the picture. Known colour names (zwart, wit, rood, blauw, grijs, groen, geel, oranje, roze, paars, bruin, beige, navy) also get a colour dot. Add a colour by duplicating an image block, remove one by deleting it. A card with one image shows no buttons. (If a caption is empty, the image's Alternative text is used.)
- **Colour picker script**: the pattern *Merch – kleurkiezer (script, 1x per pagina)* sits under the product grid and must stay on the page once.
- **Deadline, payment and FAQ**: the order section has a Deadline and a Betalen paragraph, and the page ends with a FAQ (click a question to edit it like any block). Replace every `[Placeholder: …]` (deadline, MerchCo email address, delivery time) before the page goes public.
- **Order form**: pattern *Merch – bestelformulier* embeds the merch Google Form (`…/viewform?embedded=true`). The form stays the same each round; it only opens and closes on the Google side. Above it sits a text link that opens the same form in a new tab (edit it like any paragraph link). The embed is 1500px tall (set in the CSS rule `.fortius-merch-form iframe`).
