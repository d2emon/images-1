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


def main(input_file, output_file, grade):
    print("Loading image from {}...".format(input_file))
    image = Image.open(input_file).convert('L')
    # image.show()

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

        # Оценить размах сигнала, его математическое ожидание и СКО.
        Δu = data.max() - data.min()
        mᵤ = mean(data)
        σᵤ = std(data)

        # Вычислить теоретическое значение σQ, руководствуясь уравнением (11) для оптимального квантователя.
        L = math.log2(grade)
        Δf = (2 ** 8) / (2 ** L)
        σQ = math.sqrt((Δf ** 2) / 12)

        # Оценить отношение С/Ш для оптимального квантования в соответствии с уравнением (12).
        signal_to_noise = 20 * math.log10(Δu / σQ)
        # K_sq =
        """
        c) Оценить отношение С/Ш для оптимального квантования в соответствии с уравнением (12), учитывая реальный
            размах сигнала
                                                  , дБ.                                               (14)
        d) Оценить СКО шума квантования как СКО сигнала разности изображений квантованного и исходного .
        e) Оценить относительное СКО в соответствии с формулой:
                                                    .                                                       (15)
        f) Определить отношение СКО сигнала к СКО шума квантования по формуле:
            ,                                                 (16)
            где .
        g) Оценить отношение сигнал/шум для квантованных изображений в соответствии с формулой (14).
        h) На основании эксперимента построить графики зависимости отношения сигнал/шум и относительного СКО от числа 
            уровней квантования и сравнить их с теоретическими оценками.
        """

        print("Δu = {}".format(Δu))
        print("mᵤ = {}".format(mᵤ))
        print("σᵤ = {}".format(σᵤ))

        print("Δf = {}".format(Δf))
        print("σQ = {}".format(σQ))

        print("С/Ш = {}".format(signal_to_noise))
        # print("K sq = {}".format(K_sq))

        quantized.show(grade)

    print(input_file, output_file)
    """
    3. Наложить на исходное изображение реализацию нормального шума (0,) [3].
    4. Выполнить пункт 2 для этого изображения.
    5. Выполнить квантование исходного изображения и изображения с шумом на 8 уровней. Оценить, как влияет шум на 
        формирование ложных контуров на изображении.
    6. Выполнить эквализацию гистограмм изображений. Выполнить квантование исходного и нелинейно преобразованного 
        изображения на 8 уровней. Сравнить полученные изображения.
    """


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("images-1.py <inputfile> <outputfile> <grade>")
        sys.exit(0)

    try:
        grade = int(sys.argv[3])
        # [None, 8, 16, 32, 64, 128]
    except (IndexError, ValueError):
        grade = None

    main(*sys.argv[1:3], grade)
