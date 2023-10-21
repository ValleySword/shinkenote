import random

# from .discord_sender import DiscordSender
from .google_image import GoogleImage
from .interfaces.oshi_search_condition import OshiSearchCondition

import requests
import json


class OshiSearch:
    def __init__(
        self,
        api_key,
        custom_search_engine,
        webhook,
        search_max_index,
        logger,
        *,
        isH
    ):
        # self.discord_sender = DiscordSender(webhook, logger)
        self.google_image = GoogleImage(api_key, custom_search_engine, logger)
        self.search_max_index = search_max_index
        self.logger = logger
        self.isH = isH

    def decide_condition(self, search_conditions):
        return random.choice(search_conditions)

    def execute(self, search_conditions):
        target:OshiSearchCondition = self.decide_condition(search_conditions)

        start_index:int = random.randint(1, self.search_max_index)

        # キーワードがまったく同じであっても結果がまったく同じになるというわけではない
        keyword = random.choice(target.keywords)

        link_list = self.google_image.get_link_list(
            f"{keyword}" if self.isH else keyword,
            start_index
        )
        # 画像を一枚に絞るための処理
        # link = random.choice(link_list)
        # image = self.google_image.get_image(link)

        if link_list:
            text = f"{target.name} : {target.success}"
            for i in link_list:
                with open('count.json', 'r') as file:
                    count = json.load(file)
                    count['count'] += 1
                with open('count.json', 'w') as f:
                    json.dump(count, f)
                    print(count['count']) 
                with open(f"./image/{keyword}{count['count']}.jpg", 'wb') as file:
                    file.write(self.google_image.get_image(i))
            print(text)
        else:
            text = f"{target.name} : {target.error}"
            print(text)

