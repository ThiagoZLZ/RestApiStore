
import pytest
from product.models import Product, Category
from product.serializers.product_serializer import ProductSerializer

@pytest.mark.django_db
def test_product_serializer_serialization():
    # cria categorias com os campos corretos
    cat1 = Category.objects.create(title="Roupas", slug="roupas")
    cat2 = Category.objects.create(title="Acessórios", slug="acessorios")

    # cria produto e associa categorias
    product = Product.objects.create(
        title="Camiseta",
        description="Camiseta 100% algodão",
        price=59,
        active=True
    )
    product.category.add(cat1, cat2)

    # serializa o produto
    serializer = ProductSerializer(product)
    data = serializer.data

    # checa os campos principais
    assert data["title"] == "Camiseta"
    assert data["description"] == "Camiseta 100% algodão"
    assert data["price"] == 59
    assert data["active"] is True

    # checa categorias
    assert len(data["category"]) == 2
    assert any(cat["title"] == "Roupas" for cat in data["category"])
    assert any(cat["title"] == "Acessórios" for cat in data["category"])


@pytest.mark.django_db
def test_product_serializer_validation_invalid():
    # dados inválidos
    invalid_data = {
        "title": "",
        "description": "",
        "price": "",
        "active": "",
        "category": []
    }
    serializer = ProductSerializer(data=invalid_data)

    assert not serializer.is_valid()
    assert "title" in serializer.errors
    assert "price" in serializer.errors
    assert "active" in serializer.errors

############################# TESTE #2 ####################################
    
import pytest
from product.models import Category
from product.serializers.category_serializer import CategorySerializer

@pytest.mark.django_db
def test_category_serializer_serialization():
    # cria uma categoria
    category = Category.objects.create(
        title="Roupas",
        slug="roupas",
        description="Categoria de roupas",
        active=True
    )

    # serializa a categoria
    serializer = CategorySerializer(category)
    data = serializer.data

    # checa os campos
    assert data["title"] == "Roupas"
    assert data["slug"] == "roupas"
    assert data["description"] == "Categoria de roupas"
    assert data["active"] is True

@pytest.mark.django_db
def test_category_serializer_validation_invalid():
    # dados inválidos (slug é obrigatório)
    invalid_data = {
        "title": "",
        "slug": "",
        "description": "",
        "active": ""
    }
    serializer = CategorySerializer(data=invalid_data)

    assert not serializer.is_valid()
    assert "title" in serializer.errors
    assert "slug" in serializer.errors

