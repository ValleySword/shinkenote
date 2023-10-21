import os
from dotenv import load_dotenv

class AppParameters:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)

        self.api_key = os.environ['API_KEY']
        self.custom_search_engine = os.environ['CUSTOM_SEARCH_ENGINE']
        self.discord_webhook = os.environ['DISCORD_WEBHOOK']
        self.search_max_index = int(os.environ['SEARCH_MAX_INDEX'])
        self.file_name = os.environ['FILE_NAME']
