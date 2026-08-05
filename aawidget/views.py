"""Opslaan van de dashboardindeling — Widget.

Eén endpoint, alleen POST, alleen voor wie mag indelen. De browser stuurt de
volgorde en de breedtes op zodra je klaar bent met slepen.
"""

import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from aawidget.models import Indeling, schoon_breedtes, schoon_volgorde


def mag_indelen(user):
    """Wie de indeling voor iedereen mag bepalen.

    Superuser of staff, of het losse recht — zodat je het kunt weggeven zonder
    iemand meteen de hele admin in te laten.
    """
    return bool(user and user.is_authenticated
                and (user.is_superuser or user.is_staff
                     or user.has_perm("aawidget.indelen")))


@login_required
@require_POST
def opslaan(request):
    """De indeling bewaren. Geldt daarna voor iedereen."""
    if not mag_indelen(request.user):
        return JsonResponse({"ok": False, "fout": "geen rechten"}, status=403)

    try:
        gegevens = json.loads(request.body or b"{}")
    except ValueError:
        return JsonResponse({"ok": False, "fout": "onleesbaar"}, status=400)

    indeling = Indeling.haal()
    indeling.volgorde = schoon_volgorde(gegevens.get("volgorde"))
    indeling.breedtes = schoon_breedtes(gegevens.get("breedtes"))
    indeling.door = request.user
    indeling.save()
    return JsonResponse({"ok": True, "blokken": len(indeling.volgorde)})


@login_required
@require_POST
def herstellen(request):
    """Terug naar de standaardindeling van Alliance Auth, voor iedereen."""
    if not mag_indelen(request.user):
        return JsonResponse({"ok": False, "fout": "geen rechten"}, status=403)

    indeling = Indeling.haal()
    indeling.volgorde = []
    indeling.breedtes = {}
    indeling.door = request.user
    indeling.save()
    return JsonResponse({"ok": True})
