import pytest
import pytest_asyncio


class TestOrder:

    @pytest_asyncio.fixture(autouse=True)
    async def setup(self):

        self.product = {
            "name": 'Product1',
            "description": 'Test',
            "price": 100,
            "quantity": 5,
        }


    @pytest.mark.asyncio
    async def test_01_create_product(self, client):
        response = await client.post(url="/api/products", json=self.product)

        assert response.status_code == 201
        assert response.json()["transaction"] == "Товар успешно создан"


    @pytest.mark.asyncio
    async def test_02_create_product(self, client):
        new_product = {
            "name": 'Product2',
            "description": 'Test',
            "price": 150,
            "quantity": 10,
            "is_active": True,
        }

        response = await client.post(url="/api/products", json=new_product)

        assert response.status_code == 201
        assert response.json()["transaction"] == "Товар успешно создан"


    @pytest.mark.asyncio
    async def test_update_products(self, client):
        update_product = {
            "name": "Product-new",
            "description": "Test2",
            "price": 100,
            "quantity": 5,
        }
        response = await client.put(f"/api/products/{2}?product_id=2", json=update_product)

        updated_product = response.json()
        assert response.status_code == 200
        assert updated_product["name"] == update_product["name"]
        assert updated_product["description"] == update_product["description"]
        assert updated_product["price"] == update_product["price"]
        assert updated_product["quantity"] == update_product["quantity"]


    @pytest.mark.asyncio
    async def test_get_all_products(self, client):
        response = await client.get("/api/products")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 2


    @pytest.mark.asyncio
    async def test_delete_null_products(self, client):
        response = await client.delete(f"/api/products/{0}?product_id=0")

        assert response.status_code == 404
        assert response.json()['detail'] == "Product not found"


    @pytest.mark.asyncio
    async def test_delete_products(self, client):
        response = await client.delete(f"/api/products/{2}?product_id=2")
        response_all = await client.get("/api/products")

        assert response.status_code == 201
        assert response.json()['transaction'] == "Product deleted"
        assert len(response_all.json()) == 1
