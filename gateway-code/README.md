# Configuration BeagleBone Black (BBB) en gateway Wifi avec dongle USB netgear WNA 1100

![alt Beaglebone](../images/bbb.jpg)
![alt Dongle USB WIFI](../images/USB-WIFI-WNA1100.png)

## Etape 1 : Connection de l'interface wifi usb
- Vérifier que le périphérique est reconnu :
```
#root@beaglebone:~# lsusb
Bus 001 Device 002: ID 0846:9030 NetGear, Inc. WNA1100 Wireless-N 150 [Atheros AR9271]

#root@beaglebone:~# iwconfig
wlan0     IEEE 802.11bgn  Mode:Master  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```
## Etape 2 : Configuration des interfaces réseaux :
- Editer le fichier /etc/network/interfaces comme suit :
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
- Redémarrer le service réseau :
```
root@beaglebone:~# /etc/init.d/networking restart
[ ok ] Restarting networking (via systemctl): networking.service.
```

## Etape 3 : Configuration du point d'accès wifi :
- Installer le paquet hostapd :
```
apt-get install hostapd
```
- Editer le fichier /etc/default/hostapd :
```
vim /etc/default/hostapd
```
- Modifier la directive comme suit :
```
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```
- Créer le fichier /etc/hostapd/hostapd.conf :
```
vim /etc/hostapd/hostapd.conf
```
- Ajouter les lignes suivantes en adaptant les paramètres "SSID" et "wpa_passphrase" :
```
### Wireless network name ###
interface=wlan0
#
### Set your bridge name ###
#bridge=br0

#driver
driver=nl80211

country_code=HU

ssid=NOM_SSID

channel=7

hw_mode=g

# # Static WPA2 key configuration
# #1=wpa1, 2=wpa2, 3=both
wpa=2

wpa_passphrase=your_password

## Key management algorithms ##
wpa_key_mgmt=WPA-PSK
#
## Set cipher suites (encryption algorithms) ##
## TKIP = Temporal Key Integrity Protocol
## CCMP = AES in Counter mode with CBC-MAC
wpa_pairwise=TKIP
#rsn_pairwise=CCMP
#
## Shared Key Authentication ##
auth_algs=1
## Accept all MAC address ###
macaddr_acl=0
#enables/disables broadcasting the ssid
ignore_broadcast_ssid=0
# Needed for Windows clients
eapol_key_index_workaround=0

```
## Etape 4 : Démarrer le point d'accès wifi :
- Vérifier si le process "wpa_supplicant" tourne :
```
root@beaglebone:~# ps -aux | grep wpa
root       900  0.0  0.8   5584  4288 ?        Ss   08:45   0:00 /sbin/wpa_supplicant -u -s -O /run/wpa_supplicant
```
- Si le service tourne le kill avec son numéro de process (ici 900)
```
root@beaglebone:~# kill -9 900
```
- Démarrer hostapd :
```
root@beaglebone:~# hostapd /etc/hostapd/hostapd.conf
Configuration file: /etc/hostapd/hostapd.conf
wlan0: interface state UNINITIALIZED->COUNTRY_UPDATE
Using interface wlan0 with hwaddr XX:XX:XX:XX:XX:XX and ssid "NOM_SSID"
wlan0: interface state COUNTRY_UPDATE->ENABLED
wlan0: AP-ENABLED
```
## Etape 5 : Mise en place d'un serveur DHCP :
- Installer les paquets DHCP server :
```
apt-get update
apt-get install isc-dhcp-server
```
- Editer le fichier /etc/dhcp/dhcpd.conf :
```
vim /etc/dhcp/dhcpd.conf
```
- ajouter les lignes suivantes correspondant à votre plan IP
```
subnet 192.168.4.0 netmask 255.255.255.0 {
  range 192.168.4.10 192.168.4.100;
  option domain-name-servers 1.1.1.1;
  option routers 192.168.4.1;
}
```
- Redémarrer le service DHCP server :
```
/etc/init.d/isc-dhcp-server restart
```
- Vous dever maintenant pouvoir vous connecter au wifi et obtenir une ip via dhcp.

## Etape 6 : Configuration du routage et du NAT permettant l'accès à internet
Afin que les utilisateurs wifi puissent accéder à internet nous allons router leur paquets vers l'interface eth0 qui accéde à internet

- Activer le forwarding :
- Editer le fichier /etc/sysctl.conf en modifiant en dé-commantant la ligne suivante :
```
net.ipv4.ip_forward=1
```
- Prise en compte de la modification :
```
sysctl -p
```
- Ajout des règles de forwarding et de NAT via iptables :
```
iptables -A FORWARD -o eth0 -j ACCEPT
iptables -A FORWARD -i eth0 -j ACCEPT
iptables -A FORWARD -i wlan0 -j ACCEPT
iptables -A FORWARD -o wlan0 -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```
- Sauvegarder la conf iptables :
```
iptables-save > /etc/iptables.save
```
- Décommenter la ligne suivante dans le fichier /etc/network/interfaces
```
post-up iptables-restore < /etc/iptables.save
```
- Vérifier la configuration iptables en place :
```
root@beaglebone:~# iptables -L -t nat
Chain PREROUTING (policy ACCEPT)
target     prot opt source               destination

Chain INPUT (policy ACCEPT)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination

Chain POSTROUTING (policy ACCEPT)
target     prot opt source               destination
MASQUERADE  all  --  anywhere             anywhere

```

