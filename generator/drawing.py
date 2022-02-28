from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def colour(src: str | Image.Image, color: tuple) -> Image.Image:
    if isinstance(src, str):
        img = Image.open(src)
    else:
        img = src

    pixels = np.asarray(img, dtype=np.uint8)

    mask = pixels[:,:,3] > 0
    r, g, b = color
    pixels[mask, :3] = [r, g, b]
    return Image.fromarray(np.uint8(pixels)).convert("RGBA")


def generate_colours_objects_png(path_base_pic: str, out_dir: str, colors_rgb: list[tuple]) -> None:
    out_dir.rstrip("/")
    base_img = Image.open(path_base_pic)
    pixels = np.asarray(base_img, dtype=np.uint8)
    assert pixels.shape[-1] > 3, "This is not .png file..."
    mask = pixels[:,:,3] > 0
    for r, g, b in colors_rgb:
        pixels[mask, :3] = [r, g, b]
        plt.imsave(f"{out_dir}/{r}_{g}_{b}.png", pixels)


if __name__ == "__main__":
    generate_colours_objects_png("../images/test_forNp.png", "../testNp", [(255, 0, 0),
                                                                         (0, 255, 0),
                                                                         (0, 0, 255),
                                                                         (127, 127, 127),
                                                                         (255, 254, 255)])
