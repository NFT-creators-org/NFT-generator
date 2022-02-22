from PIL import Image, ImageDraw


def createSomeImages(directory: str, log=False, step=50, from_colour=0, to_colour=255):
    path = f"{directory}/basa.jpg"
    new_img = directory + "/"
    img = Image.open(path)
    pixels = img.load()
    img.close()
    for new_r in range(from_colour, to_colour, step):
        for new_g in range(from_colour, to_colour, step):
            for new_b in range(from_colour, to_colour, step):
                img = Image.open(path)
                height_img, width_img = img.size
                idraw = ImageDraw.Draw(img)
                for h in range(height_img):
                    for w in range(width_img):
                        pixel = pixels[h, w]
                        r, g, b = pixel
                        if (r < 180 and g < 180 and b < 180):  # if now it's black
                            idraw.point((h, w), fill=(new_r, new_g, new_b))  # draw new colour
                            continue
                        if (r != 255 and g != 255 and b != 255):  # can have error
                            idraw.point((h, w), fill=(255, 255, 255))
                name = new_img + f"{directory}_" + str(new_r) + "_" + str(new_g) + "_" + str(new_b) + ".png"  # new name
                if log:
                    print(name)
                img.save(name)
