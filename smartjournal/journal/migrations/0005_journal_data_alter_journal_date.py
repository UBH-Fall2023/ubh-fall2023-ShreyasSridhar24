# Generated by Django 4.2.7 on 2023-11-05 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0004_alter_journal_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='data',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='date',
            field=models.DateField(),
        ),
    ]