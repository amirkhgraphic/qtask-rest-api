from rest_framework import serializers

from .models import KeyValue


class KeyValueSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent = serializers.PrimaryKeyRelatedField(queryset=KeyValue.objects.none(), allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = KeyValue.objects.filter(type=KeyValue.KeyValueTypeChoices.NESTED)

    def get_children(self, instance):
        """Recursively serialize nested key-value pairs."""
        if instance.children.exists():
            return KeyValueSerializer(instance.children.all(), many=True).data
        return []

    def validate(self, data):
        if KeyValue.objects.filter(key=data["key"], parent=data["parent"]).exists():
            raise serializers.ValidationError(f"A key '{data['key']}' already exists in the same namespace.")

        if data["type"] == KeyValue.KeyValueTypeChoices.BOOLEAN and not isinstance(data["value"], bool):
            raise serializers.ValidationError("For a Boolean type, value must be a boolean (true/false).")
        elif data["type"] == KeyValue.KeyValueTypeChoices.NUMBER and not isinstance(data["value"], int):
            raise serializers.ValidationError("For a Number type, value must be an integer.")
        elif data["type"] == KeyValue.KeyValueTypeChoices.ARRAY and not isinstance(data["value"], list):
            raise serializers.ValidationError("For an Array type, value must be a list.")

        return data

    class Meta:
        model = KeyValue
        fields = [
            'key',
            'value',
            'type',
            'parent',
            'children',
            'created_at',
        ]

        extra_kwargs = {
            'parent': {
                'write_only': True
            },
        }
