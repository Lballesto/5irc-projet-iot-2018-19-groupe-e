# Configuration BeagleBone Black (BBB) en gateway Wifi avec dongle USB netgear WNA 1100

![alt Beaglebone](../images/bbb.jpg)
![alt Beaglebone](../images/USB-WIFI-WNA1100.png)

Etape 1 : Connection de l'interface wifi usb
- Vérifier que le périphérique est reconnu :
- root@beaglebone:/home/debian# lsusb
Bus 001 Device 002: ID 0846:9030 NetGear, Inc. WNA1100 Wireless-N 150 [Atheros AR9271]

-  root@beaglebone:/home/debian# iwconfig
wlan0     IEEE 802.11bgn  Mode:Master  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off

