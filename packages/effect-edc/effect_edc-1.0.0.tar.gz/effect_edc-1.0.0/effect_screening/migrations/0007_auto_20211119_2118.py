# Generated by Django 3.2.9 on 2021-11-19 18:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_screening", "0006_auto_20211119_2106"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="csf_results_date",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name="Date `pending results` expected (estimate)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="lp_done",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("not_answered", "Not answered")],
                default="not_answered",
                help_text="If YES, provide date below",
                max_length=15,
                null=True,
                verbose_name="Was LP done?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="csf_results_date",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name="Date `pending results` expected (estimate)",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="lp_done",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("not_answered", "Not answered")],
                default="not_answered",
                help_text="If YES, provide date below",
                max_length=15,
                null=True,
                verbose_name="Was LP done?",
            ),
        ),
    ]
