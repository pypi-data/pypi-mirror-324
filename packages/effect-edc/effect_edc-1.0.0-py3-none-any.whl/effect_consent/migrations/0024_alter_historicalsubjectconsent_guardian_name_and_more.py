# Generated by Django 5.1.5 on 2025-01-22 04:21

import django_crypto_fields.fields.encrypted_char_field
import django_crypto_fields.fields.lastname_field
import edc_consent.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("effect_consent", "0023_create_off_schedule_consent_v2_action_items"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="guardian_name",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text="Required only if participant is a minor.<BR>Format is &#x27;LASTNAME, FIRSTNAME&#x27;. All uppercase separated by a comma. (Encryption: RSA local)",
                max_length=71,
                null=True,
                validators=[edc_consent.validators.FullNameValidator()],
                verbose_name="Guardian's last and first name",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="is_incarcerated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="If 'Yes' STOP participant cannot be consented.",
                max_length=3,
                null=True,
                validators=[edc_consent.validators.eligible_if_no],
                verbose_name="Is the participant under involuntary incarceration?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsent",
            name="witness_name",
            field=django_crypto_fields.fields.lastname_field.LastnameField(
                blank=True,
                help_text="Required only if participant is illiterate.<BR>Format is &#x27;LASTNAME, FIRSTNAME&#x27;. All uppercase separated by a comma. (Encryption: RSA local)",
                max_length=71,
                null=True,
                validators=[edc_consent.validators.FullNameValidator()],
                verbose_name="Witness's last and first name",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv1",
            name="guardian_name",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text="Required only if participant is a minor.<BR>Format is &#x27;LASTNAME, FIRSTNAME&#x27;. All uppercase separated by a comma. (Encryption: RSA local)",
                max_length=71,
                null=True,
                validators=[edc_consent.validators.FullNameValidator()],
                verbose_name="Guardian's last and first name",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv1",
            name="is_incarcerated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="If 'Yes' STOP participant cannot be consented.",
                max_length=3,
                null=True,
                validators=[edc_consent.validators.eligible_if_no],
                verbose_name="Is the participant under involuntary incarceration?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv1",
            name="witness_name",
            field=django_crypto_fields.fields.lastname_field.LastnameField(
                blank=True,
                help_text="Required only if participant is illiterate.<BR>Format is &#x27;LASTNAME, FIRSTNAME&#x27;. All uppercase separated by a comma. (Encryption: RSA local)",
                max_length=71,
                null=True,
                validators=[edc_consent.validators.FullNameValidator()],
                verbose_name="Witness's last and first name",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv2",
            name="guardian_name",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text="Required only if participant is a minor.<BR>Format is &#x27;LASTNAME, FIRSTNAME&#x27;. All uppercase separated by a comma. (Encryption: RSA local)",
                max_length=71,
                null=True,
                validators=[edc_consent.validators.FullNameValidator()],
                verbose_name="Guardian's last and first name",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv2",
            name="is_incarcerated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="If 'Yes' STOP participant cannot be consented.",
                max_length=3,
                null=True,
                validators=[edc_consent.validators.eligible_if_no],
                verbose_name="Is the participant under involuntary incarceration?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectconsentv2",
            name="witness_name",
            field=django_crypto_fields.fields.lastname_field.LastnameField(
                blank=True,
                help_text="Required only if participant is illiterate.<BR>Format is &#x27;LASTNAME, FIRSTNAME&#x27;. All uppercase separated by a comma. (Encryption: RSA local)",
                max_length=71,
                null=True,
                validators=[edc_consent.validators.FullNameValidator()],
                verbose_name="Witness's last and first name",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="guardian_name",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text="Required only if participant is a minor.<BR>Format is &#x27;LASTNAME, FIRSTNAME&#x27;. All uppercase separated by a comma. (Encryption: RSA local)",
                max_length=71,
                null=True,
                validators=[edc_consent.validators.FullNameValidator()],
                verbose_name="Guardian's last and first name",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="is_incarcerated",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="If 'Yes' STOP participant cannot be consented.",
                max_length=3,
                null=True,
                validators=[edc_consent.validators.eligible_if_no],
                verbose_name="Is the participant under involuntary incarceration?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsent",
            name="witness_name",
            field=django_crypto_fields.fields.lastname_field.LastnameField(
                blank=True,
                help_text="Required only if participant is illiterate.<BR>Format is &#x27;LASTNAME, FIRSTNAME&#x27;. All uppercase separated by a comma. (Encryption: RSA local)",
                max_length=71,
                null=True,
                validators=[edc_consent.validators.FullNameValidator()],
                verbose_name="Witness's last and first name",
            ),
        ),
    ]
