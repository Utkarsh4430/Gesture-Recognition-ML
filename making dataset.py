import cv2
video_capture = cv2.VideoCapture(0) # We turn the webcam on

#Following values of variables are to place the rectangle 
#found by trial and error
x = 380
y = 125
h = 210
w = 210

def func(frame):
	frame = cv2.flip(frame,1) #flipping because webcam gives laterally inverted image
	cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2) #forming a rectangular area to mark the area for gestures
	hand = frame[y:y+h,x:x+w]	
	hand = cv2.cvtColor(hand, cv2.COLOR_BGR2GRAY)	#converting to greyscale
	thresh = cv2.threshold(hand,210,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]  #marking a threshold for colours
	frame[y:y+h,x:x+w,0] = thresh   #rectanguler of the image is converted to black and white to mark the area of gestures
	frame[y:y+h,x:x+w,1] = thresh
	frame[y:y+h,x:x+w,2] = thresh
	return thresh,frame;

count = 1;
while True: # We repeat infinitely (until break):
	_, frame = video_capture.read() 
	thresh,frame = func(frame)
	name = str(count) + '.jpeg'
	if count<=1200:
		cv2.imwrite(name,thresh)  #writing the files
		count+=1
	cv2.imshow('Video', frame) # We display the outputs.
	if cv2.waitKey(1) & 0xFF == ord('q'): # If we type 'q' on the keyboard:
		break # We stop the loop.

video_capture.release() # We turn the webcam off.
cv2.destroyAllWindows() # We destroy all the windows inside which the images were displayed.