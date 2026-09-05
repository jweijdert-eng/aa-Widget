"""Stukken bínnen een blok kunnen verbergen."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aawidget', '0002_indeling_verborgen'),
    ]

    operations = [
        migrations.AddField(
            model_name='indeling',
            name='stukken',
            field=models.JSONField(
                blank=True, default=list,
                help_text='Delen bínnen een blok die weg mogen, als paren van '
                          'bloksleutel en css-pad. Zo kun je bijvoorbeeld alleen '
                          'de geschiedenis onder de ESI-status weghalen zonder '
                          'het hele blok te verliezen.',
                verbose_name='Verborgen stukken'),
        ),
    ]
