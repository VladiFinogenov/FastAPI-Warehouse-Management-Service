from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "Создан"
    SHIPPED = "Отправлен"
    DELIVERED = "Доставлен"
    CANCELED = "Отменен"
