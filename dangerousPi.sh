#!/bin/bash
# Creating a dangerous Raspberry Pi that can be placed on a network and enumerate machines 
# XXXTheInternXXX

echo ""

# Verify as root
if [[ $EUID -ne 0 ]]; then
	echo "This script most be run as root" 1>&2
	exit 1
fi 

echo ""
echo " Dangerous Pi Install"
echo ""
echo " This installer will load a system to enumerate machines "
echo " keep in mind that Debian Raspberry Pi distribution must be "
echo " onto the SD card before continuing. See the README.txt for "
echo " for more information. "
echo ""
echo " [!] Warning: Before proceeding keep in mind this could take a while [!]"
echo " Please do not interupt this process!"
echo ""
echo "Press ENTER to continue, CTRL+C to abort."
read INPUT
echo ""

# Make sure installer files are owned by root
chown -R root:root .

# Update debian packages
echo "[+] Updating base system Debian packages..."
aptitude -y update 
apt dist-upgrade -y
aptitude -y upgrade 
echo "[+] Base system Debian packages updated."

# Install baseline pentesting tools via aptitude 
echo "[+] Installing baseline pentesting tools/dependencies..."
aptitude -y install vim telnet tree btscanner libnet-dns-perl hostapd nmap dsniff netcat nikto xprobe python-scapy wireshark tcpdump
echo "[+] Baseline pentesting tools installed"

# Remove unneeded startup items 
echo "[+] Remove unneeded startup items..."
update-rc.d -f gpsd remove 
update-rc.d -f tinyproxy remove 
update-rc.d -f ntp remove 
apt-get -y purge portmap
apt-get -y autoremove gdm
apt-get -y autoremove
echo "[+] Unneeded startup items removed."

echo ""
#Install more scanning and enumeration tools
echo "Installing dependencies for script"
apt-get update -y
apt-get install python3.6 -y
apt-get install python3-pip -y
wget https://xael.org/norman/python/python-nmap/python-nmap-0.4.1.tar.gz
tar xvzf python-nmap-0.4.1.tar.gz
rm -rf python-nmap-0.4.1.tar.gz
cd python-nmap-0.4.1/
sudo python setup.py install 
cd ../

echo "Installing git"
apt-get install git -y
echo "Git installed"


curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
sudo pip install requests

echo ""

clear

echo "Making sure NIC is set to eth0"
cp /lib/udev/rules.d/73-usb-net-by-mac.rules /lib/udev/rules.d/73-usb-net-by-mac.rules.backup
sed -i 's/$env{ID_NET_NAME_MAC}/eth0/g' /lib/udev/rules.d/73-usb-net-by-mac.rules
echo "Finished, if failed you may have to fix this manually"
echo "A backup is made just in case..."

echo "Two things to remember/change"
echo ""
echo "Make sure that your ethernet NIC is set to eth0"
echo ""
echo "To make sure, nano /lib/udev/rules.d/73-usb-net-by-mac.rules"
read INPUT

echo "Finally edit your /etc/rc.local file so that the script can be run on startup"
echo "" 
echo "On the bottom of the rc.local file put these lines"
echo "cd /path/were/file/is ; python networkEnumeration.py"
read INPUT

echo "Finished Install!"
echo "Enjoy!"

echo "[+] Rebooting now..."

sudo reboot --