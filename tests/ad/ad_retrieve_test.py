import pytest
from rest_framework import status

from ads.serializers import AdDetailSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_retrieve(client, user_and_token):
    user, access_token = user_and_token
    ad = AdFactory.create()
    response = client.get(f"/ads/{ad.pk}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.get(f"/ads/{ad.pk}/", HTTP_AUTHORIZATION=f"Bearer {access_token}")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == AdDetailSerializer(ad).data
