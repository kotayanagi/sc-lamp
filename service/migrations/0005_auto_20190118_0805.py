# Generated by Django 2.1.5 on 2019-01-18 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20190118_0804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='keyword_link',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='keyword_link'),
        ),
    ]
