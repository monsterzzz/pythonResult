import numpy as np
import cv2
import math
from scipy import signal
import image
import scipy

def Hessian2D(I, Sigma):

    if Sigma < 1:
        print("error: Sigma<1")
        return -1
    I = np.array(I, dtype=float)
    Sigma = np.array(Sigma, dtype=float)
    S_round = np.round(3 * Sigma)

    [X, Y] = np.mgrid[-S_round:S_round + 1, -S_round:S_round + 1]

    DGaussxx = 1 / (2 * math.pi * pow(Sigma, 4)) * (X ** 2 / pow(Sigma, 2) - 1) * np.exp(
        -(X ** 2 + Y ** 2) / (2 * pow(Sigma, 2)))
    DGaussxy = 1 / (2 * math.pi * pow(Sigma, 6)) * (X * Y) * np.exp(-(X ** 2 + Y ** 2) / (2 * pow(Sigma, 2)))
    DGaussyy = 1 / (2 * math.pi * pow(Sigma, 4)) * (Y ** 2 / pow(Sigma, 2) - 1) * np.exp(
        -(X ** 2 + Y ** 2) / (2 * pow(Sigma, 2)))

    Dxx = signal.convolve2d(I, DGaussxx, boundary='fill', mode='same', fillvalue=0)
    Dxy = signal.convolve2d(I, DGaussxy, boundary='fill', mode='same', fillvalue=0)
    Dyy = signal.convolve2d(I, DGaussyy, boundary='fill', mode='same', fillvalue=0)

    return Dxx, Dxy, Dyy


def eig2image(Dxx, Dxy, Dyy):
    Dxx = np.array(Dxx, dtype=float)
    Dyy = np.array(Dyy, dtype=float)
    Dxy = np.array(Dxy, dtype=float)
    if (len(Dxx.shape) != 2):
        print("len(Dxx.shape)!=2,Dxx is not！")
        return 0

    tmp = np.sqrt((Dxx - Dyy) ** 2 + 4 * Dxy ** 2)

    v2x = 2 * Dxy
    v2y = Dyy - Dxx + tmp

    mag = np.sqrt(v2x ** 2 + v2y ** 2)
    i = np.array(mag != 0)

    v2x[i == True] = v2x[i == True] / mag[i == True]
    v2y[i == True] = v2y[i == True] / mag[i == True]

    v1x = -v2y
    v1y = v2x

    mu1 = 0.5 * (Dxx + Dyy + tmp)
    mu2 = 0.5 * (Dxx + Dyy - tmp)

    check = abs(mu1) > abs(mu2)

    Lambda1 = mu1.copy()
    Lambda1[check == True] = mu2[check == True]
    Lambda2 = mu2.copy()
    Lambda2[check == True] = mu1[check == True]

    Ix1 = v1x
    Ix1[check == True] = v2x[check == True]
    Iy1 = v1y
    Iy1[check == True] = v2y[check == True]

    Ix2 = v2x
    Ix2[check == True] = v1x[check == True]
    Iy2 = v2y
    Iy2[check == True] = v1y[check == True]

    return Lambda1, Lambda2, Ix1, Iy1, Ix2, Iy2

# def IPgaussian(sigma):
#     sigma = np.array(sigma)
#     R = np.int(2*sigma)+1
#     sum = 0
#     gau_template=np.zeros([R,R])
#     #[x,y] = np.mgrid[-R:R+1,-R:R+1]
#     for x in range(-sigma,sigma+1):
#         for y in range(-sigma,sigma+1):
#             gau_template[x+sigma][y+sigma] = 1 / (2 * math.pi * (sigma ** 2)) * np.exp(-(x ** 2 + y ** 2) / (2 * (sigma ** 2)))
#             sum = sum + gau_template[x+sigma,y+sigma]
#     g=gau_template/sum
#     return g
#
# def conv(image,template):
#     height,width=image.shape
#     h,w=template.shape
#     new_image=np.zeros([height,width],np.float32)
#     for i in range(0,height-h+1):
#         for j in range(0,width-w+1):
#             new_image[i,j]=np.sum(image[i:i+w,j:j+h]*template)
#             # new_image=new_image.clip(0,255)
#     return new_image

if __name__ == "__main__":
    img = cv2.imread('/Users/zhentang/Desktop/111.jpeg',0)
    # g = cv2.GaussianBlur(img, (3, 3), 2)
    [Dxx,Dxy,Dyy] = Hessian2D(img,2)
    [Lambda1, Lambda2, Ix1, Iy1, Ix2, Iy2]=eig2image(Dxx,Dxy,Dyy)
    R = np.array(Lambda2)
    print(R)

    # scipy.misc.imsave('/Users/zhentang/Desktop/1112.jpg', R)
    # blood = cv2.normalize(image.astype('double'), None, 0.0, 1.0, cv2.NORM_MINMAX) # Convert to normalized floating point
    # outIm=FrangiFilter2D(blood)
    # img=outIm*(10000)

    cv2.imshow('3',R)
    scipy.misc.imsave('/Users/zhentang/Desktop/101.bmp',R)
    cv2.waitKey(0)