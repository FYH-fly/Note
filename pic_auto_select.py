'''
Created on 2020-9-16

@author: fWX457893
'''
import os
import cv2
import time
import copy
import shutil
import logging
import numpy as np

# 均值哈希算法
def avg_hash(img_path):
#     将图片缩放为8*8的
    image = cv2.imread(img_path)
    wid = 20
    hei = 20
    image = cv2.resize(image, (wid, hei), interpolation=cv2.INTER_CUBIC)
    # 将图片转化为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # s为像素和初始灰度值，hash_str为哈希值初始值
    s = 0
    # 遍历像素累加和
    for i in range(wid):
        for j in range(hei):
            s = s + gray[i, j]
    # 计算像素平均值
    avg = s / (wid*hei)
    # 灰度大于平均值为1相反为0，得到图片的平均哈希值，此时得到的hash值为64位的01字符串
    ahash_str = ''
    for i in range(wid):
        for j in range(hei):
            if gray[i, j] > avg:
                ahash_str = ahash_str + '1'
            else:
                ahash_str = ahash_str + '0'
#     for i in range(0, 64, 4):
#         result += ''.join('%x' % int(ahash_str[i: i + 4], 2))
#     print("avg_hash:", ahash_str)
    return ahash_str

# phash
def phash1(path):
    # 加载并调整图片为32*32的灰度图片
    img = cv2.imread(path)
    img1 = cv2.resize(img, (32, 32), cv2.COLOR_RGB2GRAY)
    # 创建二维列表
    h, w = img.shape[:2]
    vis0 = np.zeros((h, w), np.float32)
    vis0[:h, :w] = img1
    # DCT二维变换
    # 离散余弦变换，得到dct系数矩阵
    img_dct = cv2.dct(cv2.dct(vis0))
    img_dct.resize(8,8)
    # 把list变成一维list
    img_list = np.array().flatten(img_dct.tolist())
    # 计算均值
    img_mean = cv2.mean(img_list)
    avg_list = ['0' if i<img_mean else '1' for i in img_list]
    return ''.join(['%x' % int(''.join(avg_list[x:x+4]),2) for x in range(0,64,4)])


def phash(path):
    # 感知哈希算法 perceptive hash algorithm
    # 缩放32*32
    img = cv2.imread(path)
    img = cv2.resize(img, (32, 32), interpolation=cv2.INTER_CUBIC)
 
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 将灰度图转为浮点型，再进行dct变换
    dct = cv2.dct(np.float32(gray))
    # opencv实现的掩码操作
    dct_roi = dct[0:20, 0:20]
    phash = ''
    avreage = np.mean(dct_roi)
#     print(avreage)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > avreage:
                phash = phash + '1'
            else:
                phash = phash + '0'
#     print('phash:', (phash))
    return phash


# 差异值哈希算法
def dhash(img_path):
    image = cv2.imread(img_path)
    # 将图片转化为8*8
    image = cv2.resize(image, (21, 20), interpolation=cv2.INTER_CUBIC)
    # 将图片转化为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    dhash_str = ''
    for i in range(20):
        for j in range(20):
            if gray[i, j] > gray[i, j + 1]:
                dhash_str = dhash_str + '1'
            else:
                dhash_str = dhash_str + '0'
#     result = ''
#     for i in range(0, 64, 4):
#         result += ''.join('%x' % int(dhash_str[i: i + 4], 2))
#     print("dhash:", dhash_str)
    return dhash_str

# 计算两个哈希值之间的差异
def cmp_hash(hash1, hash2):
    n = 0
    # hash长度不同返回-1,此时不能比较
    if len(hash1) != len(hash2):
        return -1
    # 如果hash长度相同遍历长度
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n + 1
    # print(len(hash1))
    return (len(hash1)-n)/len(hash1)


def judge_pics(path):
    pic1, pic2 = os.listdir(path)
    
    pic1 = os.path.join(path, pic1)
    pic2 = os.path.join(path, pic2)
    
    std = avg_hash(pic1)
    cmps = avg_hash(pic2)
    
    return cmp_hash(std, cmps)
    
def judge_pics_p(path):
    pic1, pic2 = os.listdir(path)
    
    pic1 = os.path.join(path, pic1)
    pic2 = os.path.join(path, pic2)
    
    std = phash(pic1)
    cmps = phash(pic2)
    
    return cmp_hash(std, cmps)
    
def judge_pics_d(path):
    pic1, pic2 = os.listdir(path)
    
    pic1 = os.path.join(path, pic1)
    pic2 = os.path.join(path, pic2)
    
    std = dhash(pic1)
    cmps = dhash(pic2)
    
    return cmp_hash(std, cmps)


def judge_pics_ops(path, func):
    pic1, pic2 = os.listdir(path)
    
    pic1 = os.path.join(path, pic1)
    pic2 = os.path.join(path, pic2)
    
    std = func(pic1)
    cmps = func(pic2)
    
    return cmp_hash(std, cmps)

class PicModule(object):
    def __init__(self):
        self.pic_path = ''
        self.pic_md5 = ''
        self.pic_md5_path = ''
        self.cmp_ratio = 0
        self.cmp_total = 0
        self.cmp_pass_count = 0
        self.del_flag = False
        self.cmp_pass = False
        self.cmp_same_pic_path = []
        self.similar_pic_list = []
        pass
    
    def __str__(self, *args, **kwargs):
        ss = 'pic_path = {}, pic_md5_path = {}, pic_md5 = {}, \n\t\t\tcmp_ratio = {}, cmp_total = {}, cmp_pass_count = {}, del_flag = {}, cmp_pass = {}, cmp_same_pic_path = {}'\
                .format(self.pic_path, self.pic_md5_path, self.pic_md5, self.cmp_ratio,\
                         self.cmp_total, self.cmp_pass_count, self.del_flag, self.cmp_pass, self.cmp_same_pic_path)
        return ss

def get_jpg_files(path, del_md5_flag=False):
    pics = []
    for file in os.listdir(path):
        if '.jpg' in file:
            pics.append(os.path.join(path, file))
        elif '.md5' in file:
            if del_md5_flag:
                os.remove(os.path.join(path, file))
            pass
        else:
            pass
    return pics

def filter_camera_img(hash_func=phash):
    
    
    pic_lists = get_jpg_files(img_path, del_md5_flag)
    logging.info('pic_lists = {}'.format(pic_lists))
    
    similar_pic_dir = os.path.dirname(pic_lists[0]) + '/like/' # new folder
    if not os.path.exists(similar_pic_dir):
        os.mkdir(similar_pic_dir)
        
    pic_modules = []
    for pic in pic_lists: # 初始化图片列表
        picture = PicModule()
        picture.pic_path = pic
        picture.pic_md5_path = pic.split('.jpg')[0] + '.md5'
        if not os.path.exists(picture.pic_md5_path): 
            picture.pic_md5 = hash_func(picture.pic_path)
            with open(picture.pic_md5_path, 'w') as fp:
                fp.write(picture.pic_md5)
            pic_modules.append(picture)
            logging.info('{} making md5 file.'.format(picture.pic_path))
        else:
            with open(picture.pic_md5_path, 'r') as fp:
                picture.pic_md5 = fp.read().strip()
                print(picture.pic_md5)
            pic_modules.append(picture)
            logging.info('{} md5 has exists, read from md5 file.'.format(picture.pic_path))
            
    logging.info("totals pic = {}".format(len(pic_modules)))
    
    for pic in pic_modules:
        std_pic = pic.pic_md5
        logging.info("pic_modules[{}] = {}".format(pic_modules.index(pic), pic.pic_path))
        
        
        # setp 20, A picture can be compared only for 20 times.
        length = pic_modules.index(pic) + 1 + 10
        
        if length > len(pic_modules):
            length = len(pic_modules)
            
        for index in range(pic_modules.index(pic)+1, length):
            cmp_pic = pic_modules[index].pic_md5
            ratio = cmp_hash(std_pic, cmp_pic)
            pic.cmp_total += 1
            if ratio > 0.9:
                pic.cmp_pass_count += 1
                pic.del_flag = True
                pic.cmp_ratio = ratio
                pic.cmp_same_pic_path.append(pic_modules[index].pic_path)
                pic_modules[index].cmp_pass_count += 1 
                pic_modules[index].cmp_total += 1
                pic_modules[index].cmp_ratio = ratio
                
                logging.info('curr_pic:{}'.format(pic.pic_path))
                logging.info('curr modules[{}]: {}'.format(index, pic_modules[index].pic_path))
                logging.info('ratio = {}, {} {} similar.'.format(ratio, pic_modules.index(pic), index))
                pic.similar_pic_list.append(copy.copy(pic_modules[index]))
                break
            else:
#                 logging.info('ratio = {}, {} {} not similar.'.format(ratio, pic_modules.index(pic), index))
                pass
        pass
    
    index = 0
    for pic in pic_modules:
        if pic.del_flag:
            logging.info(pic)
            same_folder = pic.pic_path.split('.jpg')[0] + "_" + str(index)
            
            print(same_folder)
            if not os.path.exists(same_folder):
                os.makedirs(same_folder)
            shutil.copy(pic.pic_path, same_folder)
            if pic.cmp_same_pic_path[0]:
                shutil.copy(pic.cmp_same_pic_path[0], same_folder)
            
            for psss in pic.cmp_same_pic_path:
                logging.info(psss)
                shutil.copy(psss, same_folder)
                shutil.copy(pic.pic_path, same_folder)
            
#             os.remove(pic.pic_path)
            for p in pic.similar_pic_list:
                shutil.copy(p.pic_path, same_folder)
                logging.info(p)
            index += 1
            
            # move file to like folder

def initLogging(logFilename):
    """Init for logging
    """
    logging.basicConfig(
                      level    = logging.INFO,
                      format   ='%(asctime)s [%(levelname)s]<%(funcName)s,%(lineno)d> %(message)s',
                      datefmt  = '%Y_%m_%d %H:%M:%S',
                      filename = logFilename,
                      filemode = 'w');
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]<%(funcName)s,%(lineno)d> %(message)s')
    console.setFormatter(formatter)
#     th = handlers.TimedRotatingFileHandler(filename=logFilename,when='D',backupCount=3,encoding='utf-8')
#     th.setFormatter('%y-%m-%d %H:%M:%S')
    logging.getLogger('').addHandler(console)

def getCurrentDate():
    return time.strftime('%Y-%m-%d_%H_%M_%S')


def get_test_result_folder(path):
    tmp = []
    like = ''
    for folder in os.listdir(path):
        if os.path.isdir(os.path.join(path, folder)):
            if 'IMG' in folder:
                tmp.append(os.path.join(path, folder))
            else:
                like = os.path.join(path, folder)
    return tmp, like

def test_result_correct_ratio(path):
    pic_folders, like_folder = get_test_result_folder(path)
    print(like_folder)
    print(pic_folders)
    
    for pic_folder in pic_folders:
        ahash_res = judge_pics_ops(pic_folder, avg_hash)
        phash_res = judge_pics_ops(pic_folder, phash)
        dhash_res = judge_pics_ops(pic_folder, dhash)
        print('{} ahash = {}. phash = {}, dhash = {}'.format(pic_folder, ahash_res, phash_res, dhash_res))
        
    pass


if __name__ == '__main__':
    
#     img1 = cv2.imread("./img1.jpg")
#     img2 = cv2.imread("./img2.jpg")
#     img2 = cv2.imread("./img1.jpg")
#     
#     img1_ahash = avg_hash("./img1.jpg")
#     img2_ahash = avg_hash("./img2.jpg")
#     
#     img1_dhash = dhash(img1)
#     img2_dhash = dhash(img2)
#     
#     print(cmp_hash(img1_ahash, img2_ahash))
#     print(cmp_hash(img1_dhash, img2_dhash))
#     
#     img1_phash = phash("./img1.jpg")
#     img2_phash = phash("./img2.jpg")
#     print(cmp_hash(img1_phash, img2_phash))
    
    
    paths = 'E:\img\IMG_20200731_154849.jpg16'
    paths = 'E:\img\cmpcmp.jpg1'
    paths = 'E:\camera\IMG_20200731_153725.jpg10'
    paths = 'E:\camera\IMG_20200731_154331.jpg97'
    paths = 'E:\camera\IMG_20200731_154134.jpg32'
    paths = 'E:\camera\IMG_20200731_154012.jpg19'
#     paths = 'E:\img\IMG_20200731_155002.jpg34'
#     judge_pics(paths)
#     judge_pics_p(paths)
#     judge_pics_d(paths)
    
    pathss = 'E:\camera'
#     test_result_correct_ratio(pathss)
    
    
    del_md5_flag = True
    img_path = 'E:\\camera'
    
    initLogging(getCurrentDate() + '.log')
    filter_camera_img()
    

    logging.info('#'*40)
    logging.info('#'*11 + ' PIC_COMPARE_END ' + '#'*12)
    logging.info('#'*40)
    pass



