# Generated by Django 4.0.4 on 2022-05-25 16:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("effect_subject", "0067_historicalsubjectvisit_document_status_comments_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalfollowup",
            name="action_item",
        ),
        migrations.RemoveField(
            model_name="historicalfollowup",
            name="history_user",
        ),
        migrations.RemoveField(
            model_name="historicalfollowup",
            name="parent_action_item",
        ),
        migrations.RemoveField(
            model_name="historicalfollowup",
            name="related_action_item",
        ),
        migrations.RemoveField(
            model_name="historicalfollowup",
            name="site",
        ),
        migrations.RemoveField(
            model_name="historicalfollowup",
            name="subject_visit",
        ),
        migrations.DeleteModel(
            name="Followup",
        ),
        migrations.DeleteModel(
            name="HistoricalFollowup",
        ),
    ]
