from rest_framework import serializers
from product.models import Product
from order.models import Order
from product.serializers.product_serializer import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=True)
    products_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, many=True
    )
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['product', 'total', 'user', 'products_id']
        extra_kwargs = {'product': {'required': False}, 'user': {'read_only': False}}

    def get_total(self, instance):
        return sum([product.price for product in instance.product.all()])

    def validate(self, attrs):
        # Pega o usuário do contexto (request) ou do data
        request = self.context.get('request')
        user = getattr(request, 'user', None) if request else attrs.get('user')

        if not user or user.is_anonymous:
            raise serializers.ValidationError({'user': 'Usuário é obrigatório.'})

        # Adiciona user no validated_data para o create()
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        products_data = validated_data.pop('products_id', [])
        user = validated_data.pop('user')

        order = Order.objects.create(user=user)
        order.product.set(products_data)
        return order


