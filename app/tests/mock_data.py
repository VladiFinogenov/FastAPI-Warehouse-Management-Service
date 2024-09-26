MOCK_CREATE_ORDER_DATA = {
    "items": [
        {
            "product_id": 1,
            "quantity": 2
        },
    ]
}

MOCK_UPDATE_STATUS_ORDER_DATA = {
    "status": "Доставлен"
}

MOCK_PRODUCT_DATA = [
    {
        "name": "Product1",
        "description": "Product one",
        "price": 100,
        "quantity": 2,
    },
    {
        "name": "Product2",
        "description": "Product two",
        "price": 150,
        "quantity": 2,
    },
]

MOCK_NOT_QUANTITY_PRODUCT_DATA = [
    {
        "name": "Product1",
        "description": "Product one",
        "price": 100,
        "quantity": 0,
    },
]

MOCK_NOT_QUANTITY_ORDER_DATA = {
    "items": [
        {
            "product_id": 1,
            "quantity": 10
        },
    ]
}


MOCK_PRODUCT_NOT_FOUND_ORDER_DATA = {
    "items": [
        {
            "product_id": 0,
            "quantity": 5
        },
    ]
}
