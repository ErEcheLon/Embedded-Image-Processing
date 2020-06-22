import serial
#import globals
from time import sleep
#/dev/ttyUSB0
sp = serial.Serial("/dev/ttyUSB0", 250000, timeout=30)#30sec timeout
BeadSize =9.5
LiftHeight  =18
TouchHeight  =3

OriginalX=68
OriginalY=105

Xpos,Ypos,Zpos=0,0,0

def AutoHome():
    global Xpos,Ypos,Zpos
    SetSpeed(250)
    Move(z=LiftHeight)
    SendCommand("G28")
    Xpos,Ypos,Zpos=0,0,0
    #globals.Is_Autohome = True
    #globals.Is_Work = True
    
def SendRoute(Coor,Routes):#Coor(X,Y)
    StylusLift()
    MoveToBead_w6_h5(Coor)
    StylusTouch()
    
    for Dir in Routes:
        if Dir == "U":
            MoveR(x=BeadSize)
        elif Dir == "D":
            MoveR(x=BeadSize*-1)
        elif Dir == "L":
            MoveR(y=BeadSize)
        elif Dir == "R":
            MoveR(y=BeadSize*-1)
            
    StylusLift()
    Move(x=0,y=0)
    
def MoveToBead_w6_h5(Coor):
    Move(x=OriginalX+Coor[1]*BeadSize*-1,y=OriginalY+Coor[0]*BeadSize*-1)#Flip X,Y in Pursa i3

def Move(x=None,y=None,z=None):
    global Xpos,Ypos,Zpos
    cmd = "G0 "
    if x!=None:
        cmd+=" X"+str(x)
        Xpos=x
    if y!=None:
        cmd+=" Y"+str(y)
        Ypos=y
    if z!=None:
        cmd+=" Z"+str(z)
        Zpos=z
    
    if x!=None or y!=None or z!=None:
        SendCommand(cmd)
        
        
def MoveR(x=None,y=None,z=None):#MoveRelative
    absX,absY,absZ= None,None,None
    if x!=None:
        absX=Xpos+x
    if y!=None:
        absY=Ypos+y
    if z!=None:
        absZ=Zpos+z
    
    if absX!=None or absY!=None or absZ!=None:
        Move(x=absX,y=absY,z=absZ)

def StylusLift():
    Move(z=LiftHeight);

def StylusTouch():
    Move(z=TouchHeight);
    
def SetSpeed(speed):
    return SendCommand("M220 S"+str(speed))

def WaitUntilFinish():
    return SendCommand("M400")

def SendCommand(cmd):
    sp.write(cmd.encode('ascii'))
    sp.write(b"\r\n")
    print("Sp Tx:"+cmd)
    rx = sp.readline()
    print("Sp Rx:"+str(rx))
    return rx==b'ok\n'
    
if __name__ == '__main__':
    AutoHome()
    SendRoute((1,0),["D","D","R","R","U","U","L","L"])
    
    
    
    