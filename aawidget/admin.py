"""Beheerscherm — Widget.

Het indelen zelf doe je op het dashboard door te slepen; hier zie je alleen wat
er vastligt, en kun je het zo nodig leegmaken.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from aawidget.models import Indeling


@admin.register(Indeling)
class IndelingAdmin(admin.ModelAdmin):
    """Eén rij, die je alleen kunt bekijken en wissen — niet toevoegen."""

    list_display = ("__str__", "aantal_blokken", "door", "bijgewerkt")
    readonly_fields = ("door", "bijgewerkt")
    actions = ("leegmaken",)

    def has_add_permission(self, request):
        return (super().has_add_permission(request)
                and not Indeling.objects.exists())

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description=_("Blokken vastgelegd"))
    def aantal_blokken(self, obj):
        return len(obj.volgorde or [])

    @admin.action(description=_("Terug naar de standaardindeling"))
    def leegmaken(self, request, queryset):
        queryset.update(volgorde=[], breedtes={}, door=request.user)
