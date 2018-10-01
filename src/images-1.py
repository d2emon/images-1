import sys
import math
from PIL import Image
from numpy import asarray, mean, std


def quantize(image, grade):
    color_delta = int(256 / grade)

    return image.point(lambda c: int(c / color_delta) * color_delta)


def calculations(image, title, grade):
    image = image.convert('L')
    data = asarray(image)

    du = data.max() - data.min()
    l = math.log2(grade)
    df = (2 ** 8) / (2 ** l)
    disperse = math.sqrt((df ** 2) / 12)
    sh = 20 * math.log10(du / disperse)

    print('-' * 80)
    print(title)
    print("min = {}\tmax = {}".format(data.min(), data.max()))
    print("delta = {}".format(du))
    print("mean = {}".format(mean(data)))
    print("std = {}".format(std(data)))
    print("df = {}".format(df))
    print("disperse = {}".format(disperse))
    print("s/sh = {}".format(sh))


def main(input_file, output_file):
    print("Loading image from {}...".format(input_file))
    image = Image.open(input_file).convert('L')
    image.show()
    calculations(image, 'original', 256)

    # for grade in [8, 16, 32, 64, 128]:
    for grade in [8,]:
        quantified = quantize(image, grade)
        calculations(quantified, grade, grade)
        quantified.show(grade)

        quantified = image.quantize(grade)
        calculations(quantified, grade, grade)
        quantified.show(grade)

    print(input_file, output_file)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("images-1.py <inputfile> <outputfile>")
        sys.exit(0)
    input_file, output_file = sys.argv[1:3]
    main(input_file, output_file)
