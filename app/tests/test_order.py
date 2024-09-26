import pytest

from app.tests.mock_data import (MOCK_CREATE_ORDER_DATA,
                                 MOCK_NOT_QUANTITY_ORDER_DATA,
                                 MOCK_PRODUCT_DATA,
                                 MOCK_PRODUCT_NOT_FOUND_ORDER_DATA,
                                 MOCK_UPDATE_STATUS_ORDER_DATA)


class Test:


    @pytest.mark.asyncio
    async def test_01_create_order(self, client):
        response = await client.post(url="/api/products", json=MOCK_PRODUCT_DATA[0])
        response = await client.post(url="/api/products", json=MOCK_PRODUCT_DATA[1])

        response = await client.post(url="/api/orders", json=MOCK_CREATE_ORDER_DATA)

        assert response.status_code == 201
        assert response.json()["transaction"] == "Заказ успешно создан"


    @pytest.mark.asyncio
    async def test_create_not_quantity_product(self, client):

        response = await client.post(url="/api/orders", json=MOCK_NOT_QUANTITY_ORDER_DATA)

        assert response.status_code == 400
        assert response.json()["detail"] == "Недостаточно товара на складе"


    @pytest.mark.asyncio
    async def test_create_product_not_found(self, client):

        response = await client.post(url="/api/orders", json=MOCK_PRODUCT_NOT_FOUND_ORDER_DATA)

        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"


    @pytest.mark.asyncio
    async def test_all_orders(self, client):

        response = await client.get(f"/api/orders")

        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) == 1

        status_order = response.json()
        assert status_order[0]["status"] == 'Создан'

    @pytest.mark.asyncio
    async def test_update_statys_order(self, client):
        response = await client.put(f"/api/orders/{1}?order_id=1", json=MOCK_UPDATE_STATUS_ORDER_DATA)

        assert response.status_code == 200


    @pytest.mark.asyncio
    async def test_detail_order(self, client):
        response = await client.get(f"/api/orders/{1}?order_id=1")

        assert response.status_code == 200
        status_order = response.json()
        assert status_order["status"] == 'Доставлен'
