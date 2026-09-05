"""Blokken kunnen verbergen."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aawidget', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='indeling',
            name='verborgen',
            field=models.JSONField(
                blank=True, default=list,
                help_text='De sleutels van blokken die niemand te zien krijgt. '
                          'Wie mag indelen ziet ze nog wel, doorzichtig, om ze '
                          'terug te kunnen zetten.',
                verbose_name='Verborgen'),
        ),
    ]
