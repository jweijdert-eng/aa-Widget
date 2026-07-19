# Widget

Herschik de **Alliance Auth-dashboardblokken** door ze te verslepen.

AA rendert de dashboardwidgets (Karakter, Lidmaatschap, Onboarding, CharLink,
Member Audit …) in een vaste, server-bepaalde volgorde. Deze plugin voegt via
de officiële `dashboard_hook` een klein, onzichtbaar blok toe dat een stukje JS
meelevert: dat maakt de andere blokken **sleepbaar** (greep rechtsboven op elk
blok) en onthoudt **jouw** volgorde in de browser (localStorage). Een knop
*Herstel standaard* zet alles terug.

- Geen template-override, geen conflict met andere branding-plugins.
- Geen database, geen migraties, geen tokens of permissies.
- De volgorde is persoonlijk en per browser.

## Installatie

```bash
pip install -e .            # editable, voor lokale ontwikkeling
```

Voeg `aawidget` toe aan `INSTALLED_APPS` en herstart AA. Klaar — open het
dashboard en sleep.

## Hoe het werkt

`aawidget/auth_hooks.py` registreert een `DashboardItemHook` met een hoge
`order`, zodat het als laatste rendert. Het bijbehorende `reorder.html` verbergt
zichzelf en verrijkt de zusterblokken met drag-and-drop. Elk blok krijgt een
sleutel afgeleid van z'n kop, zodat de opgeslagen volgorde herkenbaar blijft.
