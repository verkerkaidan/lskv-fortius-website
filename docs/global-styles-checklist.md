# Global Styles on WordPress.com – click-by-click

Personal plan has no Global Styles import, so enter these once. Open **Appearance → Editor → Styles**. Do the steps in order; the full machine-readable source is `dist/global-styles.json`.

## 1. Palette (Styles → Colors → Palette → Theme)
Rename/recolour the 8 existing swatches (keep their order), then add a 9th custom swatch:

| Slot | Name | Hex |
|---|---|---|
| Base | Zwart | #121212 |
| Contrast | Licht (off-white) | #F0F0F0 |
| Accent 1 | Grijs | #8a8a86 |
| Accent 2 | Donkerrood | #8f1520 |
| Accent 3 | Rood | #c81e2c |
| Accent 4 | Wit | #ffffff |
| Accent 5 | Donkergrijs | #3a3a38 |
| Accent 6 | Lichtgrijs | #c9c9ce |
| Accent 7 (new) | Rood (licht, voor tekst op zwart) | #e8414d |

Site-wide: Colors → Background = Zwart, Text = Wit (the header/footer and dark pages rely on this).

## 2. Typography (Styles → Typography)
- Text: Archivo, 16px, line height 1.4.
- Headings: Titan One (Typography → Headings; same for H1–H6).

## 3. Buttons (Styles → Blocks → Button)
- Colors: background Rood, text Wit. Hover: background Donkerrood, text Wit.
- Border: 2px solid, colour Rood, radius 0. Hover border: Donkerrood.
- Padding: 0.8rem top/bottom, 2rem left/right.
- Typography: Archivo, 14px, bold (700), uppercase, letter spacing 0.04em.
- **Variations → Outline**: background transparent, text "currentColor" (type `currentColor` in the custom field if the UI allows, otherwise leave unset), border 2px solid same colour as text, same padding. Hover: background Wit, text Zwart, border Wit.

## 4. Section styles (Styles → Blocks → Group → Variations)
Repeat the same values for **Group**, **Columns** and **Column**. For each variation set Background, Text, then under Elements → Headings and → Buttons the colours below.

| Variation | Background | Text | Headings | Button (hover) |
|---|---|---|---|---|
| Style 1 | Zwart | Wit | Wit | Rood / Wit (Donkerrood) |
| Style 2 | Rood | Wit | Wit | Wit / Rood (Zwart, text Wit) |
| Style 3 | Wit | Donkergrijs | Zwart | Rood / Wit (Donkerrood) |
| Style 4 | Donkergrijs | Wit | Wit | Rood / Wit (Donkerrood) |
| Style 5 | Licht (#F0F0F0) | Donkergrijs | Zwart | Rood / Wit (Donkerrood) |

## 5. Annotation (Styles → Blocks → Paragraph → Variations → Annotation)
Text Rood; Archivo 14px bold, uppercase, letter spacing 0.15em, line height 1.4; padding 0.

## 6. Additional CSS
Styles → ⋮ → Additional CSS: paste `dist/additional.css` (replaces the old one).

Then continue with `docs/deploy.md` steps 2–5.
