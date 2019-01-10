# Configuration BeagleBone Black (BBB) en gateway Wifi avec dongle USB netgear WNA 1100

![alt Beaglebone](../images/bbb.jpg)
![alt Dongle USB WIFI](../images/USB-WIFI-WNA1100.png)

## Etape 1 : Connection de l'interface wifi usb
- Vérifier que le périphérique est reconnu :
```root@beaglebone:/home/debian# lsusb
Bus 001 Device 002: ID 0846:9030 NetGear, Inc. WNA1100 Wireless-N 150 [Atheros AR9271]

-  root@beaglebone:/home/debian# iwconfig
wlan0     IEEE 802.11bgn  Mode:Master  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```
## Etape 2 : Configuration des interfaces réseaux :
- vim /etc/network/interfaces :
```
auto lo
iface lo inet loopback

auto eth0
iface usb0 inet static
    address 192.168.7.2
    netmask 255.255.255.252
    network 192.168.7.0
    gateway 192.168.7.1

iface eth0 inet static
    address 192.168.100.2
    netmask 255.255.255.0
    network 192.168.100.0
    gateway 192.168.100.1
# post-up iptables-restore < /etc/iptables.save # (1)

auto wlan0
iface wlan0 inet static
        address 192.168.4.1
        network 192.168.4.0
        netmask 255.255.255.0
        broadcast 192.168.4.255
#       hostapd /etc/hostapd/hostapd.conf
```
