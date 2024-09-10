from vkcc_auto.filehandler import allowed_file


def test_allowed_file():
    assert allowed_file("test_file.xlsx")
    assert not allowed_file("test_file.txt")


# def test_index_post(client):
#     response = client.post('/')
