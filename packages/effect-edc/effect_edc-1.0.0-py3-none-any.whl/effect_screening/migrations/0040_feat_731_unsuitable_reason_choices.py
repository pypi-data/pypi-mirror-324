# Generated by Django 4.2.6 on 2024-03-12 12:48
# Last modified on 2024-04-18 13:53


from django.db import migrations
from django.db.migrations import RunPython
from edc_constants.constants import DECEASED, NOT_APPLICABLE, OTHER, YES
from edc_utils import get_utcnow
from tqdm import tqdm

from effect_screening.constants import G4_RAISED_CREATININE, UNABLE_TO_CONTACT


def matches_unable_to_contact(reasons_unsuitable: str) -> bool:
    return reasons_unsuitable.lower() in [
        reason.lower()
        for reason in [
            "unable to contact patient.",
            "unable to contact patient",
            "unable to contact patient..",
            "unable to contact participant",
            "unable to contact",
            "cannot contact patient",
            "cannot contact patient.",
            "not able to contact the patient.",
            "patient cannot be contacted.",
        ]
    ]


def matches_deceased(reasons_unsuitable: str) -> bool:
    return reasons_unsuitable.lower() in [
        reason.lower()
        for reason in [
            "patient died prior to screening",
            "died prior to screening",
            "patient died prior to screening.",
        ]
    ]


def matches_g4_raised_creatinine(reasons_unsuitable: str) -> bool:
    return (
        reasons_unsuitable.lower()
        in [
            reason.lower()
            for reason in [
                "meets late exclusion criteria (renal)",
                "late exclusion criteria (renal function)",
                "Renal failure",
                "Renal failure - Grd 4 DAIDS",
                "Met late exclusion criteria - Creatinine high",
                "DAIDS Grade 4 Creatinine at screening.",
                (
                    "Meets late exclusion criteria: DAIDS grade 4 "
                    "abnormalities of creatinine level"
                ),
                "known to have DAIDS g4 renal impairment",
            ]
        ]
        or (
            (
                reasons_unsuitable.lower().startswith("Renal failure creat ".lower())
                or reasons_unsuitable.lower().startswith("Creat ".lower())
            )
            and reasons_unsuitable.lower().endswith(
                ", will meet late exclusion criteria".lower()
            )
        )
        or (
            reasons_unsuitable.lower().startswith("Chronic renal failure creat ".lower())
            and reasons_unsuitable.lower().endswith(
                ". Will meet late exclusion criteria.".lower()
            )
        )
        or (
            reasons_unsuitable.lower().startswith("Creatinine = ".lower())
            and reasons_unsuitable.lower().endswith(
                " (DAIDS Grade 4 - exclusion criteria)".lower()
            )
        )
    )


def update_screening_unsuitable(apps, schema_editor):
    model_cls = apps.get_model("effect_screening.subjectscreening")
    qs = model_cls.objects.all()
    total = qs.count()
    print(f"\nProcessing {total} Subject Screening instances for unsuitable_reasons ...")
    for obj in tqdm(qs, total=total):
        if matches_unable_to_contact(obj.reasons_unsuitable):
            obj.unsuitable_reason = UNABLE_TO_CONTACT
            if obj.unsuitable_agreed == YES:
                obj.unsuitable_agreed = NOT_APPLICABLE  # see #731

        elif matches_deceased(obj.reasons_unsuitable):
            obj.unsuitable_reason = DECEASED
            if obj.unsuitable_agreed == YES:
                obj.unsuitable_agreed = NOT_APPLICABLE  # see #731

        elif matches_g4_raised_creatinine(obj.reasons_unsuitable):
            obj.unsuitable_reason = G4_RAISED_CREATININE
            if obj.unsuitable_agreed == YES:
                obj.unsuitable_agreed = NOT_APPLICABLE  # see #731

        elif obj.reasons_unsuitable:
            obj.unsuitable_reason = OTHER
            obj.unsuitable_reason_other = obj.reasons_unsuitable

        if obj.unsuitable_reason and obj.unsuitable_reason != NOT_APPLICABLE:
            obj.modified = get_utcnow()
            obj.user_modified = __name__ if len(__name__) <= 50 else f"{__name__[:46]} ..."

            update_fields = [
                "unsuitable_reason",
                "modified",
                "user_modified",
            ]
            if obj.unsuitable_reason != OTHER:
                update_fields.append("unsuitable_agreed")
            else:
                update_fields.append("unsuitable_reason_other"),

            obj.save_base(update_fields=update_fields)

            print(
                f" * Updating '{obj.screening_identifier}' with '{obj.unsuitable_reason=}' "
                # f"from '{obj.reasons_unsuitable=}'"
            )

    print("Final `unsuitable_reason` DB update summary ...")
    print(f" * {model_cls.objects.filter(unsuitable_reason=UNABLE_TO_CONTACT).count()=}")
    print(f" * {model_cls.objects.filter(unsuitable_reason=DECEASED).count()=}")
    print(f" * {model_cls.objects.filter(unsuitable_reason=G4_RAISED_CREATININE).count()=}")
    print(f" * {model_cls.objects.filter(unsuitable_reason=OTHER).count()=}")
    print("Done.")


class Migration(migrations.Migration):

    dependencies = [
        ("effect_screening", "0039_historicalsubjectscreening_unsuitable_reason_and_more"),
    ]

    operations = [RunPython(update_screening_unsuitable)]
