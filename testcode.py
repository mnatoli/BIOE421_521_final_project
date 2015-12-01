#!/usr/bin/python

# remember to change the GPIO values below to match your sensors
#GPIO output = 18;
#GPIO input = 23;
from __future__ import division
import picamera
from collections import deque
def reading(sensor):
    import time
    import RPi.GPIO as GPIO 
    import array
    import itertools
    #Initialize camera
    camera = picamera.PiCamera()
    
    # Disable any warning message such as GPIO pins in use
    GPIO.setwarnings(False)
    
    # use the values of the GPIO pins, and not the actual pin number
    # so if you connect to GPIO 25 which is on pin number 22, the 
    # reference in this code is 25, which is the number of the GPIO 
    # port and not the number of the physical pin
    GPIO.setmode(GPIO.BCM)
    
    if sensor == 0:
        
        # point the software to the GPIO pins the sensor is using
        # change these values to the pins you are using
        # GPIO output = the pin that's connected to "Trig" on the sensor
        # GPIO input = the pin that's connected to "Echo" on the sensor
        GPIO.setup(18,GPIO.OUT)
        GPIO.setup(23,GPIO.IN)
        GPIO.output(18, GPIO.LOW)
        
        # found that the sensor can crash if there isn't a delay here
        # no idea why. If you have odd crashing issues, increase delay
        time.sleep(5)
        
        # sensor manual says a pulse ength of 10Us will trigger the 
        # sensor to transmit 8 cycles of ultrasonic burst at 40kHz and 
        # wait for the reflected ultrasonic burst to be received
        
        # to get a pulse length of 10Us we need to start the pulse, then
        # wait for 10 microseconds, then stop the pulse. This will 
        # result in the pulse length being 10Us.
	approaching = 0
	#create array limited to max length of 5 elements to store averages returned from Ulstrasonic sensor
	avgDistArray = deque(5*[0],5)
	while (approaching == 0):
		#create array of individual distance recordings
		distRecs = [0,0,0,0,0]
		for i in range(5):  
			# start the pulse on the GPIO pin 
		 	# change this value to the pin you are using
		   	# GPIO output = the pin that's connected to "Trig" on the sensor
		        GPIO.output(18, True)       
		        # wait 10 micro seconds (this is 0.00001 seconds) so the pulse
		        # length is 10Us as the sensor expects
	        	time.sleep(0.00001)        
		        # stop the pulse after the time above has passed
		        # change this value to the pin you are using
		        # GPIO output = the pin that's connected to "Trig" on the sensor
	        	GPIO.output(18, False)
		        # listen to the input pin. 0 means nothing is happening. Once a
		        # signal is received the value will be 1 so the while loop
		        # stops and has the last recorded time the signal was 0
		        # change this value to the pin you are using
		        # GPIO input = the pin that's connected to "Echo" on the sensor
	        	while GPIO.input(23) == 0:
	        	  signaloff = time.time()
		        # listen to the input pin. Once a signal is received, record the
		        # time the signal came through
		        # change this value to the pin you are using
		        # GPIO input = the pin that's connected to "Echo" on the sensor
	        	while GPIO.input(23) == 1:
	        	  signalon = time.time()
		        # work out the difference in the two recorded times above to 
		        # calculate the distance of an object in front of the sensor
	        	timepassed = signalon - signaloff
		        # we now have our distance but it's not in a useful unit of
		        # measurement. So now we convert this distance into centimetres
	        	distance = timepassed * 17000
		        # return the distance of an object in front of the sensor in cm
			#print (distance)
			distRecs[i] = distance
			#return distance
		        # we're no longer using the GPIO, so tell software we're done
		#take average of 5 individual distance recordings
		avgDistance = sum(distRecs)/len(distRecs)
		print (avgDistance)
		#remove right most element from the array (AKA prepare for shift)
		avgDistArray.pop()
		#Shift elements in array from left to right (FIFO)
		avgDistArray.appendleft(avgDistance)
		print (avgDistArray)
		#compare most recent 5 average distance recordings and look for an approaching pattern
		if avgDistArray[0] < avgDistArray[1] < avgDistArray[2] < avgDistArray[3] < avgDistArray[4]:
			#update that car is approaching so we can exit rear ultrasonic recording loop
			approaching = 1
		#delay between recordings to reduce power consumption
		time.sleep(0.3)
	camera.capture('approachingcar.jpg')
	#camera.capture(timestamp/'approachingcar.jpg')
	#print(timestamp, avgDistArray, passingDistance ->> datainfo.txt)
	return avgDistArray
        GPIO.cleanup()

    else:
        print "Incorrect usonic() function varible."

        
#print reading(0)
