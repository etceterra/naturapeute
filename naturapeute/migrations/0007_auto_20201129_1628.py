# Generated by Django 3.1.2 on 2020-11-29 16:28

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('naturapeute', '0006_officepicture_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapist',
            name='agreements',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='firstname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='is_certified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='languages',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=2), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='lastname',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='therapist',
            name='payment_types',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='photo',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='price',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='socials',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.TextField(), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='therapist',
            name='timetable',
            field=models.TextField(blank=True, null=True),
        ),
    ]
