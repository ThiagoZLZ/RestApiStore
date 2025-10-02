from django.test import TestCase
from order.serializers.order_serializers import OrderSerializer
from order.models import Order
from product.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

class TestOrderSerializerTest(TestCase):
    def setUp(self):
        # Criar um usuário fake
        self.user = User.objects.create(username="testeuser")

        # Criar alguns produtos fake
        self.product1 = Product.objects.create(title="Produto A", price=10)
        self.product2 = Product.objects.create(title="Produto B", price=20)

    def test_create_order_with_valid_data(self):
        data = {
            "products_id": [self.product1.id, self.product2.id],
            "user": self.user.id
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        order = serializer.save()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product.count(), 2)
        self.assertEqual(order.product.first().title, "Produto A")

    def test_order_total_calculation(self):
        order = Order.objects.create(user=self.user)
        order.product.add(self.product1, self.product2)

        serializer = OrderSerializer(order)
        self.assertEqual(serializer.data["total"], 30.00)  # 10 + 20

    def test_invalid_order_missing_user(self):
        data = {
            "products_id": [self.product1.id]
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)

    def test_invalid_order_with_wrong_product_id(self):
        data = {
            "products_id": [999],  # ID inexistente
            "user": self.user.id
        }
        serializer = OrderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("products_id", serializer.errors)
