# Generated by Django 3.1.2 on 2020-11-29 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naturapeute', '0008_auto_20201129_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapist',
            name='gender',
            field=models.CharField(choices=[('man', 'Homme'), ('woman', 'Femme')], default='woman', max_length=6),
        ),
    ]
