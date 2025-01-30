# Generated by Django 3.2.11 on 2022-02-24 12:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0010_auto_20220223_2258"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="histopathology",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Histopathoplogy",
                "verbose_name_plural": "Histopathoplogy",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalhistopathology",
            options={
                "get_latest_by": "history_date",
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Histopathoplogy",
            },
        ),
        migrations.AddField(
            model_name="histopathology",
            name="tissue_biopsy_organism_text",
            field=models.TextField(
                blank=True, null=True, verbose_name="If growth positive, organism"
            ),
        ),
        migrations.AddField(
            model_name="historicalhistopathology",
            name="tissue_biopsy_organism_text",
            field=models.TextField(
                blank=True, null=True, verbose_name="If growth positive, organism"
            ),
        ),
        migrations.AlterField(
            model_name="histopathology",
            name="tissue_biopsy_organism",
            field=models.CharField(
                choices=[
                    ("cryptococcus_neoformans", "Cryptococcus neoformans"),
                    ("mycobacterium_tuberculosis", "Mycobacterium Tuberculosis"),
                    ("OTHER", "Other"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=50,
                verbose_name="If growth POSITIVE, organism",
            ),
        ),
        migrations.AlterField(
            model_name="historicalhistopathology",
            name="tissue_biopsy_organism",
            field=models.CharField(
                choices=[
                    ("cryptococcus_neoformans", "Cryptococcus neoformans"),
                    ("mycobacterium_tuberculosis", "Mycobacterium Tuberculosis"),
                    ("OTHER", "Other"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=50,
                verbose_name="If growth POSITIVE, organism",
            ),
        ),
    ]
