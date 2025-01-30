# Generated by Django 5.1.1 on 2024-09-12 14:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_subject", "0116_alter_bloodculture_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bloodresultschem",
            name="sodium_abnormal",
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
            name="sodium_grade",
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
            name="sodium_grade_description",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Grade description"
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="sodium_quantifier",
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
            name="sodium_reportable",
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
            name="sodium_units",
            field=models.CharField(
                blank=True,
                choices=[("mmol/L", "mmol/L (millimoles/L)")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AddField(
            model_name="bloodresultschem",
            name="sodium_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=0,
                max_digits=8,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
                verbose_name="Sodium (Na)",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="sodium_abnormal",
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
            name="sodium_grade",
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
            name="sodium_grade_description",
            field=models.CharField(
                blank=True, max_length=250, null=True, verbose_name="Grade description"
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="sodium_quantifier",
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
            name="sodium_reportable",
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
            name="sodium_units",
            field=models.CharField(
                blank=True,
                choices=[("mmol/L", "mmol/L (millimoles/L)")],
                max_length=15,
                null=True,
                verbose_name="units",
            ),
        ),
        migrations.AddField(
            model_name="historicalbloodresultschem",
            name="sodium_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=0,
                max_digits=8,
                null=True,
                validators=[django.core.validators.MinValueValidator(0.0)],
                verbose_name="Sodium (Na)",
            ),
        ),
    ]
