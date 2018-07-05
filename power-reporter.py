import os

import paho.mqtt.client as mqtt
import requests

from bs4 import BeautifulSoup


def get_power(client, userdata, msg):
    data = requests.post(
        "https://{hostname}/data".format(
            hostname=os.environ.get("DRAC_HOSTNAME")
        ),
        params={
            "get": "powermonitordata"
        },
        headers={
            "ST2": os.environ.get("DRAC_ST2"),
            "Cookie": "_appwebSessionId_={}".format(
                os.environ.get("DRAC_COOKIE_SESSION_ID")
            )
        },
        verify=False
    )

    soup = BeautifulSoup(data.text, 'lxml-xml')
    wattage = int(soup.root.powermonitordata.ipowerWatts1.text)

    print("Submitting {}".format(wattage))
    client.publish(os.environ.get("MQTT_DESTINATION"), wattage)


def on_connect(client, userdata, flags, retcode):
    client.subscribe(os.environ.get("MQTT_TIMESIGNAL", "timesignal/60"))
    print("subscribed")


if __name__ == "__main__":
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = get_power

    mqtt_client.connect(os.environ.get("MQTT_HOSTNAME"))
    print("starting")
    mqtt_client.loop_forever()
