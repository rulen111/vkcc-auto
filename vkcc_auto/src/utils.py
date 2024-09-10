class InvalidTokenError(Exception):
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return "User authorization failed: invalid access_token"


class WBReaderError(Exception):
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return "Error while trying to read workbook file"


class WBWriterError(Exception):
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return "Error while trying to write workbook to a file"
