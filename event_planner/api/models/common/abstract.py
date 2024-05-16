from django.db import models as m


class ModelWithTimestamps(m.Model):
    """An abstract model with the two common timestamps: created_at and updated_at."""

    created_at = m.DateTimeField(
        auto_now_add=True,
        help_text="The datetime at which the section was created",
    )
    updated_at = m.DateTimeField(
        auto_now=True,
        help_text="The datetime at which the section was last updated",
    )

    class Meta:
        abstract = True
