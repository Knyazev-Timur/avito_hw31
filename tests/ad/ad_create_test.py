import pytest
from rest_framework import status


@pytest.mark.django_db
def test_ad_create(client, user, category):
    data = {
        "author": user.username,
        "category": category.name,
        "name": "Крепкие бочки 40шт. состояние б/у, для хранения горячего масла",
        "price": 100
    }

    expected_response = {
        "id": 1,
        "author": user.username,
        "category": category.name,
        "is_published": False,
        "name": "Крепкие бочки 40шт. состояние б/у, для хранения горячего масла",
        "price": 100,
        "description": None,
        "image": None
    }
    response = client.post(f"/ads/", data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_response
