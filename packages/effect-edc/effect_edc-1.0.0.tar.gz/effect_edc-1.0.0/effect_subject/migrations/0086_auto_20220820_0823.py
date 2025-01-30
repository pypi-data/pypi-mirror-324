# Generated by Django 3.2 on 2022-08-20 06:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0085_auto_20220729_1844"),
    ]

    operations = [
        migrations.AddField(
            model_name="bloodresultschem",
            name="egfr_drop_abnormal",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                null=True,
                verbose_name="abnormal",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="egfr_drop_grade",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (0, "Not graded"),
                    (1, "Grade 1"),
                    (2, "Grade 2"),
                    (3, "Grade 3"),
                    (4, "Grade 4"),
                    (5, "Grade 5"),
                ],
                null=True,
                verbose_name="Grade",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="egfr_drop_grade_description",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Grade description"
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="egfr_drop_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="egfr_drop_reportable",
            field=models.CharField(
                blank=True,
                choices=[
                    ("N/A", "Not applicable"),
                    ("3", "Yes, grade 3"),
                    ("4", "Yes, grade 4"),
                    ("No", "Not reportable"),
                    ("Already reported", "Already reported"),
                    ("present_at_baseline", "Present at baseline"),
                ],
                max_length=25,
                null=True,
                verbose_name="reportable",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="egfr_drop_units",
            field=models.CharField(
                blank=True,
                choices=[("%", "%")],
                default="%",
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="egfr_drop_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=4,
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
                verbose_name="eGFR Drop",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="egfr_drop_abnormal",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                null=True,
                verbose_name="abnormal",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="egfr_drop_grade",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (0, "Not graded"),
                    (1, "Grade 1"),
                    (2, "Grade 2"),
                    (3, "Grade 3"),
                    (4, "Grade 4"),
                    (5, "Grade 5"),
                ],
                null=True,
                verbose_name="Grade",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="egfr_drop_grade_description",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Grade description"
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="egfr_drop_quantifier",
            field=models.CharField(
                blank=True,
                choices=[("=", "="), (">", ">"), (">=", ">="), ("<", "<"), ("<=", "<=")],
                default="=",
                max_length=10,
                null=True,
                verbose_name="Quantifier",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="egfr_drop_reportable",
            field=models.CharField(
                blank=True,
                choices=[
                    ("N/A", "Not applicable"),
                    ("3", "Yes, grade 3"),
                    ("4", "Yes, grade 4"),
                    ("No", "Not reportable"),
                    ("Already reported", "Already reported"),
                    ("present_at_baseline", "Present at baseline"),
                ],
                max_length=25,
                null=True,
                verbose_name="reportable",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="egfr_drop_units",
            field=models.CharField(
                blank=True,
                choices=[("%", "%")],
                default="%",
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="egfr_drop_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=4,
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
                verbose_name="eGFR Drop",
            ),
        ),
    ]
