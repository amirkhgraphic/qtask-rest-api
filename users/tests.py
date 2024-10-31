from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserTests(APITestCase):

    def setUp(self):
        # Create a user for the tests
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="testuser@example.com"
        )
        self.token_url = reverse('users:token_obtain_pair')
        token_data = {"username": "testuser", "password": "password123"}
        token_response = self.client.post(self.token_url, token_data, format='json')
        self.access_token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_user_registration(self):
        """
        Ensure we can create a new user via the registration endpoint.
        """
        url = reverse('users:signup')
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username="newuser").email, "newuser@example.com")

    def test_user_retrieve(self):
        """
        Ensure we can retrieve a user by ID.
        """
        url = reverse('users:retrieve-update-delete', kwargs={"user_id": self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        """
        Ensure we can update a user by ID.
        """
        url = reverse('users:retrieve-update-delete', kwargs={"user_id": self.user.id})
        update_data = {"username": "updateduser"}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(id=self.user.id).username, "updateduser")

    def test_user_delete(self):
        """
        Ensure we can delete a user by ID.
        """
        url = reverse('users:retrieve-update-delete', kwargs={"user_id": self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.filter(id=self.user.id).count(), 0)

    def test_user_list(self):
        """
        Ensure admin can list all users.
        """
        User.objects.create_superuser(
            username="adminuser",
            password="password123",
            email="admin@example.com"
        )

        # Authenticate
        token_data = {"username": "adminuser", "password": "password123"}
        token_response = self.client.post(self.token_url, token_data, format='json')
        access_token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        # API call
        url = reverse('users:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
