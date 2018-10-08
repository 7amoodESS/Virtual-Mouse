#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 15:02:20 2018

@author: rld1996
"""

import numpy as np
import cv2
import wx
from pynput.mouse import Button,Controller
lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])
cam=cv2.VideoCapture(0)

   
mouse=Controller()
app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
(camx,camy)=(400,400)

while(cam.isOpened()):
    ret,img=cam.read()
    img=cv2.resize(img,(400,400))
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    filt=cv2.inRange(hsv,lowerBound,upperBound)
    
    kernelOpen=np.ones((5,5))
    kernelClose=np.ones((20,20))
    maskOpen=cv2.morphologyEx(filt,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    
    
    im2,conts,h=cv2.findContours(maskClose.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img,conts,-1,(0,220,0),5)
    for cnt in conts:
        vertices = cv2.boundingRect(cnt)
        x=vertices[0]
        y=vertices[1]
        w=vertices[2]
        h=vertices[3]    
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        
    pinch=0
   
    if len(conts)==2:
        if(pinch==1):
            pinch=0
            
            
        
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),3)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),3)
        cx1=x1+w1/2
        cy1=y1+h1/2
        cx2=x2+w2/2
        cy2=y2+h2/2
        cv2.line(img,(cx1,cy1),(cx2,cy2),(0,0,255),3)
        clx=(cx1+cx2)/2
        cly=(cy1+cy2)/2
        cv2.circle(img,(clx,cly),5,(0,255,0),3)
        
        mouseLocation=(sx-(clx*sx/camx),cly*sy/camy)
        mouse.position=mouseLocation
        if mouse.position!=mouseLocation:
            pass
        else:
            mouse.press(Button.left)
        
    elif len(conts)==1:
        if(pinch==0):
            pinch=1
       # if(mouse.press(Button.left)):
            mouse.release(Button.left)
        
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),3)
        
        clx=x1+w1/2
        cly=y1+h1/2
        
        
        
        cv2.circle(img,(clx,cly),5,(0,255,0),3)
        mouseLocation=(sx-(clx*sx/camx),cly*sy/camy)
        mouse.position=mouseLocation
        if mouse.position!=mouseLocation:
            pass
        
     
    
    
    img2=np.hstack((maskOpen,maskClose))
    img2=np.hstack((maskOpen,maskClose,im2))
    cv2.imshow("all1",filt)
    cv2.imshow("all3",img)
    cv2.imshow("all2",img2)
    k=cv2.waitKey(10)
    if k==27:
        cv2.destroyAllWindows()
        cam.release()
        
   
    
        
