# Generated by Django 3.1.2 on 2020-11-30 21:14

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('naturapeute', '0014_auto_20201130_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='latlng',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.DecimalField(decimal_places=15, max_digits=17), size=2),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='practices',
            field=models.ManyToManyField(blank=True, related_name='therapists', to='naturapeute.Practice', verbose_name='Autres pratiques'),
        ),
    ]