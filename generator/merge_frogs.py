from PIL import Image
import os
from random import shuffle, randint


'''
@author Maxim Trofimov (@trofik00777)
'''


def merge(pix1, pix2, size, ignore_color=(255, 255, 255)):
    IGNORE_COLOR = ignore_color

    w, h = size
    for x in range(w):
        for y in range(h):
            pixs = pix2[x, y]
            if (len(pixs) == 3 and pixs != IGNORE_COLOR) or (len(pixs) == 4 and pixs[-1] > 0):
                pix1[x, y] = pix2[x, y]


def merge_frogs(path: str, out_path: str, count=10):
    PRIORITIES = {
        1: "body",
        2: "paunch",
        3: "head",
        4: "legs"
    }

    if not path.endswith("/"):
        path += "/"

    ACCESSORIES = list(os.listdir(f"{path}accessories"))

    parts = dict()
    keys = list(PRIORITIES.keys())
    keys.sort()

    for key in keys:
        mode = PRIORITIES[key]

        curr_path = path + mode
        parts[mode] = os.listdir(curr_path)
        shuffle(parts[mode])

    for i in range(count):
        img_back = Image.open(f"{path + PRIORITIES[keys[0]]}/{parts[PRIORITIES[keys[0]]][i]}")
        pix_back = img_back.load()
        for front_i in range(1, len(keys)):
            mode = PRIORITIES[keys[front_i]]
            img_front = Image.open(f"{path + mode}/{parts[mode][i]}")
            pix_front = img_front.load()
            merge(pix_back, pix_front, img_back.size)

        count_accessories = randint(0, len(ACCESSORIES) - 1)
        if count_accessories > 0:
            shuffle(ACCESSORIES)

        for j in range(count_accessories):
            pics = list(os.listdir(f"{path}accessories/{ACCESSORIES[j]}"))
            pic = pics[randint(0, len(pics) - 1)]
            pix_access = Image.open(f"{path}accessories/{ACCESSORIES[j]}/{pic}").load()
            merge(pix_back, pix_access, img_back.size)

        img_back.save(f"{out_path.rstrip('/')}/{i}.png")


if __name__ == "__main__":
    merge_frogs("../images", "../images/NFT_result", 10)
