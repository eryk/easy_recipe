# -*- coding: UTF-8 -*-
import os
from flask import Flask, render_template

import glob
import json
import random

urls = set()
ban_words = ['爪', '舌']

dish_list = []


def is_baned(ingredient_list):
    for ingredient in ingredient_list:
        for word in ban_words:
            if word in ingredient.encode('utf8'):
                return True
    return False


def download_img(img_url, download_path):
    import requests
    r = requests.get(img_url)
    with open(download_path, 'wb') as f:
        f.write(r.content)


def path_name_ext(path):
    (dir_path, tempfilename) = os.path.split(path)
    (file_name, extension) = os.path.splitext(tempfilename)
    return dir_path, file_name, extension


def exists(path):
    return os.path.exists(path)


for file in glob.glob('recipe/*.json')[:]:
    with open(file, 'rb') as f:
        dish_map = json.load(f)
        for dish in dish_map:
            if dish['url'] in urls:
                continue
            if is_baned(dish['ingredient']):
                continue
            urls.add(dish['url'])
            dish_list.append(dish)

app = Flask(__name__)


@app.route('/')
def daily_order():
    selected = []
    for i in range(7):
        dish = dish_list[random.randint(1, len(dish_list))]
        if '?' in dish['pic']:
            dish['pic'] = dish['pic'].split('?')[0]
        if '@' in dish['pic']:
            dish['pic'] = dish['pic'].split('@')[0]
        path, name, ext = path_name_ext(dish['pic'])
        pic_path = './static/' + name + ext
        if not exists(pic_path):
            download_img(dish['pic'], pic_path)
        dish['pic'] = pic_path
        dish['ingredient'] = ','.join(dish['ingredient'])
        selected.append(dish)
    return render_template('home.html', dish_list=selected)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=False
    )
