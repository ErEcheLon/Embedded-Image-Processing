import cv2
import numpy as np
from asq import query
import Real_IMG
import Stylus
import time

ShowDebugImg=1
PhoneStartX,PhoneStartY = None,None
EndX,EndY = None,None
        

def FindPhone(img):    
    global PhoneStartX,PhoneStartY,EndX,EndY
    
    #previous found
    if PhoneStartX!=None and PhoneStartY!=None and EndX!=None and EndY!=None:
        return (1,img[PhoneStartY:EndY, PhoneStartX:EndX],(PhoneStartX,PhoneStartY),(EndX,EndY))

    height, width, channels = img.shape
    if ShowDebugImg:
        DebugImg = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret,thres_img = cv2.threshold(gray, 25, 0, cv2.THRESH_TOZERO)
    #if ShowDebugImg:
    #    cv2.imshow("thres_img",thres_img)
    
    kernel5 = np.ones((5,5),np.uint8)
    erosion = cv2.erode(thres_img,kernel5,iterations = 1)
    kernel3 = np.ones((3,3),np.uint8)
    dilation = cv2.dilate(erosion,kernel3,iterations = 1)
    #if ShowDebugImg:
    #    cv2.imshow("morh",dilation)
    
    ret,thres_img2 = cv2.threshold(dilation, 25, 0, cv2.THRESH_TOZERO)
    #if ShowDebugImg:
    #    cv2.imshow("thres_img2",thres_img2)
    
    CannyIMG = cv2.Canny(thres_img2, 25, 200)
    #if ShowDebugImg:
    #    cv2.imshow("CannyIMG",CannyIMG)
    contours, hierarchy = cv2.findContours(CannyIMG, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    RectOriginPoints=[]
    RectEndPoints=[]
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)        
        wh_ratio = w/h
        area = w*h
        
        if 1350>=area>=600 and 1.2>=wh_ratio>=0.8:
            RectOriginPoints.append((x,y))
            RectEndPoints.append((x+w,y+h))
            if ShowDebugImg:
                cv2.rectangle(DebugImg, (x,y), (x+w,y+h), (127,127,127), 2)        
            
    
    #Search board
    BoardX,BoardY = 0,0
    EndX,EndY = 0,0
    TolerancePx=5
        
    if(len(RectOriginPoints)>0):
        #find start
        MinX,MinY = query(RectOriginPoints).select(lambda p: p[0]).min(),query(RectOriginPoints).select(lambda p: p[1]).min()
        for x in range(MinX,width,2):
            if query(RectOriginPoints).where(lambda p: abs(p[0]-x)<TolerancePx).count()>=3:
                BoardX=x
                break
                
        for y in range(MinY,height,2):
            if query(RectOriginPoints).where(lambda p: abs(p[1]-y)<TolerancePx).count()>=2:
                BoardY=y
                break
                

        #find end
        MaxX,MaxY = query(RectEndPoints).select(lambda p: p[0]).max(),query(RectEndPoints).select(lambda p: p[1]).max()
        for x in range(MaxX,0,-2):
            if query(RectEndPoints).where(lambda p: abs(p[0]-x)<TolerancePx).count()>=3:
                EndX=x
                break
                
        for y in range(MaxY,0,-2):
            if query(RectEndPoints).where(lambda p: abs(p[1]-y)<TolerancePx).count()>=2:
                EndY=y
                break
                
        #draw panel
        if ShowDebugImg:
            cv2.rectangle(DebugImg, (BoardX,BoardY), (EndX,EndY), (0,255,0), 2)

        PhoneHeight = EndY-BoardY
        PhoneWidth = (PhoneHeight/9)*16
        
        PhoneStartX = int(EndX-PhoneWidth)
        PhoneStartY = int(EndY-PhoneHeight)
        
        #draw Phone
        if ShowDebugImg:
            cv2.rectangle(DebugImg, (PhoneStartX,PhoneStartY), (EndX,EndY), (0,0,255), 2)
            cv2.imshow("DebugImg",DebugImg)
                
        found=PhoneStartX>0 and PhoneStartY>0 and EndY>PhoneStartY and EndX>PhoneStartX
        return (found,img[PhoneStartY:EndY, PhoneStartX:EndX],(PhoneStartX,PhoneStartY),(EndX,EndY))
    else:
        return (None,None,(0,0),(0,0))

def CalcBrightness(board_img):
    platehsv = cv2.cvtColor(board_img, cv2.COLOR_BGR2HSV)
    avg = platehsv[...,2].mean()
    return avg
    
def ExtractBoardImg(img):
    height, width, depth = img.shape
    perBeadSideLen = width/6
    return img[int(height-perBeadSideLen*5):int(height),0:int(width)]
    
if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    state='init'
    
    while 1:
        success, img = camera.read()
        #£cv2.imshow("img",img)
        if success:
            found,PhoneImg,StartP,EndP = FindPhone(img.copy())
        cv2.waitKey(10)    
    camera.release()
    
    
    
