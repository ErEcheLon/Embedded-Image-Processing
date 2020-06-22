import cv2
import numpy as np
from asq import query
import Real_IMG
import Stylus
import time
import ImageAnalyzer

if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    state='init'
    
    while 1:
        success, img = camera.read()
        
        #cv2.imshow("img",img);
        if success:
            found,PhoneImg,StartP,EndP = ImageAnalyzer.FindPhone(img.copy())
            #found=1
            #PhoneImg = img[138:356,120:513]#328 138 513 356            
            if(found):
                PhoneImg = np.rot90(PhoneImg,3)
                cv2.imshow("PhoneImg",PhoneImg)
                BoardImg=ImageAnalyzer.ExtractBoardImg(PhoneImg)
                brightness=ImageAnalyzer.CalcBrightness(BoardImg)
                cv2.imshow("BoardImg",BoardImg)
                cv2.waitKey(10)
                
                if state=='init':
                    print("init....")
                    Stylus.AutoHome()
                    Stylus.SetSpeed(400)
                    BrightnessLowThres=ImageAnalyzer.CalcBrightness(BoardImg)*0.6
                    print("BrightnessLowThres:"+str(BrightnessLowThres))
                    BrightnessUpThres=ImageAnalyzer.CalcBrightness(BoardImg)*0.9
                    print("BrightnessUpThres:"+str(BrightnessUpThres))
                    print("switch to play")
                    state='play'
                    
                elif state=='play':
                    board=Real_IMG.DetectedPlate(PhoneImg)
                    print(board)
                    startX,startY,routes=Real_IMG.DetectedRoute(board)
                    Stylus.SendRoute((startX,startY),routes)
                    Stylus.Move(x=0,y=0)
                    Stylus.WaitUntilFinish()
                    print("switch to waitdrop")
                    state='waitdrop'                    
                    
                elif state=='waitdrop':
                    if(ImageAnalyzer.CalcBrightness(BoardImg)<BrightnessLowThres):
                        state='waitstage'
                        print("brightness:"+str(brightness))
                        print("switch to waitstage")
                
                
                elif state=='waitstage':
                    if(ImageAnalyzer.CalcBrightness(BoardImg)>BrightnessUpThres):
                        state='play'
                        print("brightness:"+str(brightness))
                        print("switch to play")
                        time.sleep(0.5)
                    elif Real_IMG.DetectedFinish(PhoneImg):
                        print("Finished!")                        
                        break;
camera.release()                        
cv2.waitKey(0)
cv2.destroyAllWindows()


# #設定window
# window = Tk()
# window.title("Auto Rolling")
# window.geometry('1200x410')

# #創建hp視窗
# panel_hp = Label(window)
# panel_hp.place(x=500, y=180, anchor='nw')

# #創建contours視窗
# panel_contours = Label(window)
# panel_contours.place(x=20, y=10, anchor='nw')

# #創建final視窗
# panel_final = Label(window)
# panel_final.place(x=250, y=10, anchor='nw')

# #創建盤面資訊視窗
# label_text = Label(window)
# label_text.place(x=500,y=50,anchor='nw')

# #創建盤面資訊視窗
# label_result = Label(window)
# label_result.place(x=500,y=80,anchor='nw')

# #創建資訊視窗
# label_information = Label(window)
# label_information.place(x=500,y=120,anchor='nw')

# #創建hp視窗
# label_hp = Label(window)
# label_hp.place(x=500,y=200,anchor='nw')

# #創建hp視窗
# label_hp_Percent = Label(window)
# label_hp_Percent.place(x=560, y=200, anchor='nw')

# #創建StartX顯示視窗
# label_StartX = Label(window)
# label_StartX.place(x=580,y=220,anchor='nw')

# #創建StartY顯示視窗
# label_StartY = Label(window)
# label_StartY.place(x=560,y=220,anchor='nw')

# #創建G code控制視窗
# label_ControlInfo = Label(window)
# label_ControlInfo.place(x=560,y=250,anchor='nw')

# #創建G code控制視窗
# label_ControlInfo = Label(window)
# label_ControlInfo.place(x=560,y=250,anchor='nw')

# #創建start按鈕
# #btn_start = Button(window, text="Start", command=take_star).place(x=500, y=10, anchor='nw')

# #創建auto home按鈕
# btn_start = Button(window, text="Start", command=take_AutoHome).place(x=600, y=10, anchor='nw')


# camera_loop()
# window.mainloop()

# #完成後關閉攝影機釋放資源
# camera.release()
# cv2.destroyAllWindows()