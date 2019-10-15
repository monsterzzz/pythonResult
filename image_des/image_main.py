from PIL import Image
import pytesseract
#上面都是导包，只需要下面这一行就能实现图片文字识别

the_door = 180
table = []
for i in range(256):
    if i < the_door:
        table.append(1)
    else:
        table.append(0)

cout = 0
for i in range(1,6):
    for k in range(31):
        try:
            print('2011_0%s/%s.png' % (str(i),str(k)))
            im = Image.open('2011_0%s/%s.png' % (str(i),str(k)))
            size = im.size
            #new_im = im.crop((size[0]/2,size[1],size[0],size[1]))
            new_im = im.crop((83,35,128,50))
            size = new_im.size
            new_im = new_im.resize((size[0] * 10, size[1] * 10),Image.ANTIALIAS)
            new_im = new_im.convert('L')
            new_im = new_im.point(table,'1')
            size = new_im.size
            new_im = new_im.resize((int(size[0] / 10) , int(size[1]  / 10)),Image.ANTIALIAS)
            # datas = new_im.getdata()
            # print(datas)
            # newData = []
            # for item in datas:
            #     #print(item)
            #     if item == 1:
            #         newData.append(( 255, 255, 255, 0))
            #     else:
            #         newData.append(item)
            
            # new_im.putdata(newData)
            #img.save(dstImageName,"PNG")
            #print(new_im.size)
            #text = pytesseract.image_to_string(new_im)
            new_im.save('test/'+ str(cout) + '.png')
            #new_im.save('test/'+ text + '.png')
            #print(text)
            #break
            cout += 1
        except BaseException as e:
            print(e)


# im = Image.open('2011_02/16.png')
# size = im.size
# #new_im = im.crop((size[0]/2,size[1],size[0],size[1]))
# new_im = im.crop((83,35,128,50))
# size = new_im.size
# new_im = new_im.resize((size[0] * 10, size[1] * 10),Image.ANTIALIAS)
# new_im = new_im.convert('L')
# new_im = new_im.point(table,'1')
# size = new_im.size
# new_im = new_im.resize((int(size[0] / 10) , int(size[1]  / 10)),Image.ANTIALIAS)
# new_im.save('k.png')