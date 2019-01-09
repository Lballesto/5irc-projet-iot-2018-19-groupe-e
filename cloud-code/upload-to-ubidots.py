import time
import requests
import math
import random

TOKEN = "BBFF-lQwKrCh8JOWwESdNZ3vet5oQP75uWI"  # Put your TOKEN here
DEVICE_LABEL = "random_value"  # Put your device label here 
VARIABLE_LABEL_1 = "temperature"  # Put your first variable label here
VARIABLE_LABEL_2 = "humidity"  # Put your second variable label here
VARIABLE_LABEL_3 = "position"  # Put your second variable label here
VARIABLE_LABEL_4 = "LOAD" 

def build_payload(variable_1, variable_2, variable_3, variable_4):
    # Creates two random values for sending data
    value_1 = random.randint(-10, 50)
    value_2 = random.randint(0, 85)
    #value_4 = ('$(cat /proc/loadavg)'.split()[0]) 
    value_4 = format(float(open("/proc/loadavg").readline().split()[0])  *100)
    
    print(value_4)

    # Creates a random gps coordinates
    lat = random.randrange(34, 36, 1) + \
    random.randrange(1, 1000, 1) / 1000.0
    lng = random.randrange(-83, -87, -1) + \
    random.randrange(1, 1000, 1) / 1000.0
    payload = {variable_1: value_1,
        variable_2: value_2,
        variable_3: {"value": 1, "context": {"lat": lat, "lng": lng}},
        variable_4: value_4
        }

    return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")

        return False

    print("[INFO] request made properly, your device is updated")
    return True

def main():
    payload = build_payload(
            VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3, VARIABLE_LABEL_4 )
    
    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")
    time.sleep(30)


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
