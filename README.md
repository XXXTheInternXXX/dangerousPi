# dangerousPi
Scripts to enumerate networks with a Raspberry Pi.

_Run pip install -r requirments.txt for python dependencies_

Edit rc.local to ensure the python script runs at startup
Edit NIC to make sure the ethernet NIC is named as eth0

**To avoid the "NIC" part edit line 28 and change "eth0" to you NIC name**

**_The shell script will install the dependencies and the script (python) should be set to run on the startup of the RaspberryPi._**

The python scripts will automatically enumerate hosts on the network, then notify the user that its done with a blinking green LED,
and lastly it will check for a connection so it can be unplugged safely.


**_Keep in mind you may have to change some configuration in your RaspberryPi, these include changing the NIC to say eth0 and changing the /etc/rc.local file to run script on startup._**

These files are for educational purposes only so don't use these on a network that you do not have consent to scan/enumerate. **The creator will take no responsibility/liability for any damages that may occur to the RaspberryPi or the target network.**

This script will notify the user when the scanning is finished, the GREEN LED (ONBOARD) will start to blink, simulating a heartbeat, telling the user that the scanning is completed. 

Once it is finished unplug the ethernet first, wait 10 seconds, and allow the raspberryPi will automatically shutdown. It can then be safely unplugged and on its way. 

IF YOU ARE FAMILIAR WITH NMAP THESE SCANS CAN TAKE VERY LONG, CURRENTLY THEY ARE SET TO -T2, TO MAKE THESE FASTER CHANGE LINE 88 (-T2) TO -T3, -T4, OR -T5 

**Please keep in mind that a faster scan could flood a network**