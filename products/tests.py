from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework import status


from rest_framework.test import APITestCase
from rest_framework import status

from .models import Brand, Category, Perfume


class PerfumeAPITest(APITestCase):

    def setUp(self):

        self.brand = Brand.objects.create(
            name="Dior"
        )

        self.category = Category.objects.create(
            name="Men"
        )

        self.perfume = Perfume.objects.create(
            name="Sauvage",
            description="Luxury perfume",
            price=5000,
            stock=10,
            brand=self.brand,
            category=self.category
        )

    def test_get_perfumes(self):

        response = self.client.get(
            "/api/products/perfumes/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data),
            1
        )

    def test_get_single_perfume(self):

        response = self.client.get(
            f"/api/products/perfumes/{self.perfume.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["name"],
            "Sauvage"
        )

    def test_search_perfume(self):

        response = self.client.get(
            "/api/products/perfumes/?search=Sauvage"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_filter_by_category(self):

        response = self.client.get(
            "/api/products/perfumes/?category=Men"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_filter_by_price(self):

        response = self.client.get(
            "/api/products/perfumes/?min_price=1000&max_price=6000"
        )

        self.assertEqual(
            response.status_code,
            200
        )