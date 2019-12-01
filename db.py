from influxdb import InfluxDBClient
import pandas as pd
import json, os, glob

client = InfluxDBClient(port=8086, database='initial_db')


print("returns version of Influxdb",client.ping())



print("list of databases",client.get_list_database())


print("list of measurements",client.get_list_measurements())



def write_points():
    json_body = [
        {
            "measurement": "temprature",  # defining measurment 
            "tags": {
                "Location": "East-region",  
            },
            "fields": {
                "values": 25,
                "server":10
            },
        }
    ]
    client.write_points(json_body, database="initial_db")
    

write_points()


rs = client.query("SELECT * from temprature", database="initial_db")


points = list(rs.get_points(measurement='temprature'))

print(points)


def write_to_csv_file():

    for i in rs:
        for j in i:
            file = [f for f in glob.glob("temp.csv")]
            if file:
                df = pd.DataFrame.from_dict(j,orient='index').transpose()
                # df = df.fillna(method='ffill')
            
                df.to_csv("temp.csv", mode="a",header=False)
            else:
                df = pd.DataFrame.from_dict(j,orient='index').transpose()
                # df = df.fillna(method='ffill')
            
                df.to_csv("temp.csv", mode="w")

write_to_csv_file()
