from PIL import ImageDraw, Image
import numpy as np
import hashlib
import random


# array_list = [1]
background_color = '#F2F1F2'
colors = ['#CD00CD', 'Red', 'Orange', "#66FF00", "#2A52BE"]


def generate_array(bytes):

    ## Generate array

    for i in range(100):

        # Array 6 * 12
        need_array = np.array([bit == '1' for byte in bytes[3:3 + 9] for bit in bin(byte)[2:].zfill(8)]).reshape(6, 12)

        # Get full array 12 * 12
        need_array = np.concatenate((need_array, need_array[::-1]), axis=0)

        for i in range(12):
            need_array[0, i] = 0
            need_array[11, i] = 0
            need_array[i, 0] = 0
            need_array[i, 11] = 0

        return need_array


def generate_pyxies(pyxie_size: int, s: str) -> None:
    bytes = hashlib.md5(s.encode('utf-8')).digest()

    need_color = generate_array(bytes)

    ## Draw image

    img_size = (pyxie_size, pyxie_size)
    block_size = pyxie_size // 12  # Size

    img = Image.new('RGB', img_size, background_color)
    draw = ImageDraw.Draw(img)

    for x in range(pyxie_size):
        for y in range(pyxie_size):
            need_to_paint = need_color[x // block_size, y // block_size]
            if need_to_paint:
                draw.point((x, y), random.choice(colors))
    format = 'jpeg'
    path = f'CryptoPyxie_{s}.{format}'
    img.save(path, format)


if __name__ == "__main__":

    # argv[1] - size of pictures (pixels)
    # argv[2] - int - hash generate

    from sys import argv

    cryptopyxie_size = int(argv[1])
    cryptopyxie_name = argv[2]
    cycle = generate_pyxies(int(cryptopyxie_size // 12 * 12), cryptopyxie_name)