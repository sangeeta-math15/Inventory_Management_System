from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Item
from django.contrib.auth.models import User
import json
import uuid


class ItemViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.item1 = Item.objects.create(
            name="Item 1",
            description="Test Item 1",
            quantity=10,
            price=100.00
        )
        self.item2 = Item.objects.create(
            name="Item 2",
            description="Test Item 2",
            quantity=20,
            price=200.00
        )

        self.create_url = reverse('item-list')

    def tearDown(self):
        pass

    def test_retrieve_item_by_uuid(self):
        url = reverse('item-detail', kwargs={'pk': self.item1.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], self.item1.name)

    def test_create_item(self):
        data = {
            "name": "New Item",
            "description": "A new test item",
            "quantity": 15,
            "price": 150.00
        }

        response = self.client.post(self.create_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], "New Item")

    def test_update_item(self):
        url = reverse('item-detail', kwargs={'pk': self.item1.id})
        updated_data = {
            "name": "Updated Item",
            "description": "Updated description",
            "quantity": 25,
            "price": 120.50
        }

        response = self.client.put(url, data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], "Updated Item")
        self.assertEqual(response.data['data']['quantity'], 25)

    def test_delete_item(self):
        url = reverse('item-detail', kwargs={'pk': self.item1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_nonexistent_item(self):
        non_existent_uuid = uuid.uuid4()
        url = reverse('item-detail', kwargs={'pk': non_existent_uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
