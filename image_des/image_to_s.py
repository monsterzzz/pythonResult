from PIL import Image
import pytesseract


left = 27
upper = 0
right = 93
lower = 150

change = 80

# for i in range(20):
#     for k in range(3):
#         im = Image.open('test/%s.png' % str(i))
#         box = (left,upper,right,lower)
#         new_im = im.crop(box)
#         new_im.save('s/%s-%s.png' % (str(i),str(k)))
#         left += change
#         right += change
#         text = pytesseract.image_to_string(new_im)

for i in range(30):
    for k in range(3):
        im = Image.open('test/%s.png' % str(i))
        box = (left,upper,right,lower)
        new_im = im.crop(box)
        new_im.save('s/%s-%s.png' % (str(i),str(k)))
        left += change
        right += change
        text = pytesseract.image_to_string(new_im)
        print(text)
    left = 27
    right = 90