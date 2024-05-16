from django.db import models as m


class Event(m.Model):
    name = m.CharField(max_length=255)
    start = m.DateTimeField()
    end = m.DateTimeField()

    created_at = m.DateTimeField(auto_now_add=True)
    updated_at = m.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return string representation of the model."""
        return f'Event(name="{self.name}", start="{self.start}", end="{self.end}")'
