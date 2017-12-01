import math
from PIL import Image
#import numpy as np
IMAGE_PATH = "./"  # Путь до картинки, с которой будем работать, пустой если находится в той же директоррии, что и программа.
IMAGE_NAME = "pic"  # Имя картинки.
IMAGE_TYPE = "jpg"  # Тип картинки, крайне рекомендуется jpg.


def quantum(pixel):
    r, g, b = pixel
    return round(r / 20) * 20, round(g / 20) * 20, round(b / 20) * 20

def convert_base(num, to_base=2, from_base=10):
    # first convert to decimal number
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    # now convert decimal to 'to_base' base
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base] # возращет строчку

#1
original_image = Image.open(IMAGE_PATH + IMAGE_NAME + "." + IMAGE_TYPE)  # Открываем изображение.
width = original_image.size[0]  # Определяем ширину.
height = original_image.size[1]  # Определяем высоту.
pixels = original_image.load()
channels = 2

#2
for i in range(width):
    for j in range(height):
        pixels[i, j] = quantum(pixels[i, j])

#3
alphabet = []
probability = []
sum = 0

for i in range(256):
    alphabet.append(0)
    probability.append(0)

for i in range(width):
    for j in range(height):
        r, g, b = pixels[i, j]
        alphabet[r] += 1
        #alphabet[g] += 1
        #alphabet[b] += 1
#print(alphabet)

for i in range(256):
    sum += alphabet[i]

for i in range(0, 256, 20):
    probability[i] = alphabet[i] / sum
    #print(probability[i])
#4

entropy = 0

for i in range(0, 256, 20):
    entropy -= probability[i] * math.log(probability[i], 2)
#print(entropy)
#5
binCode = [[0] * 128 for i in range(128)]

for i in range(width):
    for j in range(height):
        r, g, b = pixels[i, j]
        binNum = convert_base(r / 20)
        binCode[i][j] = (('0' * (4 - int(len(binNum)))) + binNum)
        #print (binCode[i][j])
#6
#for i in range(0, 256, 20):
 #   print(alphabet[i])
fanoCode = [[0] * 128 for i in range(128)]

for i in range(width):
    for j in range(height):
        r, g, b = pixels[i, j]
        if r == 0: #A
            fanoCode[i][j] = '1001'
        elif r == 20: #B
            fanoCode[i][j] = '010'
        elif r == 40: #C
            fanoCode[i][j] = '1000'
        elif r == 60: #D
            fanoCode[i][j] = '1100'
        elif r == 80: #E
            fanoCode[i][j] = '001'
        elif r == 100: #F
            fanoCode[i][j] = '1101'
        elif r == 120: #G
            fanoCode[i][j] = '1110'
        elif r == 140: #H
            fanoCode[i][j] = '11111'
        elif r == 160: #I
            fanoCode[i][j] = '11110'
        elif r == 180: #J
            fanoCode[i][j] = '1010'
        elif r == 200: #K
            fanoCode[i][j] = '1011'
        elif r == 220: #L
            fanoCode[i][j] = '011'
        elif r == 240: #M
            fanoCode[i][j] = '000'
#print(fanoCode)

#7
haffCode = [[0] * 128 for i in range(128)]

for i in range(width):
    for j in range(height):
        r, g, b = pixels[i, j]
        if r == 0: #A
            haffCode[i][j] = '1001'
        elif r == 20: #B
            haffCode[i][j] = '010'
        elif r == 40: #C
            haffCode[i][j] = '1100'
        elif r == 60: #D
            haffCode[i][j] = '0110'
        elif r == 80: #E
            haffCode[i][j] = '100'
        elif r == 100: #F
            haffCode[i][j] = '0011'
        elif r == 120: #G
            haffCode[i][j] = '0010'
        elif r == 140: #H
            haffCode[i][j] = '11010'
        elif r == 160: #I
            haffCode[i][j] = '11011'
        elif r == 180: #J
            haffCode[i][j] = '1010'
        elif r == 200: #K
            haffCode[i][j] = '0111'
        elif r == 220: #L
            haffCode[i][j] = '000'
        elif r == 240: #M
            haffCode[i][j] = '111'
#print(haffCode)

#8
eqMidLen = 4
fanoMidLen = (2696 *3 + 2134 * 3 + 1688 * 3 + 1460 * 3 + 1226 * 4 + 1121 * 4 + 1031 * 4 + 980 * 4 + 971 * 4 + 769 * 4 + 748 * 4 + 691 * 5 + 561 * 5) / 16384
haffMidLen = (2696 *3 + 2134 * 3 + 1688 * 3 + 1460 * 3 + 1226 * 4 + 1121 * 4 + 1031 * 4 + 980 * 4 + 971 * 4 + 769 * 4 + 748 * 4 + 691 * 5 + 561 * 5) / 16384
#print(eqMidLen)
#print(fanoMidLen)
#print(haffMidLen)

#9
# определяю размер после квантования
origSize = 4 * 128 * 128
fanoSize = fanoMidLen * 128 * 128
haffSize = haffMidLen * 128 * 128
fanoCompress = (origSize - fanoSize) / origSize * 100
haffCompres = (origSize - haffSize) / origSize * 100
#print(fanoCompress)
#print(haffCompres)

#10
# Избыточность
fanoEff = 1 - (entropy / fanoMidLen)
haffEff = 1 - (entropy / haffMidLen)
#print(fanoEff)
#print(haffEff)

