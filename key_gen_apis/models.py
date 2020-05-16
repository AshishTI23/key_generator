from django.db import models


class Key(models.Model):
    api_key = models.CharField(max_length=20, null=False, unique=True)
    alive = models.DateTimeField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "key"
        ordering = ["pk"]

    def __str__(self):
        """__str__."""
        return str(self.api_key)
