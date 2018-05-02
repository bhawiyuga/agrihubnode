import httplib
import json
import time

ip_server = "167.99.74.22"
port_server = 8080

def send_data(data):
    conn = httplib.HTTPConnection(ip_server, port=port_server)
    header = {
        "Content-Type" : "application/json",
        "Authorization" : "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVhYzkwN2FhYTBjY2Y3MzdhMmY3OGUxNiIsImV4cCI6MTUyNTg0MTY2NiwibGFiZWwiOiJLaXNrZW5kYSJ9.I4FnEYmobll-nXr-_T1cHqUzy0zoJomHUOOCgLSMq14"
        }
    conn.request("POST", "/sensordatas/", data, header)
    # Baca responsenya
    data = conn.getresponse().read()
    print(data)

utc_time = int(time.time())

data  = {
        "label" : "Kiskenda",
        "sensors" : [
                {
                        "label" : "TEMP",
                        "value" : [
                                [70, utc_time]
                        ]
                }
        ],
        "nodes" : []
}

json_data = json.dumps(data)
send_data(json_data)

