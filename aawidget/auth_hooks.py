"""Hook into Alliance Auth — Widget (dashboard herschikken).

We voegen géén zichtbaar blok toe, maar registreren een dashboard-hook die een
klein stukje JS meelevert. Dat script zet de dashboardblokken in de volgorde en
de breedte die een admin heeft vastgelegd, en geeft admins de gereedschappen om
dat te veranderen. Zo hoeven we de dashboard-template niet te overschrijven —
puur via de officiële hook.
"""

from django.template.loader import render_to_string

from allianceauth import hooks
from allianceauth.hooks import DashboardItemHook
from allianceauth.services.hooks import UrlHook

from aawidget import urls
from aawidget.views import mag_indelen


class ReorderHook(DashboardItemHook):
    def __init__(self):
        # Hoge order → wordt als laatste gerenderd; het blok verbergt zichzelf.
        super().__init__(self.render_enhancer, order=9999)

    def render_enhancer(self, request):
        """Iedereen krijgt de indeling te zien; alleen admins de knoppen.

        Voorheen kregen niet-admins hier niets terug, want er viel voor hen ook
        niets te zien: de indeling stond in hun eigen browser. Nu ligt er één
        indeling voor de hele site, en die moeten ze juist wél toegepast krijgen.
        """
        from aawidget.models import Indeling

        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return ""
        try:
            indeling = Indeling.haal()
            volgorde, breedtes = indeling.volgorde, indeling.breedtes
        except Exception:  # noqa: BLE001 — tabel bestaat nog niet (vóór migrate)
            volgorde, breedtes = [], {}
        return render_to_string(
            "aawidget/reorder.html",
            {"aaw_volgorde": volgorde, "aaw_breedtes": breedtes,
             "aaw_mag_indelen": mag_indelen(user)},
            request=request)


@hooks.register("dashboard_hook")
def register_reorder_hook():
    return ReorderHook()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "aawidget", r"^aawidget/")
