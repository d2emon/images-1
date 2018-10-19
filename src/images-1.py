import sys
import math
from PIL import Image
from numpy import asarray, mean, std


def quantize(image, grade=None):
    if grade is None:
        return image

    color_delta = int(256 / grade)
    print(grade, color_delta, int(color_delta / 2))

    return image.point(lambda c: int(c / color_delta) * color_delta + int(color_delta / 2))


def main(input_file, output_file):
    print("Loading image from {}...".format(input_file))
    image = Image.open(input_file).convert('L')
    # image.show()

    for grade in [None, 8, 16, 32, 64, 128]:
        if grade is None:
            images = image,
        else:
            images = image.quantize(grade), quantize(image, grade)

        print('=' * 80)
        print("quantize grade = {}".format(grade or "original"))
        for id, quantized in enumerate(images):
            quantized = quantized.convert('L')
            data = asarray(quantized)

            print('-' * 20)
            if id == 0:
                print("PIL quantizer")
            else:
                print("My quantizer")

            print("min = {}".format(data.min()))
            print("max = {}".format(data.max()))
            if grade is None:
                print("original")
                continue

            du = data.max() - data.min()
            L = math.log2(grade)
            df = (2 ** 8) / (2 ** L)
            disperse = math.sqrt((df ** 2) / 12)
            sh = 20 * math.log10(du / disperse)
            # K_sq =

            print("delta u = {}".format(du))
            print("mean = {}".format(mean(data)))
            print("std = {}".format(std(data)))
            print("df = {}".format(df))
            print("disperse = {}".format(disperse))
            print("s/sh = {}".format(sh))
            # print("K sq = {}".format(K_sq))

            quantized.show(grade)

    print(input_file, output_file)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("images-1.py <inputfile> <outputfile>")
        sys.exit(0)
    main(*sys.argv[1:3])
