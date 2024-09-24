import pytest
import pytest_asyncio


class Test:

    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, product):

        # TODO категория создается под индексом 2 автоматически
        self.product = {
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "image_url": product.image_url,
            "stock": product.stock,
            "category_id": 2,
        }


    @pytest.mark.asyncio
    async def test_create_product(self, client, category):
        response = await client.post(url="/products/create", json=self.product)

        assert response.status_code == 200
        assert response.json()["transaction"] == "Successful"


    @pytest.mark.asyncio
    async def test_get_all_products(self, client):
        response = await client.get("/products/")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert response.json()[0]['name'] == self.product["name"]
        assert response.json()[0]['id'] == 1
    #
    #
    # @pytest.mark.asyncio
    # async def test_update_product(self, client):
    #     category_id = 1
    #     update_data = {
    #         "name": "new_category",
    #         "parent_id": None,
    #         "category_id": category_id
    #     }
    #
    #     response = await client.put(f"/category/update_category/{category_id}", json=update_data)
    #
    #     assert response.status_code == 200
    #     assert response.json()["transaction"] == "Category update is successful"
    #
    #
    # @pytest.mark.asyncio
    # async def test_delete_product(self, client):
    #     category_id = 1
    #     response = await client.delete(f"/category/delete/{category_id}")
    #
    #     assert response.status_code == 200
    #     assert response.json()["transaction"] == "Category delete is successful"