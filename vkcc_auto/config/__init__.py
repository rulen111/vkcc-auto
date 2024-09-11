class DefaultConfig(object):
    # VK API access token, can be of any type (user, service, community)
    TOKEN = "1234"
    # The amount of time to wait before sending next request to VK API
    API_RPS_RATE = 6

    # Index of an excel workbook row to be considered first
    # to have relevant data (starts from 1, not 0)
    PAYLOAD_FIRST_ROW = 2
    # Index of an excel workbook column to be considered
    # as an input column (starts from 1, not 0)
    PAYLOAD_INPUT_COL = 1
    # Index of an excel workbook column to be considered
    # as an output column (starts from 1, not 0)
    PAYLOAD_TARGET_COL = 2
