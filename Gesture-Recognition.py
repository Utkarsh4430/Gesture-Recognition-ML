import numpy as np
import cv2
from keras.models import load_model

weights = load_model("Gesture-model-saved.h5")

classes = {
	0:"peace out",
	1:"spock",
	2:"fuck",
	3:"you",
	4:"all the best",
	5:""
}

def predict(hand):
	img = cv2.resize(hand,(64,64))
	img = img/255.0
	img = img.reshape(1,64,64,1)
	pred = weights.predict(img)
	final = pred.argmax()
	return classes[final]


video_capture = cv2.VideoCapture(0) # We turn the webcam on

#Following values of variables are to place the rectangle 
#found by trial and error
x = 380
y = 125
h = 210
w = 210

count = 1;
prev = ""
new = ""
total = "" 
basic = 150
def func(frame):
	frame = cv2.flip(frame,1) #flipping because webcam gives laterally inverted image
	cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) #forming a rectangular area to mark the area for gestures
	hand = frame[y:y+h,x:x+w]	
	hand = cv2.cvtColor(hand, cv2.COLOR_BGR2GRAY)	#converting to greyscale
	thresh = cv2.threshold(hand,220,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]  #marking a threshold for colours
	frame[y:y+h,x:x+w,0] = thresh   #rectanguler of the image is converted to black and white to mark the area of gestures
	frame[y:y+h,x:x+w,1] = thresh
	frame[y:y+h,x:x+w,2] = thresh
	return thresh,frame;


while True: # We repeat infinitely (until break):
	_, frame = video_capture.read() 
	thresh,frame = func(frame)
	prev = new
	new = predict(thresh)
	if(basic>=0):
		basic-=1
		new = ""
	if prev==new:
		count+=1
	else:
		count=0
	screen = np.zeros(frame.shape)
	cv2.putText(screen, "Predicted text - ", (20, 40), cv2.FONT_HERSHEY_TRIPLEX, 1, (122, 155, 0))
	if count > 100 and new != "":
            total += new + " "
            count = 0
	cv2.putText(screen, total, (20, 80), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (123, 123, 123))
	if(count>250):
		count = 0;

	cv2.imshow('Video', frame) # We display the outputs.
	cv2.imshow('Text', screen)
	if cv2.waitKey(1) & 0xFF == ord('q'): # If we type 'q' on the keyboard:
		break # We stop the loop.

video_capture.release() # We turn the webcam off.
cv2.destroyAllWindows() # We destroy all the windows inside which the images were displayed.