# Generated by Django 5.0.6 on 2024-05-15 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0027_delete_listadesejoscafe'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Franquia',
        ),
        migrations.RemoveField(
            model_name='cafe',
            name='vezes_visitado',
        ),
    ]
