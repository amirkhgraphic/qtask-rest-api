from django.db import models
from django.core.exceptions import ValidationError


class KeyValue(models.Model):
    class KeyValueTypeChoices(models.TextChoices):
        NESTED = 'NESTED', 'Nested'
        STRING = 'STRING', 'String'
        NUMBER = 'NUMBER', 'Number'
        BOOLEAN = 'BOOLEAN', 'Boolean'
        ARRAY = 'ARRAY', 'Array'

    key = models.CharField(max_length=127)
    type = models.CharField(
        max_length=7,
        choices=KeyValueTypeChoices.choices,
        default=KeyValueTypeChoices.NESTED,
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
    )
    value = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self, *args, **kwargs):
        """
        Ensure the key is unique across all key-value types.
        Ensure the type of the pair is compatible with its value.
        """
        duplicate_kv = KeyValue.objects.filter(key=self.key, parent=self.parent)
        if duplicate_kv.exists() and duplicate_kv.first() != self:
            raise ValidationError(f"A key '{self.key}' already exists in the same namespace.")

        if self.type == self.KeyValueTypeChoices.BOOLEAN and not isinstance(self.value, bool):
            raise ValidationError("For a Boolean type, value must be a boolean (true/false).")
        elif self.type == self.KeyValueTypeChoices.NUMBER and not isinstance(self.value, int):
            raise ValidationError("For a Number type, value must be an integer.")
        elif self.type == self.KeyValueTypeChoices.ARRAY and not isinstance(self.value, list):
            raise ValidationError("For an Array type, value must be a list.")

        if self.parent and self.parent.type != self.KeyValueTypeChoices.NESTED:
            raise ValidationError("Parent key should be a Nested type key-value")

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.key} <{self.type}>" +
            (f": {self.value}" if self.type != self.KeyValueTypeChoices.NESTED else "")
        )
