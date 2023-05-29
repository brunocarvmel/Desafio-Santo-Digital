import pytest
from fastapi.testclient import TestClient

from main import app, conn, cursor, Product

@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client

def setup_module(module):
    # Cria uma tabela temporária para os testes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_test (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            ProductNumber TEXT,
            Color TEXT,
            Price FLOAT
        )
    """)

def teardown_module(module):
    # Remove a tabela temporária após os testes
    cursor.execute("DROP TABLE IF EXISTS product_test")

def test_add_product(test_client):
    product_data = {
        "Name": "Produto Teste",
        "ProductNumber": "P123",
        "Color": "Red",
        "Price": 9.99
    }
    response = test_client.post("/products", json=product_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Produto Produto Teste foi criado !"}


def test_list_products(test_client):
    response = test_client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json()["products"], list)


def test_list_product(test_client):
    # Inserir um produto de teste
    cursor.execute(
        "INSERT INTO product_test (Name, ProductNumber, Color, Price) VALUES (?, ?, ?, ?)",
        ("Produto Teste", "P123", "Red", 9.99),
    )
    conn.commit()

    # Obter o ID do produto inserido
    product_id = cursor.lastrowid

    response = test_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["product"]["Id"] == product_id


def test_list_product_not_found(test_client):
    response = test_client.get("/products/999")
    assert response.status_code == 200
    assert response.json() == {"message": "Produto com ID 999 não encontrado"}


def test_update_product(test_client):
    # Inserir um produto de teste
    cursor.execute(
        "INSERT INTO product_test (Name, ProductNumber, Color, Price) VALUES (?, ?, ?, ?)",
        ("Produto Teste", "P123", "Red", 9.99),
    )
    conn.commit()

    # Obter o ID do produto inserido
    product_id = cursor.lastrowid

    updated_product_data = {
        "Name": "Produto Atualizado",
        "ProductNumber": "P456",
        "Color": "Blue",
        "Price": 19.99
    }
    response = test_client.put(f"/products/{product_id}", json=updated_product_data)
    assert response.status_code == 200
    assert response.json() == {"message": f"Produto com ID {product_id} atualizado com sucesso!"}


def test_update_product_not_found(test_client):
    updated_product_data = {
        "Name": "Produto Atualizado",
        "ProductNumber": "P456",
        "Color": "Blue",
        "Price": 19.99
    }
    response = test_client.put("/products/999", json=updated_product_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Produto com ID 999 não encontrado"}


def test_delete_product(test_client):
    # Inserir um produto de teste
    cursor.execute(
        "INSERT INTO product_test (Name, ProductNumber, Color, Price) VALUES (?, ?, ?, ?)",
        ("Produto Teste", "P123", "Red", 9.99),
    )
    conn.commit()

    # Obter o ID do produto inserido
    product_id = cursor.lastrowid

    response = test_client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Produto removido com sucesso!"}


def test_delete_product_not_found(test_client):
    response = test_client.delete("/products/999")
    assert response.status_code == 200
    assert response.json() == {"message": "Produto não encontrado!"}
