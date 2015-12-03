# BIOE421_521_final_project
#Team 06 Mary Natoli and Charles Sebesta
#Draft Title: Ultrasonic Determination of Passing Distance Between Vehicles and Bicycles

#Brainstorm:

#Rough Description: 
 - 	The goal of this project is to incorporate a sensing system onto an
		 Arduino/Raspberry Pi platform that will measure the distance between a bicycle and a passing vehicle. 
 - 	We plan to operate the system portably using a battery pack (a portable
		 charger with USB input), so that it can be mounted on a bicycle. 
 - 	For the sensing mechanism, we will use two ultrasonic range finders.
		 One will be mounted to the rear to indicate to the system when a vehicle is approaching.
		 This will trigger the collection of data from the lateral ultrasonic reader which will
		 be mounted on the side of the bicycle to measure lateral distance between the bicycle and passing objects. 
 - 	The Raspberry Pi camera will also be used to acquire video from the rear of the
		 bicycle to verify and collect data on the type of vehicle passing.
 - 	The data obtained from this system could be used to study factors that may cause drivers
		 to pass closer or give more room to cyclists (i.e. road size, time of day, road type,
		 helmet wearing), or to consider a safe passing law in Texas. Texas is currently one of
		 17 states that has no safe passing law.

In order to implement this device, one would purchase the components listed in Table 1. The user would connect the LV-EZ1 rangefinder to an Arduino Uno and connect the Aruino Uno, Raspberry Pi camera and HC-SR04 proximity sensor to a Raspberry Pi. The HC-SR04 should be connected to the Raspberry Pi according to directions found online (http://www.bytecreation.com/blog/2013/10/13/raspberry-pi-ultrasonic-sensor-hc-sr04 ) and the LV EZ-1 would be connected to the Arduino Uno according to directions found online (http://www.maxbotix.com/Ultrasonic_Sensors/MB1013.htm ) from the manufacturer. Source code for our project can be found here: https://github.com/mnatoli/BIOE421_521_final_project
For the system to be fully portable, one would laser cut an acrylic box using the Autocad file available from the authors, and run the code upon powering the system. To run the source code upon Raspberry Pi bootup, one would modify their "sudo crontab" file with the following commands:

@reboot sleep 30; cd [insert project directory]; python project code.py

This will effectively start the program 30 seconds after the raspberry pi finished booting up. The user will still be able to control the Raspberry Pi if connected to a keyboard and monitor, as the program will run in the background. The program will continue to run until the user disables the crontab command and reboots the system.
