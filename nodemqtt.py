import httplib
import json
import paho.mqtt.client as mqtt
import time

server_ip = '167.99.74.22'
server_port = 8080


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVhYzkwN2FhYTBjY2Y3MzdhMmY3OGUxNiIsImV4cCI6MTUyNTg0ODM4NywibGFiZWwiOiJBZ3Jpbm9kZSJ9.ckfrhbQagNAIb0G2et3cPeT13GmSF_GLZBKadb_Mly8"
mqtt_broker_ip = "127.0.0.1"
mqtt_broker_port = 1883



mqttc = mqtt.Client("server", clean_session=False)
mqttc.connect(mqtt_broker_ip, mqtt_broker_port)

headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT "+token
}

def generate_message(payload):
    data = json.loads(payload)
    timestamp = int(data["timestamp"])
    temp = float(data["temperature"]["value"])
    humidity = float(data["humidity"]["value"].replace(" %",""))
    rain = int(data["rain"]["value"])
    light = int(data["light"]["value"])
    soil = int(data["soil"]["value"])
    post_data = {
        "label" : "Agrinode",
        "sensors" : [
                {
                    "label" : "TEMP",
                    "value" : [
                            [temp, timestamp]
                    ]
                },
                {
                    "label" : "HUMID",
                    "value" : [
                            [humidity, timestamp]
                    ]
                },
                {
                    "label" : "RAIN",
                    "value" : [
                            [rain, timestamp]
                    ]
                },
                {
                    "label" : "LIGHT",
                    "value" : [
                            [light, timestamp]
                    ]
                },
                {
                    "label" : "SOIL",
                    "value" : [
                            [soil, timestamp]
                    ]
                }
        ],
        "nodes" : []
    }
    str_json = json.dumps(post_data)
    return str_json

def send_http(str_json):
    conn = httplib.HTTPConnection(server_ip, server_port)
    conn.request("POST", "/sensordatas/", str_json, headers)
    response = conn.getresponse()
    print response.status, response.reason

def on_message(mqttc,obj,msg):
    str_json = generate_message(msg.payload)
    print str_json
    send_http(str_json)
    
#print str_json

mqttc.on_message = on_message
mqttc.subscribe("/temperature")
mqttc.loop_forever()



'''
# Contoh hardcode
sample_json = '{"topic": "sensor/agrinode", "protocol": "mqtt", "temperature": {"unit": "celcius", "value": "22.0"}, "light": {"unit": "boolean", "value": "1"}, "timestamp": 1525242360.136197, "soil": {"unit": "boolean", "value": "0"}, "sensor": {"index": "comqtt", "tipe": "6lowpan", "module": "agri", "ip": "fe80::c030:955d:d2b7:aaf0"}, "rain": {"unit": "boolean", "value": "0"}, "humidity": {"unit": "%", "value": "38.0 %"}}'

json_data = generate_message(sample_json)

print(json_data)

send_http(json_data)
'''