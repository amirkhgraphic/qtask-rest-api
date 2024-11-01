from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import KeyValue


class KeyValueModelTests(TestCase):

    def setUp(self):
        self.parent_kv_nested = KeyValue.objects.create(
            key='parent_nested',
            value='parent_value',
            type=KeyValue.KeyValueTypeChoices.NESTED
        )
        self.parent_kv_non_nested = KeyValue.objects.create(
            key='parent_non_nested',
            value='parent_value',
            type=KeyValue.KeyValueTypeChoices.STRING
        )

    def test_unique_key_validation(self):
        """
        Ensure that duplicate keys raise a ValidationError.
        """
        KeyValue.objects.create(
            key='unique_key',
            value='value1',
            type=KeyValue.KeyValueTypeChoices.STRING,
            parent=self.parent_kv_nested
        )

        with self.assertRaises(ValidationError) as error:
            KeyValue.objects.create(
                key='unique_key',
                value='value2',
                type=KeyValue.KeyValueTypeChoices.STRING,
                parent=self.parent_kv_nested
            )

        self.assertEqual(
            error.exception.message,
            "A key 'unique_key' already exists in the same namespace."
        )

    def test_boolean_type_validation(self):
        """
        Ensure that the value is a boolean for BOOLEAN type.
        """
        with self.assertRaises(ValidationError) as error:
            KeyValue.objects.create(
                key='boolean_key',
                value='not_a_boolean',
                type=KeyValue.KeyValueTypeChoices.BOOLEAN,
                parent=self.parent_kv_nested
            )

        self.assertEqual(error.exception.message, "For a Boolean type, value must be a boolean (true/false).")

    def test_number_type_validation(self):
        """
        Ensure that the value is an integer for NUMBER type.
        """
        with self.assertRaises(ValidationError) as error:
            KeyValue.objects.create(
                key='number_key',
                value='not_an_integer',
                type=KeyValue.KeyValueTypeChoices.NUMBER,
                parent=self.parent_kv_nested
            )

        self.assertEqual(error.exception.message, "For a Number type, value must be an integer.")

    def test_array_type_validation(self):
        """
        Ensure that the value is a list for ARRAY type.
        """
        with self.assertRaises(ValidationError) as error:
            KeyValue.objects.create(
                key='array_key',
                value='not_a_list',
                type=KeyValue.KeyValueTypeChoices.ARRAY,
                parent=self.parent_kv_nested
            )

        self.assertEqual(error.exception.message, "For an Array type, value must be a list.")

    def test_parent_key_validation(self):
        """
        Ensure that the parent key is of type NESTED.
        """
        with self.assertRaises(ValidationError) as error:
            KeyValue.objects.create(
                key='child_key',
                value='child_value',
                type=KeyValue.KeyValueTypeChoices.STRING,
                parent=self.parent_kv_non_nested
            )

        self.assertEqual(error.exception.message, "Parent key should be a Nested type key-value")


class KeyValueAPITests(APITestCase):
    def setUp(self):
        self.parent_kv = KeyValue.objects.create(
            key='parent',
            type=KeyValue.KeyValueTypeChoices.NESTED,
        )

    def test_create_key_value(self):
        url = reverse('pairs:list-create')
        data = {
            'key': 'test_key',
            'value': 'some value',
            'type': KeyValue.KeyValueTypeChoices.STRING,
            'parent': self.parent_kv.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(KeyValue.objects.count(), 2)
        self.assertEqual(KeyValue.objects.get(id=2).key, 'test_key')

    def test_create_key_value_with_invalid_type(self):
        url = reverse('pairs:list-create')
        data = {
            'key': 'boolean_key',
            'value': 'not a boolean',
            'type': KeyValue.KeyValueTypeChoices.BOOLEAN,
            'parent': self.parent_kv.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'For a Boolean type, value must be a boolean (true/false).',
            response.data['invalid data']
        )

    def test_create_key_value_with_duplicate_key(self):
        url = reverse('pairs:list-create')
        data = {
            'key': 'duplicate_key',
            'value': 'some value',
            'type': KeyValue.KeyValueTypeChoices.STRING,
            'parent': self.parent_kv.id,
        }
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "A key 'duplicate_key' already exists in the same namespace.",
            response.data['invalid data']
        )

    def test_get_key_value_list(self):
        [
            KeyValue.objects.create(
                key=f'test_key{i}',
                value=list(range(1, 6)),
                type=KeyValue.KeyValueTypeChoices.ARRAY,
                parent=self.parent_kv
            ) for i in range(2)
        ]

        url = reverse('pairs:list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data[0]['children']), 2)

    def test_update_key_value(self):
        key_value = KeyValue.objects.create(
            key='update_key',
            value='old value',
            type=KeyValue.KeyValueTypeChoices.STRING,
            parent=self.parent_kv
        )
        url = reverse('pairs:retrieve-update-delete', args=[key_value.id])
        data = {
            'key': 'updated_key',
            'value': 'new value',
            'type': KeyValue.KeyValueTypeChoices.STRING,
            'parent': self.parent_kv.id,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        key_value.refresh_from_db()
        self.assertEqual(key_value.key, 'updated_key')
        self.assertEqual(key_value.value, 'new value')

    def test_delete_key_value(self):
        key_value = KeyValue.objects.create(
            key='delete_key',
            value=20,
            type=KeyValue.KeyValueTypeChoices.NUMBER,
            parent=self.parent_kv
        )
        url = reverse('pairs:retrieve-update-delete', args=[key_value.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(KeyValue.objects.count(), 1)
