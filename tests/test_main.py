from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/docs")
    assert response.status_code == 200


def test_get_products_list_no_filters():
    """Test retrieving the first page of products without any filters."""
    response = client.get("/products/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "items" in data
    assert data["current_page"] == 1
    assert data["page_size"] == 10  # Default page size
    assert data["total_items"] > 0  
    assert data["total_pages"] > 0
    assert len(data["items"]) > 0

    # Check structure of the first item (TestProd1)
    item1 = next((item for item in data["items"] if item["id"] == 1), None)
    assert item1 is not None


def test_get_products_list_pagination():
    """Test pagination parameters."""
    response = client.get("/products/?page=1&page_size=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["current_page"] == 1
    assert data["page_size"] == 2
    assert data["total_items"] > 0
    assert data["total_pages"] > 0
    assert len(data["items"]) == 2

    response = client.get("/products/?page=2&page_size=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["current_page"] == 2
    assert data["page_size"] == 2
    assert data["total_items"] > 0
    assert data["total_pages"] > 0
    assert len(data["items"]) == 2


def test_get_products_filter_by_region():
    """Test filtering products by region_code."""
    response = client.get("/products/?region_code=MY")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["total_items"] > 0
    assert len(data["items"]) > 0

    response = client.get("/products/?region_code=SG")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["total_items"] > 0
    assert len(data["items"]) > 0


def test_get_products_filter_by_rental_period():
    """Test filtering products by rental_period_months."""
    response = client.get("/products/?rental_period_months=12")  # 12 months
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["total_items"] > 0
    assert len(data["items"]) > 0

    response = client.get("/products/?rental_period_months=3")  # 3 months
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["total_items"] > 0
    assert len(data["items"]) > 0


def test_get_products_filter_by_region_and_period():
    """Test filtering products by both region and rental period."""
    # TestProd1 in SG for 12 months
    response = client.get("/products/?region_code=SG&rental_period_months=12")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_items"] > 0
    assert len(data["items"]) > 0
    assert data["items"][0]["name"] != None

    # TestProd2 in MY for 12 months
    response = client.get("/products/?region_code=MY&rental_period_months=12")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_items"] > 0
    assert len(data["items"]) > 0

    # TestProd1 in SG for 3 months
    response = client.get("/products/?region_code=SG&rental_period_months=3")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_items"] > 0
    assert len(data["items"]) > 0

    # TestProd1 in MY for 3 months
    response = client.get("/products/?region_code=MY&rental_period_months=3")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_items"] > 0
    assert len(data["items"]) > 0


def test_get_product_by_id_success():
    """Test retrieving a single product by its ID successfully."""
    product_id = 1
    response = client.get(f"/products/{product_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["id"] == product_id
    assert len(data["attributes"]) > 0


def test_get_product_by_id_not_found():
    """Test retrieving a single product with an ID that does not exist."""
    product_id = 999
    response = client.get(f"/products/{product_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data == "Product not found"
