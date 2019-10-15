from PIL import Image
import os
from libsvm.python.svmutil import *
from libsvm.python.svm import *




# cout = 0
# for i in range(80,100):
#     im = Image.open('test/%s.png' % str(i))
#     for k in range(3):
#         try:
#             new_im = im.crop((default1,default2,default3,default4))
#             default1 += change
#             default3 += change
#             new_im.save('predictdd/%s.png' % (str(cout)))
#             cout += 1
#         except BaseException as e:
#             print(e)
#     default1 = 3
#     default2 = 3
#     default3 = 9
#     default4 = 13

# for i in range(10):
#     list_dir = os.listdir(os.getcwd() + '\\result\\%s' % str(i) )
#     for k in list_dir:
#         pixel_cnt_list = []
#         new_im = Image.open(os.getcwd() + '\\result\\%s\\' % str(i) + k)
#         size = new_im.size
#         for x in range(size[0]):
#             pix_cnt_x = 0
#             for y in range(size[1]):
#                 if new_im.getpixel((x,y)) == 0:
#                     pix_cnt_x += 1
#             pixel_cnt_list.append(pix_cnt_x)
#         for y in range(size[1]):
#             pix_cnt_y = 0
#             for x in range(size[0]):
#                 if new_im.getpixel((x,y)) == 0:
#                     pix_cnt_y += 1
#             pixel_cnt_list.append(pix_cnt_y)
#         string = '%s' % str(i)
#         for item in range(len(pixel_cnt_list)):
#             string += ' %s:%s' % (str(item + 1),str(pixel_cnt_list[item]))
#         print(string)
#         with open('result.txt','a+') as f:
#             f.write(string + '\n')





def split_img(img_path):
    default1 = 3
    default2 = 3
    default3 = 9
    default4 = 13
    change = 6 + 2
    im = Image.open(img_path)
    result = []
    for k in range(5):
        try:
            new_im = im.crop((default1,default2,default3,default4))
            default1 += change
            default3 += change
            result.append(new_im)
        except BaseException as e:
            print(e)
    return result

def get_feature(img_obj):
    pixel_cnt_list = []
    new_im = img_obj
    size = new_im.size
    for x in range(size[0]):
        pix_cnt_x = 0
        for y in range(size[1]):
            if new_im.getpixel((x,y)) == 0:
                pix_cnt_x += 1
        pixel_cnt_list.append(pix_cnt_x)
    for y in range(size[1]):
        pix_cnt_y = 0
        for x in range(size[0]):
            if new_im.getpixel((x,y)) == 0:
                pix_cnt_y += 1
        pixel_cnt_list.append(pix_cnt_y)
    def get_zero(x):
        return x != 0
    if len(list(filter(get_zero,pixel_cnt_list))) == 0 :
        return False
    string = '0'
    for item in range(len(pixel_cnt_list)):
        string += ' %s:%s' % (str(item + 1),str(pixel_cnt_list[item]))
    return string

def img_to_string(feature):
    if feature == False:
        return ''
    else:
        with open('temp.txt','w+') as f:
            f.write(feature)
        yt, xt = svm_read_problem('temp.txt')
        model = svm_load_model('value_predict.model')
        p_label, p_acc, p_val = svm_predict(yt, xt, model,options="-q")
        return p_label[0]


def get_result(img_path):
    img_list = split_img(img_path)
    res = ''
    for i in img_list:
        fea = get_feature(i)
        result = img_to_string(fea)
        try:
            res += str(int(result))
        except:
            pass
    return res

for i in range(153):
    im = Image.open('test/%s.png' % str(i))
    result = get_result('test/%s.png' % str(i)).replace('9999',',')
    im.save('m/%s.png' % result)

#im = Image.open('m/17015.png')
# img_list = split_img('m/17025.png')
# d = get_feature(img_list[1])
# print(d)