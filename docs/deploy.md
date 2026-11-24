# Deploying to WordPress.com (Personal plan)

There is no one-click sync on the Personal plan, so the local copy is applied by pasting its output (`dist/`) into the editor. Everything in `dist/` already points to the live domain. Allow about an hour; do it in one sitting, in this order. Every step can be undone on its own.

## 0. Back up (5 min)
- Tools → Export → export everything (keeps pages, patterns, templates). Also copy the current Additional CSS into a text file. Both are your rollback.

## 1. Global Styles + CSS (20 min)
Appearance → Editor → Styles. Follow `docs/global-styles-checklist.md` (palette incl. the new 9th colour "Accent 7", typography, buttons, Style 1–5, Annotation), then ⋮ → Additional CSS → replace with `dist/additional.css`.
Add the palette colour **before** pasting the CSS (it uses it).

## 2. Template parts and templates (10 min)
Editor → Patterns → Template parts / Templates → open each → ⋮ → Code editor → paste the matching `dist/content/<id>-part-*.html` / `<id>-tpl-*.html`. Files are named after the item (header, footer, page, single, archive, 404, search, index, home).

## 3. Patterns (5 min)
Editor → Patterns → ⋮ → Import patterns from JSON → pick the files in `dist/patterns/` (all of them). Re-importing creates copies; delete old duplicates by hand.

## 4. Pages (15 min)
Pages → open page → ⋮ → Code editor → select all → paste `dist/content/<id>-<slug>.html` → Update. Pages: `25-home`, `728-over-ons`, `11-contact`, `404-lid-worden`, `624-english`. Page `1015-commissies` is new: Pages → Add New, title "Commissies", paste, and (before publishing) upload `assets/placeholder-image.png` to the Media Library and re-pick it on the placeholder images, or replace them with real photos. Add it to the menu under Appearance → Editor → Navigation.

## 5. Check (10 min)
Open the five key pages + Nieuws on desktop and phone. Compare with `baseline/local/` screenshots. If something is off, revert that one step from the backup.

Rebuild after edits: `python3 tools/build-patterns.py && python3 tools/build-dist.py`.
Visual regression against local: `node tools/snapshot.mjs <base-url> out.json` then `--diff baseline/snap-base.json out.json`.

## Notes from the live migration (2026-10-07)
- WordPress.com ignores block-style-variation overrides (Style 1-5, Annotation) when saved to Global Styles, even though the editor shows them. `tools/build-dist.py` therefore appends the same rules as plain CSS to `dist/additional.css`. Editing Style 1-5 in the Styles panel will not change the look; edit the CSS block "Section Styles 1-5" instead.
- The live "Over ons" page has ID 1 (local copy: 728). Patterns and other pages kept their IDs.
- The Commissies page is live as a private page (ID 877, only visible when logged in) with placeholders; use Edit page in the admin bar to work on it, then set it to Published when ready.

## SEO (set 2026-10-07, all invisible on the page)
- Meta descriptions come from each page's **Excerpt** (page sidebar → Excerpt). Keep them under ~155 characters. Home: tagline of the site is used for social previews.
- Home carries JSON-LD (WebSite + SportsOrganization with address, logo, Instagram/Linktree).
- Footer year is filled by a one-line script; the visible fallback is the year written in the footer part.
- Pages "vereniging" and "Nieuws" were moved to the trash; the site has no posts page.

## Nov 2026: Bestuur, Commissies and navigation

- `/commissies` (page 877) and `/bestuur` (page 1010) are public. Saved copies: `src/content/commissies-page.html`, `src/content/bestuur-page.html` (the older `1015-commissies.html` is superseded).
- The header menu is the Navigation post 4 (`src/content/navigation-4.html`): Home, **Over ons** (dropdown: Bestuur, Commissies), Contact, Merch (highlighted button), then EN and Word lid.
- Merch drop closed on 22 Nov 2026: the highlighted nav link was removed (CSS class `fortius-nav-merch` stays in the stylesheet for the next drop), and `/merch` now shows a closed state (no order form). The open-round versions live on as patterns *Merch – countdown naar volgende ronde* and *Merch – bestelformulier*.
