#!/usr/bin/env python3
################################################################################
# fcpi.py                                                                      #
#                                                                              #
# Record 60 seconds videos to a USB Flash Drive (runtime estimate 0.3h per GB) #
# Delete oldest file when available space is below 10%                         #
################################################################################

import subprocess
import picamera
import shutil
import time
import os

# Function to log process status
def log(text):
	# Get current time as string
	current_time = time.strftime("%Y-%m-%dUTC%Hh%Mm%Ss")
	
	# Write in log file
	try:
		with open("/home/pi/fcpi/log.txt", "a") as logfile:
			logfile.write(current_time)
			logfile.write(" ")
			logfile.write(text)
			logfile.write("\n")
			return 0
	except:
		return 1

# Function to check the USB Flash Drive connection status
def usb_check(device):
	# Check if the devide is connected to the system
	if os.path.exists(device):
		# USB Flash Drive is connected to the system
		
		return 0
	else:
		# USB Flash Drive is not connected to the system
		
		return 1

# Function to free space on the USB Flash Drive according to minimum threshold
def usb_free_space(device, folder, available_space_minimum_threshold_in_percent):
	# Check if the devide is connected to the system
	if not usb_check(device):
		# USB Flash Drive is connected to the system
		
		# Get minimum threshold in bytes
		try:
			available_space_minimum_threshold_in_bytes = shutil.disk_usage(folder).total * available_space_minimum_threshold_in_percent / 100
		except:
			log("[WARN] Error getting minimum threshold in bytes")
			return 1
		
		# Get current available space
		try:
			available_space_in_byte = shutil.disk_usage(folder).free
		except:
			log("[WARN] Error getting current available space")
		
		# Check if available space is lower than minimum threshold
		if(available_space_in_byte < available_space_minimum_threshold_in_bytes):
			# Available space is lower than minimum threshold
			
			# Get list of files sorted in increasing order
			try:
				file_list =  os.listdir(folder)
				file_list.sort()
			except:
				log("[WARN] Error getting list of files sorted in increasing order")
		else:
			# Available space is not lower than minimum threshold
			
			return 0
		
		# Set file iteration count
		i = 0
		
		# Loop while available space is lower than minimum threshold and USB Flash Drive is still connected
		while(available_space_in_byte < available_space_minimum_threshold_in_bytes and not usb_check(device)):
			# Available space is still lower than minimum threshold 
			# USB Flash Drive is still connected

			# Delete file in position i
			try:
				# Get current file
				current_file = folder + file_list[i]
				
				# Delete curent file
				os.remove(current_file)
				
				# Log file delete
				log("[INFO] Oldest file deleted")
			except:
				log("[WARN] Error deleting file")
				raise SystemExit()
			
			
			
			# Increment iteration count
			i = i + 1
			
			# Get new available space
			try:
				available_space_in_byte = shutil.disk_usage(folder).free
			except:
				log("[WARN] Error getting new available space")
		
		# Check if loop exited because available space is no longer lower than minimum threshold or if USB Flash Drive is not connected anymore
		if not usb_check(device):
			# USB Flash Drive is still connected
			# Available space is no longer lower than minimum threshold
			
			return 0
		else:
			# USB Flash Drive is not connected anymore
			
			return 1
	else:
		# USB Flash Drive is not connected to the system
		
		return 1

# Function to mount the USB Flash Drive
def usb_mount(device, folder):
	# Check if the devide is connected to the system
	if not usb_check(device):
		# USB Flash Drive is connected to the system
		
		# Mount USB Flash Drive to folder
		try:
			subprocess.call(["mount", device, folder])
			##mount -o uid=pi,gid=pi /dev/sda1 /media/usb
		except:
			log("[WARN] Error mounting USB Flash Drive to folder")
		
		return 0
	else:
		# USB Flash Drive is not connected to the system
	
		return 1

# Function to unmount the USB Flash Drive	
def usb_unmount(folder):
	# Call umount subprocess
	try:
		subprocess.call(["umount", folder])
	except:
		log("[WARN] Error calling umount subprocess")

# Define parameters (config.txt file in the future)
device = '/dev/sda1'
folder = '/media/usb/'
available_space_minimum_threshold_in_percent = 10
duration_in_seconds = 60
log("[INFO] Parameters set")

# Loop endlessly
while(True):
	# Mount the USB Flash Drive if it is connected
	if not usb_mount(device, folder):
		# The USB Flash Drive is connected
		# The USB Flash Drive was mounted
		log("[INFO] The USB Flash Drive is connected")
		log("[INFO] The USB Flash Drive was mounted")
		
		# Initialize camera_module
		try:
			# Free space on the USB Flash Drive if needed
			usb_free_space(device, folder, available_space_minimum_threshold_in_percent)
			
			with picamera.PiCamera() as camera_module:
				log("[INFO] Camera module initilazed")
				
				# Set camera_module parameters
				camera_module.resolution = (1280, 720)
				log("[INFO] Camera module parameters set")
			
				# Get current time as string
				current_time = time.strftime("%Y-%m-%dUTC%Hh%Mm%Ss")
				
				# Start recording the first video file of the batch
				try:
					camera_module.start_recording('/media/usb/' + current_time + '.h264')
					log("[INFO] Started recording the first video file of the batch")
				except:
					log("[WARN] Error starting recording the first video file of the batch")
					raise SystemExit()
				
				# Loop while the USB Flash Drive is still connected
				while not usb_check(device):
					# The USB Flash Drive is still connected
					
					# Initialize counter to zero
					i = 0
					
					# Loop while the USB Flash Drive is still connected and counter is below 61 seconds
					while not usb_check(device) and i <= duration_in_seconds:
						# The USB Flash Drive is still connected
						# Counter is below 61 seconds
						
						# Wait one second
						try:
							camera_module.wait_recording(1)
							log("[INFO] Waiting one second")
						except:
							log("[WARN] Error waiting one second")
							camera_module.stop_recording()
							log("[INFO] Stopped recording file")
							raise SystemExit()
						
						# Increment counter
						i = i + 1
					
					# Check if loop exited because counter arrived at maximum duration or if the USB Flash Drive is not connected anymore
					if not usb_check(device):
						# The USB Flash Drive is still connected
						# Loop exited because counter arrived at maximum duration
						
						# Get current time as string
						current_time = time.strftime("%Y-%m-%dUTC%Hh%Mm%Ss")
						
						# Split the record file
						try:
							camera_module.split_recording('/media/usb/' + current_time + '.h264')
							log("[INFO] File recording splitted")
						except:
							log("[WARN] Error splitting the record file")
							camera_module.stop_recording()
							log("[INFO] Stopped recording file")
							raise SystemExit()
						
						# Free space on the USB Flash Drive if needed
						usb_free_space(device, folder, available_space_minimum_threshold_in_percent)
		except:
			log("[WARN] Error with camera_module")
		
		# Unmount the USB Flash Drive
		usb_unmount(folder)
		log("[INFO] USB Flash drive unmounted")
	else:
		# USB Flash Drive is not connected
		log("[INFO] USB Flash Drive is not connected")
		
		# Wait one second
		time.sleep(1)
