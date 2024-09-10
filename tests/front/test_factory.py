from vkcc_auto import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_index(client):
    response = client.get('/')

    assert response.status_code == 200
    assert (b"<form action=\"/\" class=\"upload__form\" method=\"POST\" enctype=\"multipart/form-data\">"
            in response.data)
