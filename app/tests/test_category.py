import pytest
import pytest_asyncio


class Test:

    @pytest_asyncio.fixture(autouse=True)
    async def setup(self):
        data = {
            "name": 'Category',
            "parent_id": None
        }
        self.category = data


    @pytest.mark.asyncio
    async def test_create_category(self, client):

        response = await client.post(url="/category/create", json=self.category)

        assert response.status_code == 201
        assert response.json()["transaction"] == "Successful"

    @pytest.mark.asyncio
    async def test_create_same_category(self, client):

        response = await client.post(url="/category/create", json=self.category)

        assert response.status_code == 400
        assert response.json()["detail"] == "Category with this name already exists"


    @pytest.mark.asyncio
    async def test_get_all_categories(self, client):
        response = await client.get("/category/all_categories")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert response.json()[0]['name'] == 'Category'
        assert response.json()[0]['id'] == 1


    @pytest.mark.asyncio
    async def test_update_categories(self, client, category):
        category_id = 1
        update_data = {
            "name": "new_category",
            "parent_id": None,
        }

        response = await client.put(f"/category/update_category/{category_id}", json=update_data)

        assert response.status_code == 200
        assert response.json()["transaction"] == "Category update is successful"


    @pytest.mark.asyncio
    async def test_delete_category(self, client):
        category_id = 1
        response = await client.delete(f"/category/delete/{category_id}")

        assert response.status_code == 200
        assert response.json()["transaction"] == "Category delete is successful"


