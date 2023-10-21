import requests

from apiclient.discovery import build


class GoogleImage:
    def __init__(self, api_key, custom_search_engine, logger):
        self.custom_search_engine = custom_search_engine
        self.service = build("customsearch", "v1", developerKey=api_key, cache_discovery=False)
        self.logger = logger

    def __request(self, keyword, start_index):
        try:
            return self.service.cse().list(
                q=keyword,     # Search words
                cx=self.custom_search_engine,        # custom search engine key
                lr='lang_ja',      # Search language
                num=10,            # Number of images obtained by one request (Max 10)
                start=start_index,
                searchType='image' # search for images
            ).execute()

        except Exception as e:
            self.logger.error(e)


    def get_link_list(self, keyword, start_index):
        response = self.__request(keyword, start_index)

        if len(response['items']) > 0:
            return [response['items'][i]['link'] for i in range(len(response['items']))]

        self.logger.info("Google search result : Not found")


    def get_image(self, link):
        return requests.get(link).content
