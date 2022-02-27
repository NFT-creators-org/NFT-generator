from PIL import Image
import os
from random import shuffle, randint


def merge(src1, src2, offset=(0, 0)) -> Image:
    if isinstance(src1, str):
        img1 = Image.open(src1)
    else:
        img1 = src1
    if isinstance(src2, str):
        img2 = Image.open(src2)
    else:
        img2 = src2

    img1.paste(img2, offset, img2)
    return img1


def create_empty_layer(src: str, size: tuple):
    img = Image.new(mode="RGBA", size=size, color=(255, 255, 255, 255))
    img.save(src)


def pre_merge(src1, src2: str, new_path="new_image.png"):
    img2 = Image.open(src2)
    if not src1:
        img1 = Image.new(mode="RGBA", size=img2.size, color=(255, 255, 255, 255))
    else:
        img1 = Image.open(src1)
    img1 = merge(img1, img2)
    img1.save(src1 if src1 else new_path)


def build_all(path: str, path_accessories: str, out_path: str, priorities: dict, count=10):
    # priorities = {
    #     1: "body",
    #     2: "paunch",
    #     3: "head",
    #     4: "legs"
    # }
    path.rstrip("/")

    accessories = list(os.listdir(path_accessories))

    parts = dict()
    keys = list(priorities.keys())
    keys.sort()

    for key in keys:
        mode = priorities[key]

        curr_path = f"{path}/{mode}"
        parts[mode] = os.listdir(curr_path)
        shuffle(parts[mode])

    for i in range(count):
        img_back = Image.open(f"{path}/{priorities[keys[0]]}/{parts[priorities[keys[0]]][i]}")
        for front_i in range(1, len(keys)):
            mode = priorities[keys[front_i]]
            # img_front = Image.open(f"{path + mode}/{parts[mode][i]}")
            img_back = merge(img_back, f"{path}/{mode}/{parts[mode][i]}")

        count_accessories = randint(0, len(accessories) - 1)
        if count_accessories > 0:
            shuffle(accessories)

        for j in range(count_accessories):
            pics = list(os.listdir(f"{path}/accessories/{accessories[j]}"))
            pic = pics[randint(0, len(pics) - 1)]
            # pix_access = Image.open(f"{path}accessories/{accessories[j]}/{pic}").load()
            merge(img_back, f"{path}/accessories/{accessories[j]}/{pic}")

        img_back.save(f"{out_path.rstrip('/')}/{i}.png")


if __name__ == "__main__":
    # merge_frogs("../images", "../images/NFT_result", 10)
    a = merge("../images/accessories/eyepatch/eyepatch_wired.png", "../images/accessories/pricetag/pricetag.png")
    a.save("tres.png")