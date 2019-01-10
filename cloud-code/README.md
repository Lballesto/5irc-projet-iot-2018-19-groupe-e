# Configuration Passerelle - Cloud

## Envoie de données aléatoires et de la charge CPU du serveur éxécutant le script

- Installer les paquets nécessaire
```
apt-get install python
apt-get install python-pip
pip install requests

```
- Télécharger les fichiers à partir de git :
```
git clone https://github.com/CPELyon/5irc-projet-iot-2018-19-groupe-e.git
```
- Ajuster les valeurs de token et nom de machine à votre compte ubidots (il n'est pas nécessaire de créer le device sur l'interface ubidots, celui-ci sera ajouter automatiquement au premier envoie de données)
```
cd 5irc-projet-iot-2018-19-groupe-e/cloud-code
vim vim upload-to-ubidots.py
 TOKEN = "XXXXXX"  # Put your TOKEN here
 DEVICE_LABEL = "Your_device_name"  # Put your device label here

```
- Executer le script pyhton permettant de contacter ubidots
```
 python upload-to-ubidots.py
```
