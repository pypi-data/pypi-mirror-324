# Generated by Django 3.2.8 on 2022-03-24 16:25

import edc_model.models.fields.other_charfield
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0028_auto_20220322_2146"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="adherencestagefour",
            options={
                "verbose_name": "Adherence: Day 14+",
                "verbose_name_plural": "Adherence: Day 14+",
            },
        ),
        migrations.AlterModelOptions(
            name="adherencestagetwo",
            options={
                "verbose_name": "Adherence: On study",
                "verbose_name_plural": "Adherence: On study",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaladherencestagefour",
            options={
                "get_latest_by": "history_date",
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Adherence: Day 14+",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaladherencestagetwo",
            options={
                "get_latest_by": "history_date",
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Adherence: On study",
            },
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="diary_match_pill_count_reason_no",
            new_name="diary_match_medication_reason_no",
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="pill_count_conducted_reason_no",
            new_name="medication_reconciliation_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="diary_match_pill_count_reason_no",
            new_name="diary_match_medication_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="pill_count_conducted_reason_no",
            new_name="medication_reconciliation_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="diary_match_pill_count_reason_no",
            new_name="diary_match_medication_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="pill_count_conducted_reason_no",
            new_name="medication_reconciliation_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="diary_match_pill_count_reason_no",
            new_name="diary_match_medication_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="pill_count_conducted_reason_no",
            new_name="medication_reconciliation_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="diary_match_pill_count_reason_no",
            new_name="diary_match_medication_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="pill_count_conducted_reason_no",
            new_name="medication_reconciliation_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="diary_match_pill_count_reason_no",
            new_name="diary_match_medication_reason_no",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="pill_count_conducted_reason_no",
            new_name="medication_reconciliation_reason_no",
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="diary_match_pill_count",
            new_name="diary_match_medication",
        ),
        migrations.RenameField(
            model_name="adherence",
            old_name="pill_count_conducted",
            new_name="medication_reconciliation",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="diary_match_pill_count",
            new_name="diary_match_medication",
        ),
        migrations.RenameField(
            model_name="historicaladherence",
            old_name="pill_count_conducted",
            new_name="medication_reconciliation",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="diary_match_pill_count",
            new_name="diary_match_medication",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagefour",
            old_name="pill_count_conducted",
            new_name="medication_reconciliation",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="diary_match_pill_count",
            new_name="diary_match_medication",
        ),
        migrations.RenameField(
            model_name="historicaladherencestageone",
            old_name="pill_count_conducted",
            new_name="medication_reconciliation",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="diary_match_pill_count",
            new_name="diary_match_medication",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagethree",
            old_name="pill_count_conducted",
            new_name="medication_reconciliation",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="diary_match_pill_count",
            new_name="diary_match_medication",
        ),
        migrations.RenameField(
            model_name="historicaladherencestagetwo",
            old_name="pill_count_conducted",
            new_name="medication_reconciliation",
        ),
        migrations.AddField(
            model_name="adherence",
            name="linked_local_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Have you linked up with your local clinic?",
            ),
        ),
        migrations.AddField(
            model_name="adherence",
            name="linked_local_clinic_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="adherence",
            name="receiving_arv",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Are you receiving ARVs?",
            ),
        ),
        migrations.AddField(
            model_name="adherence",
            name="receiving_arv_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="adherence",
            name="receiving_fluconazole",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Are you receiving Fluconazole?",
            ),
        ),
        migrations.AddField(
            model_name="adherence",
            name="receiving_fluconazole_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherence",
            name="linked_local_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Have you linked up with your local clinic?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherence",
            name="linked_local_clinic_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherence",
            name="receiving_arv",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Are you receiving ARVs?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherence",
            name="receiving_arv_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherence",
            name="receiving_fluconazole",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Are you receiving Fluconazole?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherence",
            name="receiving_fluconazole_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagefour",
            name="linked_local_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Have you linked up with your local clinic?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagefour",
            name="linked_local_clinic_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagefour",
            name="receiving_arv",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Are you receiving ARVs?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagefour",
            name="receiving_arv_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagefour",
            name="receiving_fluconazole",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Are you receiving Fluconazole?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagefour",
            name="receiving_fluconazole_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestageone",
            name="linked_local_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Have you linked up with your local clinic?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestageone",
            name="linked_local_clinic_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestageone",
            name="receiving_arv",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Are you receiving ARVs?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestageone",
            name="receiving_arv_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestageone",
            name="receiving_fluconazole",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Are you receiving Fluconazole?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestageone",
            name="receiving_fluconazole_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagethree",
            name="linked_local_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Have you linked up with your local clinic?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagethree",
            name="linked_local_clinic_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagethree",
            name="receiving_arv",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Are you receiving ARVs?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagethree",
            name="receiving_arv_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagethree",
            name="receiving_fluconazole",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Are you receiving Fluconazole?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagethree",
            name="receiving_fluconazole_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagetwo",
            name="linked_local_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Have you linked up with your local clinic?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagetwo",
            name="linked_local_clinic_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagetwo",
            name="receiving_arv",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Are you receiving ARVs?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagetwo",
            name="receiving_arv_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagetwo",
            name="receiving_fluconazole",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="N/A",
                max_length=15,
                verbose_name="Are you receiving Fluconazole?",
            ),
        ),
        migrations.AddField(
            model_name="historicaladherencestagetwo",
            name="receiving_fluconazole_reason_no",
            field=edc_model.models.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If 'No', please specify reason ...",
            ),
        ),
    ]
