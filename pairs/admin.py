from django.contrib import admin

from .models import KeyValue


class KeyValueInline(admin.TabularInline):
    model = KeyValue
    extra = 1
    fields = ('key', 'type', 'value')


@admin.register(KeyValue)
class KeyValueAdmin(admin.ModelAdmin):
    list_display = ('key', 'type', 'parent', 'value')
    search_fields = ('key',)
    inlines = [KeyValueInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = KeyValue.objects.filter(type=KeyValue.KeyValueTypeChoices.NESTED)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
