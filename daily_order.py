import glob
import json
import random

urls = set()
ban_words = ['爪', '舌']

dish_list = []


def is_baned(ingredient_list):
    for ingredient in ingredient_list:
        for word in ban_words:
            if word in ingredient:
                return True
    return False


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


for i in range(10):
    print(dish_list[random.randint(1, len(dish_list))])
