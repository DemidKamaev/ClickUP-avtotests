from api_clients.task_api import ClickUpClient
from utils.helpers import CLICKUP_API_KEY

BASE_URL = 'https://api.clickup.com'
client = ClickUpClient(BASE_URL, CLICKUP_API_KEY)
FOLDER_ID = ''
WORKSPACE_ID = client.get_list_id


