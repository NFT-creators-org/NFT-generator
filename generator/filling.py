from PIL import Image
from random import randint
from merging import merge
from drawing import colour


def fill(pixels, x: int, y: int, color: tuple, w: int, h: int, mask=None) -> None:
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
            if mask is None:
                pixels[curr_x, curr_y] = color
            else:
                mask[curr_x, curr_y] = color

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


def make_fill(path_out: str, path_standart_pic: str, anchors: list[list[tuple]], count=50, colors=None) -> None:
    masks = [create_mask(path_standart_pic, anch) for anch in anchors]
    for i in range(count):
        img = Image.open(path_standart_pic)
        if colors:
            r, g, b = colors[randint(0, len(colors) - 1)]
        else:
            r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)

        for mask in masks:
            img = merge(img, colour(mask, (r, g, b)))
        # for anchor in anchors:
        #     fill(pixels=pixels, x=anchor[0], y=anchor[1],
        #          color=(randint(0, 255), randint(0, 255), randint(0, 255), 255), w=w, h=h)

        img.save(f"{path_out}/{i}.png")


def create_mask(src, list_anchors_for_once_color: list[tuple]) -> Image:
    if isinstance(src, str):
        img = Image.open(src)
    else:
        img = src

    mask = Image.new("RGBA", img.size, (0, 0, 0, 0))
    img_pix = img.load()
    mask_pix = mask.load()
    for x, y in list_anchors_for_once_color:
        fill(pixels=img_pix, x=x, y=y, color=(255, 255, 255, 255), w=img.size[0], h=img.size[1], mask=mask_pix)

    return mask


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

