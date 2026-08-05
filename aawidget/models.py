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
