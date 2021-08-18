import cv2
import os
import numpy as np
import crc16



def find_lcsubstr(s1, s2):
    m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]
    mmax = 0
    p = 0
    q = 0
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
                    p = i + 1
                    q = i - j
    print(p , q, mmax)
    return s1[p - mmax:p], p - mmax, mmax, q, p

def cut_a_shotcut(img, headimg, tailimg, height, cutFlag=True):
    shotcut = []
    if cutFlag:
        shotcut.extend(headimg)
    if len(img) > height:
        shotcut.extend(img[:height])
    else:
        shotcut.extend(img[:])
    if cutFlag:
        shotcut.extend(tailimg)
    return shotcut

dir = r'C:\Users\Gavin\Desktop\20210805微信聊天记录导出备份\聊天记录分析_pyhton\screen'
headdir = dir + r'\part\head.png'
taildir = dir + r'\part\tail.png'
image_list = [f if f.endswith('png') else None for f in os.listdir(dir)]
image_list.pop(image_list.index(None))
image_list.sort(key=lambda x: int(x[:-4]))
print(image_list)
dict = {}
all_crc16_list = []
for image in image_list:
    print(image)
    img = cv2.imdecode(np.fromfile(os.path.join(dir, image), dtype=np.uint8), -1)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    crc16_list = []
    for l in gray:
        crc16_list.append(crc16.crc16xmodem(l))
    dict[image] = crc16_list
    all_crc16_list.append(crc16_list)

final_img = []
first_img = cv2.imdecode(np.fromfile(os.path.join(dir, image_list[0]), dtype=np.uint8), -1)
headimg = cv2.imdecode(np.fromfile(headdir, dtype=np.uint8), -1)
tailimg = cv2.imdecode(np.fromfile(taildir, dtype=np.uint8), -1)
height = 1967
# height = 4000
savedir = dir+'\\part\\'
filename = 0
# cutFlag = False
cutFlag = True

final_img.extend(first_img)
for i in range(len(all_crc16_list)):
    crc16_list_1 = all_crc16_list[i]
    if i + 2 > len(all_crc16_list):
        break
    else:
        crc16_list_2 = all_crc16_list[i + 1]
        longest_common_substring, img1_cut_length, length, q, p = find_lcsubstr(crc16_list_1, crc16_list_2)
        print(longest_common_substring, img1_cut_length, length)
        if length == 0:
            continue
        img1 = cv2.imdecode(np.fromfile(os.path.join(dir, image_list[i]), dtype=np.uint8), -1)
        # new_image_1 = img1[:img1_cut_length, :, :]
        new_image_1 = img1[:p, :, :]
        tmp = len(final_img)
        final_img = final_img[:int(tmp-(img1.shape[0]-p))]
        # final_img.extend(new_image_1)
        img2 = cv2.imdecode(np.fromfile(os.path.join(dir, image_list[i + 1]), dtype=np.uint8), -1)
        idx = crc16_list_2.index(longest_common_substring[0])
        # new_image_2 = img2[crc16_list_2.index(longest_common_substring[0]) + length + q:, :, :]
        new_image_2 = img2[length + (p - q - length):, :, :]
        final_img.extend(new_image_2)

        # 切割存图
        if len(final_img) > 3 * height:
            filename = filename + 1
            part = cut_a_shotcut(final_img, headimg, tailimg, height, cutFlag)
            final_img = final_img[height:]
            cv2.imencode('.png', np.array(part))[1].tofile(savedir + str(filename) + '.png')
while True:
    filename = filename + 1
    part = cut_a_shotcut(final_img, headimg, tailimg, height, cutFlag)
    if len(final_img) > height:
        final_img = final_img[height:]
    else:
        cv2.imencode('.png', np.array(part))[1].tofile(savedir + str(filename) + '.png')
        break
    cv2.imencode('.png', np.array(part))[1].tofile(savedir + str(filename) + '.png')
