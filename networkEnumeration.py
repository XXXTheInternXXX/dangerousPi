# A script to do local network assest scanning and enumeration
# This is intended to be for wired networks not wireless
import os
import sys
import time
import socket
import subprocess
import requests
import datetime

os.system('echo mmc0 > /sys/class/leds/led0/trigger')

#Setting datetime to work for files and to keep (logs)
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%m-%d-%Y-%H:%M:%S')

# Setting up empty arrays for variables that will be used
raspIP       = []
raspMask     = []
targetSubnet = []

#Every possible netmask 
netmasks     = ['255.255.255.252', '255.255.255.248', '255.255.255.240','255.255.255.224','255.255.255.192','255.255.255.128','255.255.255.0','255.255.254.0','255.255.252.0','255.255.248.0','255.255.240.0','255.255.224.0','255.255.192.0','255.255.128.0','255.255.0.0']

#Every possible CIDR notation
cidrNotation = ['/30', '/29', '/28', '/27', '/26', '/25', '/24', '/23', '/22', '/21', '/20', '/19', '/18', '/17', '/16']

# Special commands to run during this script
cmd     = """ifconfig eth0 | grep netmask | awk \'/netmask/ {print $4;}\'"""
grepCmd = """grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'"""

# Check for a key press on startup so user can access files
def doIStart():
	try:
		print ("[+] You have 20 seconds to stop the script...")
		time.sleep(20)
		pass
	except KeyboardInterrupt:
		print ('[*] Script stopped')
		exit()

# Check if RaspberryPi can ping out if it can script will start, if not it will restart the script
def getInternet():
	try: 
		ping_response = os.system("ping -c 7 -W 3 8.8.8.8")
		if ping_response == 0:
			print ("[+] Connection received, good to go")
			pass
		else: 
			#Connection failed 
			print ("[-] Network connection failed...")
			print ("[-] Sleeping for 5 seconds before restarting...")
			time.sleep(5)
			print ("[!!!] RESTARTING [!!!]")
			python = sys.executable
			os.execl(python, python, * sys.argv)
	except Exception as e:
		print ('[*] An error occurred ' + str(e)) 

# ping google again and get the IP address for NIC eth0
def getIP():
	#Get the IP address of the nic conencted to the internet
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	raspIP.append(s.getsockname()[0])
	s.close()

# Finding the network mask that was given to the pi and helps for the NMAP scans
def getNetMask(): 
	#Getting the network mask so the subnet can be identified
	raspMaskResult = (subprocess.check_output(cmd, shell=True))
	raspMask.append(raspMaskResult.rstrip())

# Find if the netmask matches the indexes and then find the corresponding CIDR notation
def getSubnet():
	findNetmasks = netmasks.index((raspMask[0]))
	if findNetmasks > -1:
		correctNotation = cidrNotation[findNetmasks]
		targetSubnet.append(correctNotation)
	else:
		print("[!] ERROR: Subnet not found in list...")
		print ("[-] Sleeping for 5 seconds before restarting...")
		time.sleep(5)
		print ("[!!!] RESTARTING [!!!]")
		python = sys.executable
		os.execl(python, python, * sys.argv)	

# Run a ping sweep and find hosts and then single out the hosts into a file
def findMachines():
	os.system('nmap -sP {0}{1} -oG HostStatus'.format(raspIP[0], targetSubnet[0]))
	os.system('cat HostStatus | {0} >> UpHosts'.format(grepCmd))
	print ("[+] Machines found! Targets put into \"UpHosts\" file...")

# Find out very important details about machines 
# Service version, all ports, operating system, sneaky, slow
def versionDetection():
	os.system('nmap -p 1-65535 -sV -T2 -O -sS -Pn -iL UpHosts -oN {0}versionDetection'.format(st))
	print ("Discovery finished, notifying user...")
	print ("[+] The finished scan is in the \"versionDetection\" file...")

# Notify the user that the Pi is done with the scan
def scanFinishAlert(): 
	# Since this is the raspberry pi we will flash the onboard LED. 
	print ("[!!!] THE GREEN LED WILL BLINK, THE SCANS ARE FINISHED [!!!]")
	os.system('modprobe ledtrig_heartbeat')
	os.system('echo heartbeat > /sys/class/leds/led0/trigger')

# Unplug the ethernet first wait for 10 seconds and the Pi will shutdown
def safeShutdown():
	while 1 == 1:
		try:
			response = requests.get("https://www.google.com/")
			if str(response) == "<Response [200]>":
					print ("[+] Still connected... Waiting for unplug...")
					time.sleep(10)
		except requests.exceptions.ConnectionError:
			try: 
				print ('[+] Network Unplugged...')
				print ('[+] Shutdown...')
				os.system('echo mmc0 > /sys/class/leds/led0/trigger')
				os.system('shutdown -h now')
			except KeyboardInterrupt: 
				print ('[+] Keyboard Interrupt, the script will stop')
				os.system('echo mmc0 > /sys/class/leds/led0/trigger')
				exit()

# Order of operations
doIStart()		
getInternet()
getIP()
getNetMask()
getSubnet()
findMachines()
versionDetection()
scanFinishAlert()
safeShutdown()