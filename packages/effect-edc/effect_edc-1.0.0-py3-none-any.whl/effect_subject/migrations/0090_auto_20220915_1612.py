# Generated by Django 3.2 on 2022-09-15 14:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0089_auto_20220910_2045"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adherence",
            name="diary_returned",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Was participant adherence diary received and stored in participant records?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherence",
            name="diary_returned",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Was participant adherence diary received and stored in participant records?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagefour",
            name="diary_returned",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Was participant adherence diary received and stored in participant records?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestageone",
            name="diary_returned",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Was participant adherence diary received and stored in participant records?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagethree",
            name="diary_returned",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Was participant adherence diary received and stored in participant records?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaladherencestagetwo",
            name="diary_returned",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Was participant adherence diary received and stored in participant records?",
            ),
        ),
    ]
