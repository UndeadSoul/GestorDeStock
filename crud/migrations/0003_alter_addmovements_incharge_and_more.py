# Generated by Django 4.2.16 on 2024-12-11 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registerlogin', '0001_initial'),
        ('crud', '0002_remove_addmovements_incharge_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addmovements',
            name='incharge',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='registerlogin.profile', verbose_name='profile'),
        ),
        migrations.AlterField(
            model_name='removemovements',
            name='incharge',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='registerlogin.profile', verbose_name='profile'),
        ),
    ]
