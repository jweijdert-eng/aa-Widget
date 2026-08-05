# Widget

Herschik de **Alliance Auth-dashboardblokken** door ze te verslepen — en wat een
admin neerzet, ziet de hele site.

AA rendert de dashboardwidgets (Karakter, Lidmaatschap, Onboarding, CharLink,
Member Audit …) in een vaste, server-bepaalde volgorde. Deze plugin voegt via de
officiële `dashboard_hook` een klein, onzichtbaar blok toe dat een stukje JS
meelevert: dat zet de blokken in de vastgelegde volgorde en breedte, en geeft
admins een greep rechtsboven op elk blok om dat te veranderen.

- **Eén indeling voor iedereen.** Een admin sleept, iedereen ziet het resultaat.
- Geen template-override, geen conflict met andere branding-plugins.
- Geen tokens; wel één tabel met één rij.
- Gewone leden zien geen balk en geen grepen — voor hen wordt de indeling
  alleen toegepast.

## Wie mag indelen

Superuser, staff, of wie het losse recht **`aawidget | dashboardindeling | Mag
de dashboardindeling wijzigen`** heeft. Met dat laatste kun je het weggeven
zonder iemand meteen de hele admin in te laten.

## Van persoonlijk naar gedeeld

Tot 0.1.4 stonden volgorde en breedte in **localStorage**. Dat werkte, maar het
gold alleen in die ene browser: je eigen telefoon zag het al niet, en de rest van
de corp al helemaal niet. Vanaf 0.2.0 staat de indeling in de database.

Wat er van localStorage overblijft is de schakelaar *Dashboard bewerken*. Dat is
geen indeling maar een persoonlijke voorkeur, en die hoeft niemand anders te
zien.

**Bij het bijwerken begin je met een schone lei:** je oude persoonlijke indeling
verhuist niet mee. Sleep hem één keer opnieuw en dan staat hij voor iedereen goed.

## Installatie

```bash
pip install -e .            # editable, voor lokale ontwikkeling
```

Voeg `aawidget` toe aan `INSTALLED_APPS`, draai `python manage.py migrate` en
herstart AA. Klaar — open het dashboard en sleep.

## Hoe het werkt

`aawidget/auth_hooks.py` registreert een `DashboardItemHook` met een hoge
`order`, zodat het als laatste rendert. Het bijbehorende `reorder.html` verbergt
zichzelf en verrijkt de zusterblokken met drag-and-drop. Elk blok krijgt een
sleutel afgeleid van z'n kop, zodat de vastgelegde volgorde herkenbaar blijft.

De indeling gaat via `POST /aawidget/opslaan/` naar de server, gedebounced op
600 ms — anders zou dat tijdens het slepen bij elke muisbeweging afgaan. Wat
binnenkomt wordt opgeschoond voordat het wordt bewaard: alleen sleutels die
tekst zijn, hoogstens 100 blokken van 80 tekens, en alleen breedtes die de
knoppen ook kunnen maken (3, 4, 6, 8 of 12 van de twaalf). Alleen admins komen
bij dat endpoint, maar invoer die je later weer op de pagina zet controleer je
hoe dan ook.

Een blok dat nog niet in de vastgelegde volgorde staat — een nieuw geïnstalleerde
plugin bijvoorbeeld — komt gewoon achteraan te staan.
