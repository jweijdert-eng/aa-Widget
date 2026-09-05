"""De dashboardindeling — Widget.

**Waarom in de database en niet meer in de browser.** Tot 0.1.4 stonden volgorde
en breedtes in localStorage. Dat werkt, maar het geldt alleen voor die ene
browser: je eigen telefoon zag het al niet, en de rest van de corp al helemaal
niet. Eén indeling voor de hele site hoort dus aan de serverkant te staan.

Eén rij, net als bij een instellingenscherm: zo kan er nooit een tweede indeling
ontstaan waarvan je je afvraagt welke nou geldt.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Grenzen op wat de browser mag opsturen. Alleen admins komen erbij, maar
# ongecontroleerde invoer die je later weer op de pagina zet blijft ongezond.
MAX_BLOKKEN = 100
MAX_SLEUTEL = 80
MAX_STUKKEN = 200
MAX_PAD = 300
BREEDTES = (3, 4, 6, 8, 12)     # kwart, derde, half, tweederde, vol


class Indeling(models.Model):
    """De indeling die iedereen op het dashboard te zien krijgt."""

    volgorde = models.JSONField(
        default=list, blank=True, verbose_name=_("Volgorde"),
        help_text=_("De sleutels van de blokken, in de volgorde waarin ze "
                    "staan. Blokken die hier niet in staan komen achteraan."))
    breedtes = models.JSONField(
        default=dict, blank=True, verbose_name=_("Breedtes"),
        help_text=_("Per blok het aantal kolommen van de twaalf."))
    verborgen = models.JSONField(
        default=list, blank=True, verbose_name=_("Verborgen"),
        help_text=_("De sleutels van blokken die niemand te zien krijgt. Wie "
                    "mag indelen ziet ze nog wel, doorzichtig, om ze terug te "
                    "kunnen zetten."))
    stukken = models.JSONField(
        default=list, blank=True, verbose_name=_("Verborgen stukken"),
        help_text=_("Delen bínnen een blok die weg mogen, als paren van "
                    "bloksleutel en css-pad. Zo kun je bijvoorbeeld alleen de "
                    "geschiedenis onder de ESI-status weghalen zonder het hele "
                    "blok te verliezen."))
    door = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        blank=True, verbose_name=_("Laatst gewijzigd door"))
    bijgewerkt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("dashboardindeling")
        verbose_name_plural = _("dashboardindeling")
        permissions = (("indelen", _("Mag de dashboardindeling wijzigen")),)

    def __str__(self):
        return str(_("Indeling van het dashboard"))

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def haal(cls):
        return cls.objects.get_or_create(pk=1)[0]


def schoon_volgorde(waarde):
    """Alleen bruikbare sleutels overhouden, en niet meer dan een handvol."""
    if not isinstance(waarde, list):
        return []
    uit = []
    for sleutel in waarde[:MAX_BLOKKEN]:
        if isinstance(sleutel, str) and sleutel.strip():
            uit.append(sleutel.strip()[:MAX_SLEUTEL])
    return uit


def schoon_verborgen(waarde):
    """Welke blokken verborgen zijn.

    Dezelfde vorm als de volgorde - een lijst sleutels - dus hetzelfde
    schoonmaakwerk. Een aparte functie omdat de betekenis verschilt en de
    volgende die hier komt kijken dat meteen moet zien.
    """
    return schoon_volgorde(waarde)


def schoon_stukken(waarde):
    """De verborgen stukken: telkens een bloksleutel plus een css-pad.

    Het pad gaat straks door `querySelectorAll` van de browser. Een fout pad
    levert daar een uitzondering op die we opvangen, dus het ergste dat een
    onzinwaarde doet is niets - maar lengte begrenzen we hier wel, want dit
    komt van buiten en gaat de pagina weer op.
    """
    if not isinstance(waarde, list):
        return []
    uit = []
    for stuk in waarde[:MAX_STUKKEN]:
        if not isinstance(stuk, dict):
            continue
        blok = stuk.get("blok")
        pad = stuk.get("pad")
        if not isinstance(blok, str) or not isinstance(pad, str):
            continue
        blok, pad = blok.strip(), pad.strip()
        if not blok or not pad:
            continue
        uit.append({"blok": blok[:MAX_SLEUTEL], "pad": pad[:MAX_PAD]})
    return uit


def schoon_breedtes(waarde):
    """Alleen breedtes die de knoppen ook kunnen maken."""
    if not isinstance(waarde, dict):
        return {}
    uit = {}
    for sleutel, breedte in list(waarde.items())[:MAX_BLOKKEN]:
        if not isinstance(sleutel, str) or not sleutel.strip():
            continue
        try:
            breedte = int(breedte)
        except (TypeError, ValueError):
            continue
        if breedte in BREEDTES:
            uit[sleutel.strip()[:MAX_SLEUTEL]] = breedte
    return uit
