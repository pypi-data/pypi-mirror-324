# Generated by Django 4.1.2 on 2022-11-02 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("effect_screening", "0029_alter_historicalsubjectscreening_cd4_value_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="site",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="sites.site",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="site",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="sites.site",
            ),
        ),
    ]
