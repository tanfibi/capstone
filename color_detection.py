import cv2
import numpy as np
import pandas as pd
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
arg = vars(ap.parse_args()) 
image_path = arg['image']

image = cv2.imread(image_path)

clicked = False
r = g = b = xpos = ypos = 0

index=["colour","name","hex","R","G","B"]
csv = pd.read_csv('list.csv', names=index, header=None)

def getColourName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d <= minimum):
            minimum = d
            c_name = csv.loc[i,"name"]
    return c_name

def draw_colour(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = image[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
       
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_colour)

while(1):

    cv2.imshow("image",image)
    if (clicked):
   
        cv2.rectangle(image,(20,20), (500,60), (b,g,r), -1)

        text = getColourName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b) 
        
        y0, dy = 50, 4
        for i, line in enumerate(text.split('\n')):
            y = y0 + i*dy
            cv2.putText(image, text,(50,50),4,0.8,(255,255,255),2,cv2.LINE_AA)

            if(r + g + b >= 600):
                cv2.putText(image, text,(50,50),4,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
