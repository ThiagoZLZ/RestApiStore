from django.test import TestCase
from product.models.category import Category
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer

class TestProductSerializer(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(title="Categoria A", slug="categoria-a")
        self.category2 = Category.objects.create(title="Categoria B", slug="categoria-b")

        self.valid_data = {
            "title": "Produto Teste",
            "description": "Descrição do produto",
            "price": 100,
            "active": True,
            "categories_id": [self.category1.id, self.category2.id]
        }

    def test_create_product_with_valid_data(self):
        serializer = ProductSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.title, "Produto Teste")
        self.assertEqual(product.price, 100)
        self.assertEqual(product.category.count(), 2)
        self.assertIn(self.category1, product.category.all())
        self.assertIn(self.category2, product.category.all())

    def test_invalid_product_missing_title(self):
        data = self.valid_data.copy()
        data.pop("title")
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
