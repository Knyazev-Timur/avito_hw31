import pytest
from rest_framework import status

from ads.serializers import AdListSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_list_ad(client):
    ads = AdFactory.create_batch(4)
    response = client.get(f"/ads/")
    expected_response = {
        "count": 4,
        "next": None,
        "previous": None,
        "results": AdListSerializer(ads, many=True).data
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response
