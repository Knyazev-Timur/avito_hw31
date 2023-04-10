import pytest


@pytest.fixture
@pytest.mark.django_db
def user_and_token(client, django_user_model):
    username = "test_user"
    password = "test_password"

    test_user = django_user_model.objects.create_user(
        username=username, password=password, role="admin"
    )

    response = client.post(
        "/user/token/",
        {"username": username, "password": password},
        format='json'
    )
    return test_user, response.data["access"]
