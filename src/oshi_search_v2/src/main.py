#-*- coding:utf-8 -*-

import os
import json
import logging
import argparse
import random

from env.app_parameters import AppParameters
from classes.oshi_search import OshiSearch
from classes.parse_condition import parse_json_file
from classes.gacha import is_ssr
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def get_args():
    parser = argparse.ArgumentParser(description='Oshi search')

    parser.add_argument(
        "--isH",
        help="Active H mode",
        default=False,
        action='store_true'
    )

    return parser.parse_args()

def main():
    args = get_args()

    app_parameters = AppParameters()

    logger = logging.getLogger(name="oshi_search")
    logger.setLevel(logging.INFO)

    logger.info("start : oshi_search")

    oshi_search = OshiSearch(
        api_key=app_parameters.api_key,
        custom_search_engine=app_parameters.custom_search_engine,
        webhook=app_parameters.discord_webhook,
        search_max_index=app_parameters.search_max_index,
        isH= args.isH and is_ssr(),
        logger=logger
    )

    with open(os.path.join(os.path.dirname(__file__), app_parameters.file_name),encoding='utf-8') as f:
        file = json.load(f)
        oshi_search.execute(parse_json_file(file))

    logger.info("finished : oshi_search")
    
@app.route("/")
def index():
    return 'Index Page'

#  ランダムで返すAPI
@app.route("/api/image/random", methods=['GET'])
def get_image_random():
    images_path = "./image"
    images = []
    for i in range(10):
        images.append(random.choice(os.listdir(images_path)))
    json_str = json.dumps(images, ensure_ascii=False)
    return json_str

# 画像名がドメインに入力されてる場合、画像を返すAPI
@app.route('/image', methods=['GET'])
# /image?img=画像名 で画像を表示
def get_image_file():
    images_path = "./image"
    img = request.args.get('img')
    fpath = images_path + "/" + img
    return send_file(fpath)

# 画像すべてをjson形式で返すAPI　!!!パスとして返していた
@app.route('/test', methods=['GET'])
def test_image() :
    images_path = "./image"
    # iamge = os.listdir(images_path)
    json_str = json.dumps(os.listdir(images_path), ensure_ascii=False)
    fpath = images_path + "/" + json_str
    # return send_file(fpath)
    return fpath

# 画像すべてをjson形式で返すAPI
@app.route('/prefix', methods=['GET'])
def test_prefix() :
    images_path = "./image"
    images = []
    prefix = request.args.get('prefix')
    if not prefix:
        for img in os.listdir(images_path):
            images.append(img)
    else:
        for img in os.listdir(images_path):
            if img.startswith(prefix):
                images.append(img)

    json_str = json.dumps(images, ensure_ascii=False)
    return json_str


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5173')


# main()
# サーバ落とすたびに実行されるので一回停止