from vkcc_auto.filehandler import allowed_file


def test_allowed_file():
    assert allowed_file("test_file.xlsx")
    assert not allowed_file("test_file.txt")


def test_index_post(client, resources, invalid_wb_file):
    response = client.post("/", content_type='multipart/form-data')
    assert response.status_code == 302

    response = client.post("/", data={
        "file": ((resources / "input_example.xlsx").open("rb"), ""),
    }, content_type='multipart/form-data')
    assert response.status_code == 302

    response = client.post("/", data={
        "file": ((resources / "input_example.xlsx").open("rb"), "input_example.txt"),
    }, content_type='multipart/form-data')
    assert response.status_code == 302

    response = client.post("/", data={
        "file": (invalid_wb_file.open("rb"), "input_example.xlsx"),
    }, content_type='multipart/form-data')
    assert response.status_code == 302


def test_index_token(app, client, resources):
    app.config.update({
        "TOKEN": "1234"
    })
    response = client.post("/", data={
        "file": ((resources / "input_example.xlsx").open("rb"), "input_example.xlsx"),
    }, content_type='multipart/form-data')
    assert response.status_code == 302


def test_index_index(app, client, resources):
    app.config.update({
        "PAYLOAD_FIRST_ROW": -2,
    })
    response = client.post("/", data={
        "file": ((resources / "input_example.xlsx").open("rb"), "input_example.xlsx"),
    }, content_type='multipart/form-data')
    assert response.status_code == 302


def test_index_valid(client, resources):
    response = client.post("/", data={
        "file": ((resources / "input_example.xlsx").open("rb"), "input_example.xlsx"),
    }, content_type='multipart/form-data')
    assert response.status_code == 200


