#!/usr/bin/python

# remember to change the GPIO values below to match your sensors
#GPIO output = 18;
#GPIO input = 23;
##
#
# IMPORT NECESSARY CLASSES
#
##
from __future__ import division
import picamera
import serial
import time
import os
import sys
from collections import deque

#
#
# INITIALIZE SERIAL COMMUNICATION WITH ARDUINO FOR REAR RECORDING
#

ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

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
        GPIO.setup(18,GPIO.OUT) #Side Sensor trigger
        GPIO.setup(23,GPIO.IN)  #Side sensor echo
        GPIO.setup(24,GPIO.OUT)   #LED
        GPIO.output(18, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)  #LED
        
        # initial delay to prevent known crashing issue with proximity sensor
        time.sleep(0.3)
        
        # sensor manual says a pulse ength of 10Us will trigger the 
        # sensor to transmit 8 cycles of ultrasonic burst at 40kHz and 
        # wait for the reflected ultrasonic burst to be received
        
        # to get a pulse length of 10Us we need to start the pulse, then
        # wait for 10 microseconds, then stop the pulse. This will 
        # result in the pulse length being 10Us.
	
	#while 1:   #infinite loop for field recording
	for k in range(40):     # loop for field testing

	#
	#  Initialize arrays and variables
	#
		approaching = 0					# initialize that car is not approaching
		avgSideDistArray = [0,0,0,0,0,0,0,0,0,0]  	 #create array with 10 integers for recording side distances
		medianBackDistArray = deque(5*[0],5)  		 #create array limited to max length of 5 elements to store averages returned from Ulstrasonic sensor
		while (approaching == 0):
	##
	#
	#   CODE FOR NEW BACK SENSOR LV EZ-1 (Get serial data from arduino)
	#
	#
	##
			#Get median rear distance from Arduino Serial Input
			medianBackDistance=ser.readline()
			print(medianBackDistance)
			#remove right most element from the array (AKA prepare for shift)
			medianBackDistArray.pop()
			#Shift elements in array from left to right (FIFO)
			medianBackDistArray.appendleft(medianBackDistance)
			print (medianBackDistArray)
			#compare most recent 5 average distance recordings and look for an approaching pattern
			if medianBackDistArray[0] < medianBackDistArray[1] < medianBackDistArray[2] <medianBackDistArray[3] < medianBackDistArray[4]:
				#update that car is approaching so we can exit rear ultrasonic recording loop
				approaching = 1
				#TURN ON LED to signal car is detected
				GPIO.output(24, True)
				# Create string to represent time approaching car was detected
				timestr = time.strftime("%m%d-%H%M%S")
				print timestr

	
	#
	#   CAR IS APPROACHING, TAKE A PHOTO
	#
		# create directory named with approaching car's time
		os.mkdir(timestr)
		# take and save photo as [time of approach].jpg within newly created directory of the time
		camera.capture(timestr + '/' + timestr + '.jpg')
	
	#
	#
	#   Take recordings from side sensor every .5 seconds over 5seconds (estimated time it takes car to pass)
	#
	
		for j in range(10):
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
			avgSideDistance = sum(distRecs)/len(distRecs)
			print (avgSideDistance)
			avgSideDistArray[j] = avgSideDistance
			print (avgSideDistArray)
			#Create text file of complete array data saved as time of approaching car within a folder of the same name
			print >> open('/home/pi/BIOE421_521_final_project/' + timestr + '/' + timestr + '.txt', 'w'), avgSideDistArray
			print >> open('/home/pi/BIOE421_521_final_project/' + timestr + '/' + timestr + '.txt', 'a'), medianBackDistArray
			GPIO.output(24, False) #Turn off LED that was used to signal that car was approaching
			time.sleep(.5)	
		#Add passing time and minimum passing distance to overall data file saved as data.txt which can easily be parsed for statistical analysis
		print >> open('/home/pi/BIOE421_521_final_project/data2.txt', 'a'), timestr + ',' + str(min(avgSideDistArray))		
        GPIO.cleanup()

    else:
        print "Incorrect usonic() function varible."

        
print reading(0)


