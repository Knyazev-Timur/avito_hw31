import pytest
from rest_framework import status

from tests.factories import AdFactory


@pytest.mark.django_db
def test_selection_create(client, user_and_token):
    user, access_token = user_and_token

    ads = AdFactory.create_batch(3)
    data = {
        "name": "Тестовая выборка",
        "items": [ad.pk for ad in ads]
    }

    expected_response = {
        "owner": user.username,
        "name": "Тестовая выборка",
        "items": [ad.pk for ad in ads]
    }

    response = client.post(f"/selection/", data=data, HTTP_AUTHORIZATION=f"Bearer {access_token}")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_response
