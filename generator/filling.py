from PIL import Image
from random import randint


'''
@author Maxim Trofimov (@trofik00777)
'''


def fill(pixels, x: int, y: int, color: tuple, w: int, h: int) -> None:
    if x < 0 or x >= w or y < 0 or y >= h:
        return
    r, g, b, alf = pixels[x, y]
    if alf > 0:
        return
    stack = [(x, y)]
    while len(stack) > 0:
        curr_x, curr_y = stack.pop()
        alf = pixels[curr_x, curr_y][-1]
        while alf == 0 and curr_x >= 0:
            curr_x -= 1
            alf = pixels[curr_x, curr_y][-1]
        curr_x += 1
        alf = pixels[curr_x, curr_y][-1]
        is_top = is_bottom = False
        while alf == 0 and curr_x < w:
            pixels[curr_x, curr_y] = color

            if curr_y > 0:
                curr_alf = pixels[curr_x, curr_y - 1][-1]
                if is_top and curr_alf != 0:
                    is_top = False
                elif not is_top and curr_alf == 0:
                    is_top = True
                    stack.append((curr_x, curr_y - 1))
            if curr_y + 1 < h:
                curr_alf = pixels[curr_x, curr_y + 1][-1]
                if is_bottom and curr_alf != 0:
                    is_bottom = False
                elif not is_bottom and curr_alf == 0:
                    is_bottom = True
                    stack.append((curr_x, curr_y + 1))

            curr_x += 1
            alf = pixels[curr_x, curr_y][-1]


def make_fill(path: str, name_standart_pic: str, anchors: list[tuple], step=50) -> None:
    for i in range(step):
        img = Image.open(f"{path}/{name_standart_pic}")
        pixels = img.load()
        w, h = img.size
        for anchor in anchors:
            fill(pixels=pixels, x=anchor[0], y=anchor[1],
                 color=(randint(0, 255), randint(0, 255), randint(0, 255), 255), w=w, h=h)

        img.save(f"{path}/{i}.png")


def find_anchors(path: str) -> list[tuple]:
    """Try to find anchor points. If program don't work correct use your anchor points"""
    img = Image.open(path)
    pixels = img.load()
    assert len(pixels[0, 0]) == 4, "This is not .png file with alfa canal"
    w, h = img.size
    anchors = []
    for y in range(h):
        is_l = is_m = False
        l = -1
        for x in range(w):
            if pixels[x, y][-1] > 0:
                if not is_l and not is_m:
                    is_l = True
                    l = x
                    continue
                if is_l:
                    l = x
                    continue
                if is_m:
                    is_m = False
                    anchors.append(((x + l) // 2, y))
                    is_l = True
                    l = x
            else:
                if is_l:
                    is_l = False
                    is_m = True
                    continue

    answ_anchs = []
    for x, y in anchors:
        for y1 in range(y):
            if pixels[x, y1][-1] > 0:
                break
        else:
            continue

        for y2 in range(y, h):
            if pixels[x, y2][-1] > 0:
                break
        else:
            continue
        answ_anchs.append((x, y))

    return answ_anchs


if __name__ == "__main__":
    # make_fill(path="./images/accessories/watch", name_standart_pic="watch_circle.png", anchors=[(655, 720), (635, 735), (676, 725)])
    # make_fill(path="./images/accessories/eyepatch", name_standart_pic="eyepatch_wired.png", anchors=[(410, 300), (490, 280), (365, 325)])
    make_fill(path="./images/accessories/e", name_standart_pic="eyepatch_wired.png",
              anchors=find_anchors("./images/accessories/e/eyepatch_wired.png"))
    # print(find_anchors("./images/accessories/eyepatch/eyepatch_wired.png"))

