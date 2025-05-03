from api_clients.task_api import ClickUpClient
from utils.helpers import CLICKUP_API_KEY
from tests.constants import BASE_URL


client = ClickUpClient(BASE_URL, CLICKUP_API_KEY)
WORKSPACE_ID = client.get_list_id()
id_task = "86c39m3u"
BOARD_ID = "2kypr5wz-255"
TEAM_ID = "90151065503"
FOLDER_ID = '901510167328'
CARD_ID = "c17472219"
TEXT_MY_TITLE = "Clickup-тесты"
TEXT_CARD = "Test_card"
