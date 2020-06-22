import cv2
import numpy as np
import requests
import json
import asyncio
import time

def DetectedPlate(img):
    # define range of blue color in HSV
    lower_blue = np.array([89,50,0])
    upper_blue = np.array([122,255,255])

    # define range of green color in HSV 
    lower_green = np.array([58,50,0])
    upper_green = np.array([83,255,255])

    # define range of red color in HSV 
    lower_red = np.array([0,50,0])
    upper_red = np.array([21,255,255])

    # define range of yellow color in HSV
    lower_yellow = np.array([25,50,0])
    upper_yellow = np.array([58,255,255])

    #define range of purple color in HSV
    lower_purple = np.array([114,50,0])
    upper_purple = np.array([140,255,255])

    #define range of pink color in HSV
    lower_pink = np.array([138,50,0])
    upper_pink = np.array([167,255,255])

    # Height  : 399
    # Width : 226

    #血量辨識區域
    size = img.shape
    #print(size[0])
    #print(size[1])
    #print(size[2])
    #print(int(size[1]/6))

    x = 0
    y = 0 + (size[0] - int(size[1]/6)*5 - int(size[1]/6/2))
    w = size[1]
    h = int(size[1]/6/2)
    #print(w)
    #print(h)

    hp_img = img[y:y+h, x:x+w]

    hsv = cv2.cvtColor(hp_img, cv2.COLOR_BGR2HSV)
    hp_mask = 0
    hp_mask = cv2.inRange(hsv, lower_pink, upper_pink)
    k = j = hp_counter = 0
    HeartPoint = 110 #血量條僅有血量區塊以及愛心符號區域之Counter數
    num_rows, num_cols = hp_mask.shape
    for k in range(num_rows):
        for j in range(num_cols):
            if hp_mask[k][j] == 255:
                hp_counter += 1

    #盤面辨識
    size = img.shape
    #print(size[0])
    #print(size[1])
    #print(size[2])
    #print(int(size[1]/6))

    x = size[1]
    y = size[0]
    w = int(size[1]/6)
    h = int(size[1]/6)
    #print(w)
    #print(h)

    i = 0
    layout = np.zeros(shape=(5,6))
    layout_X = np.zeros(shape=(5,6))
    layout_Y = np.zeros(shape=(5,6))
    row = col = 0

    for i in range(5):
        y = y - h
        for j in range(6):
            if j == 0:
                size = img.shape
                x = size[1] - w
            else:
                x = x - w
            #print(x)
            crop_img = img[y:y+h, x:x+w]
            size = crop_img.shape
            hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
            mask = ['0','0','0','0','0','0']
            # Threshold the HSV image to get only blue colors
            mask[0] = cv2.inRange(hsv, lower_red, upper_red)
            # Threshold the HSV image to get only green colors
            mask[1] = cv2.inRange(hsv, lower_blue, upper_blue)
            # Threshold the HSV image to get only red colors   
            mask[2] = cv2.inRange(hsv, lower_green, upper_green)
            # Threshold the HSV image to get only yellow colors   
            mask[3] = cv2.inRange(hsv, lower_yellow, upper_yellow)
            # Threshold the HSV image to get only purple colors   
            mask[4] = cv2.inRange(hsv, lower_purple, upper_purple)
            # Threshold the HSV image to get only pink colors   
            mask[5] = cv2.inRange(hsv, lower_pink, upper_pink)

            z = 0;
            color_counter = [0,0,0,0,0,0];
            for z in range(len(color_counter)):
                k = j = 0;
                num_rows, num_cols = mask[z].shape
                for k in range(num_rows):
                    for j in range(num_cols):
                        if mask[z][k][j] == 255:
                            color_counter[z] += 1
            #print(color_counter)
            if color_counter[0] > color_counter[1] and color_counter[0] > color_counter[2] and color_counter[0] > color_counter[3] and color_counter[0] > color_counter[4] and color_counter[0] > color_counter[5]:
                #print('Red')
                layout[col][row] = "0"
            elif color_counter[1] > color_counter[0] and color_counter[1] > color_counter[2] and color_counter[1] > color_counter[3] and color_counter[1] > color_counter[4] and color_counter[1] > color_counter[5]:
                #print('Blue')
                layout[col][row] = "1"
            elif color_counter[2] > color_counter[0] and color_counter[2] > color_counter[1] and color_counter[2] > color_counter[3] and color_counter[2] > color_counter[4] and color_counter[2] > color_counter[5]:
                #print('Green')
                layout[col][row] = "2"
            elif color_counter[3] > color_counter[0] and color_counter[3] > color_counter[1] and color_counter[3] > color_counter[2] and color_counter[3] > color_counter[4] and color_counter[3] > color_counter[5]:
                #print('Yellow')
                layout[col][row] = "3"
            elif color_counter[4] > color_counter[0] and color_counter[4] > color_counter[1] and color_counter[4] > color_counter[2] and color_counter[4] > color_counter[3] and color_counter[4] > color_counter[5]:
                #print('Purple')
                layout[col][row] = "4"
            elif color_counter[5] > color_counter[0] and color_counter[5] > color_counter[1] and color_counter[5] > color_counter[2] and color_counter[5] > color_counter[3] and color_counter[5] > color_counter[4]:
                #print('Heart')
                layout[col][row] = "5"
            row += 1
            if row >= 6:
                row = 0
                col += 1

    #print(layout)

    new_layout = layout.reshape(layout.size)
    new_layout = new_layout[::-1]
    new_layout = new_layout.reshape(layout.shape)

    #print("\n\n\n")
    #print("Red = 0 , Blue = 1 , Green = 2 , Yellow = 3 , Purple = 4 , Heart = 5")
    #print("\n\n\n")
    #print(new_layout)

    #print("\r\nTotal hp_value:" , hp_counter)
    #print("Real hp_value:" , hp_counter-HeartPoint)
    HP_Percent = (hp_counter-HeartPoint)/465*75
    #print("HP:",HP_Percent)

    return new_layout#,HP_Percent

#POST訊息格式
#{"Width":6,"Height":5,"Beads":[5,1,5,3,1,2,1,0,5,5,1,1,3,4,0,0,3,1,2,1,1,0,0,5,4,4,0,4,4,5],"Weights":
#[1.0,1.0,1.0,1.0,1.0,1.0],"SelectStartX":0,"SelectEndX":6,"SelectStartY":0,"SelectEndY":5,"StepLimit":40,"MoveDirection":4,"TargetScore":6000,"Length":30,"BeadTypesCount":6,"HasWeight":false}

def DetectedRoute(new_layout):
    #plate
    send_layout = new_layout.flatten()
    #weight
    Weights = np.zeros(6)
    i = 0
    for i in range(len(Weights)):
        Weights[i] = 1;
    Width_value = 6
    Hight_value = 5
    i = 0
    Beads_value = '['
    for i in range(len(send_layout)): 
        if i == len(send_layout) - 1:
            Beads_value += repr(int(send_layout[i])) + ']'
        else:
            Beads_value += repr(int(send_layout[i])) + ','
    i = 0
    Weights_value = '['
    for i in range(len(Weights)):
        if i == len(Weights) - 1 :
            Weights_value += repr(Weights[i]) + ']'
        else:
            Weights_value += repr(Weights[i]) + ','
    SelectStartX_value = 0
    SelectEndX_value = 5
    SelectStartY_value = 0
    SelectEndY_value = 4
    StepLimit_value = 40
    MoveDirection_value = 4
    TargetScore_value = 7000
    Length_value = 30
    BeadTypesCount_value = 6
    
    #POST訊息
    payload = {"Width":Width_value,"Height":Hight_value,"Beads":json.loads(Beads_value),"Weights":json.loads(Weights_value),"SelectStartX":0,"SelectEndX":3,"SelectStartY":0,"SelectEndY":5,"StepLimit":StepLimit_value,"MoveDirection":MoveDirection_value,"TargetScore":TargetScore_value,"Length":Length_value,"BeadTypesCount":BeadTypesCount_value,"HasWeight":0}
    payload1 = {"Width":Width_value,"Height":Hight_value,"Beads":json.loads(Beads_value),"Weights":json.loads(Weights_value),"SelectStartX":3,"SelectEndX":6,"SelectStartY":0,"SelectEndY":5,"StepLimit":StepLimit_value,"MoveDirection":MoveDirection_value,"TargetScore":TargetScore_value,"Length":Length_value,"BeadTypesCount":BeadTypesCount_value,"HasWeight":0}

    headers={'Content-type':'application/json', 'Accept':'application/json'}
    
    loop = asyncio.new_event_loop()
    #url = 'https://padsolver.azurewebsites.net/api/solve?solvername=LinkSolver'
    url0 = 'http://163.18.109.80:5000/api/solve?solvername=LinkSolver'
    url1 = 'http://163.18.109.80:5001/api/solve?solvername=LinkSolver'

    def Req_Send(i):
        if i == 0:
            html_get = requests.post(url0, data = json.dumps(payload), headers = headers)
        elif i == 1:
            html_get = requests.post(url1, data = json.dumps(payload1), headers = headers)
        return html_get

    async def send_req(i):
        global First_Flag
        global First_Html_Get
        global response_value
        First_Flag = False

        html_get = await loop.run_in_executor(None,Req_Send,i)
        #print(html_get)
        #print(html_get.text)
        if First_Flag == False:
            First_Flag = True
            First_Html_Get = html_get
            #print("AAA")
            print(First_Html_Get.text)
            loop.stop()

    tasks = []

    i = 0
    for i in range(2):
        #print(i)
        task = loop.create_task(send_req(i))
        tasks.append(task)

    #loop.run_until_complete(asyncio.wait(tasks))
    loop.run_forever()
    loop.close()
    
    response_value = json.loads(First_Html_Get.text)
    response_value = json.loads(response_value)
    #print(response_value)

    #response
    #{"StartX":1,"StartY":3,"Directions":["D","R","R","R","U","U","L","L","L","D","D","R","R","R","R","U","U","L","L","L","U","R"],"Score":6045.0,"Result":[2,0,1,0,4,3,3,0,2,3,1,2,5,0,2,3,3,2,3,3,0,0,0,3,5,1,2,5,5,5],"TimeComsumedMs":38,"Iteration":7}
    #print(response_value['StartX'])
    #print(response_value['StartY'])
    #print(response_value['Directions'])
    
    return response_value['StartX'],response_value['StartY'],response_value['Directions']

def DetectedFinish(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binaryIMG = cv2.Canny(gray, 40, 235) #20/160
    contours, hierarchy = cv2.findContours(binaryIMG, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    i = 0  
    Finish = False
    for c in contours:
        i+=1
        M = cv2.moments(c)
        x, y, w, h = cv2.boundingRect(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        area = cv2.contourArea(c)  #計算面積
        perimeter = cv2.arcLength(c, True)    #計算周長
        if perimeter >= 400 and perimeter <= 500 and w >= 160 and w <= 190 and h >= 40 and h <= 60: #perimeter >= 450 and perimeter <= 460
            Finish = True
            break
        
    return Finish
