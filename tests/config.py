from api_clients.task_api import ClickUpClient
from utils.helpers import CLICKUP_API_KEY


BASE_URL = 'https://api.clickup.com/api'
client = ClickUpClient(BASE_URL, CLICKUP_API_KEY)

TEAM_ID = client.get_team_id
SPACE_ID = client.get_space_id(TEAM_ID)
FOLDER_ID = client.get_folder_id(SPACE_ID)
LIST_ID = client.get_list_id(FOLDER_ID)
CARD_ID = "c17472219"
TEXT_MY_TITLE = "Clickup-тесты"
TEXT_CARD = "Test_card"
task_id_invalid = "86c39m3u"
BOARD_ID = "2kypr5wz-255"
