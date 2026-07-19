"""Hook into Alliance Auth — Widget (dashboard herschikken).

We voegen géén zichtbaar blok toe, maar registreren een dashboard-hook die
een klein stukje JS meelevert. Dat script maakt de andere dashboardblokken
sleepbaar en onthoudt de volgorde per gebruiker (in de browser). Zo hoeven we
de dashboard-template niet te overschrijven — puur via de officiële hook.
"""

from django.template.loader import render_to_string

from allianceauth import hooks
from allianceauth.hooks import DashboardItemHook


class ReorderHook(DashboardItemHook):
    def __init__(self):
        # Hoge order → wordt als laatste gerenderd; het blok verbergt zichzelf.
        super().__init__(self.render_enhancer, order=9999)

    def render_enhancer(self, request):
        # Alleen admins (superuser/staff) mogen het dashboard herschikken.
        user = getattr(request, "user", None)
        if not user or not (user.is_superuser or user.is_staff):
            return ""
        return render_to_string("aawidget/reorder.html", {}, request=request)


@hooks.register("dashboard_hook")
def register_reorder_hook():
    return ReorderHook()
