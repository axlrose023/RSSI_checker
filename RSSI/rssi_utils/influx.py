from datetime import datetime, timedelta

from dotenv import load_dotenv
import os
from influxdb_client import InfluxDBClient

load_dotenv()


#
# class InfluxQuery:
#     token = os.getenv("INFLUXDB_TOKEN")
#     org = "dtd"
#     url = "https://us-west-2-1.aws.cloud2.influxdata.com/api/v2"
#     bucket = 'repeater-monitor'
#     client = InfluxDBClient(url="http://10.88.99.100:8086", token=token, org=org)
#     query_api = client.query_api()
#
#     def query_rssi(self, measurement, host, date: str = None):
#         now = datetime.now()
#         date_string = now.strftime("%Y-%m-%d")
#         if date:
#             date_string = now.strftime("%Y-%m")
#             date_string = date_string + '-' + date
#
#         query = f"""from(bucket: "repeater-monitor")
#             |> range(start:{date_string}T00:00:00Z, stop:{date_string}T23:59:59Z)
#             |> filter(fn: (r) => r._measurement == "{measurement}" and r.host == "{host}")
#             """
#
#         records = []
#         tables = self.query_api.query(query, org=self.org)
#         for table in tables:
#             for record in table.records:
#                 records.append({'host': record['host'], 'time': record['_time'], 'value': record['_value']})
#         return records

class InfluxQuery:
    token = os.getenv("INFLUXDB_TOKEN")
    org = "dtd"
    url = "https://us-west-2-1.aws.cloud2.influxdata.com/api/v2"
    bucket = 'repeater-monitor'
    client = InfluxDBClient(url="http://10.88.99.100:8086", token=token, org=org)
    query_api = client.query_api()

    def query_rssi(self, measurement, host, date: str = None):
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d")
        if date:
            date_string = now.strftime("%Y-%m")
            date_string = date_string + '-' + date

        # Adjust timezone offset
        timezone_offset = timedelta(hours=3)
        start_time = datetime.strptime(f"{date_string}T00:00:00", "%Y-%m-%dT%H:%M:%S") - timezone_offset
        end_time = datetime.strptime(f"{date_string}T23:59:59", "%Y-%m-%dT%H:%M:%S") - timezone_offset
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        print(start_time_str)
        print(end_time_str)
        query = f"""from(bucket: "repeater-monitor")
            |> range(start: {start_time_str}, stop: {end_time_str})
            |> filter(fn: (r) => r._measurement == "{measurement}" and r.host == "{host}")
            """

        records = []
        tables = self.query_api.query(query, org=self.org)
        for table in tables:
            for record in table.records:
                records.append({'host': record['host'], 'time': record['_time'], 'value': record['_value']})
        return records


class RSSITimeDict:
    def __init__(self, host):
        self.host = host
        self.time_dict = {'host': self.host}
        for hour in range(24):
            hour_plus = (hour + 1) % 24
            if hour == 23:
                hour_range = '23-00'
            else:
                hour_range = f"{hour:02d}-{hour_plus:02d}"
            self.time_dict[hour_range] = {'timeslot1<timeslot2': 0, 'timeslot1>timeslot2': 0}

    def update_time_dict(self, first_query_records, second_query_records):
        for i in range(len(first_query_records)):
            hour_range = self.return_hour_range(date_string=str(first_query_records[i]['time']))
            self.compare_values(value1=first_query_records[i]['value'], value2=second_query_records[i]['value'],
                                hour_range=hour_range)
        self.time_dict = self.return_notime_slots(self.time_dict, keys=list(self.time_dict.keys()))
        return self.time_dict

    def compare_values(self, value1, value2, hour_range):
        if value1 < value2 and abs(
                value1 - value2) > 10:
            self.time_dict[hour_range]['timeslot1<timeslot2'] += 3
        elif value1 > value2 and abs(
                value1 - value2) > 10:
            self.time_dict[hour_range]['timeslot1>timeslot2'] += 3

    def return_notime_slots(self, time_dict, keys):
        logo_range_index = keys.index(self.return_logo_range())
        for key in keys[logo_range_index:]:
            time_dict[key]['timeslot1<timeslot2'] = '-'
            time_dict[key]['timeslot1>timeslot2'] = '-'
        return time_dict

    def return_hour_range(self, date_string):
        date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S%z')
        hour = date_obj.strftime('%H')
        hour = (int(hour) + 3) % 24
        hour_plus = (int(hour) + 1) % 24
        hour_range = f"{hour:02d}-{hour_plus:02d}"
        return hour_range

    def return_logo_range(self):
        now = datetime.now()
        hour_logo = now.strftime("%H")
        hour_pluslogo = int(hour_logo) + 1
        logo_range = str(hour_pluslogo) + '-' + str(int(hour_pluslogo) + 1)
        return logo_range


import openpyxl


def convert_value(value):
    if isinstance(value, str) and len(value) > 32767:
        # Trim long strings to fit Excel's string length limit
        value = value[:32767]
    elif isinstance(value, float):
        # Round floating-point numbers to a specific precision
        value = round(value, 2)
    return value


def make_excel(data):
    try:
        workbook = openpyxl.load_workbook("data.xlsx")
    except FileNotFoundError:
        workbook = openpyxl.Workbook()

    sheet = workbook.active

    if sheet["A1"].value is None:
        sheet["A1"] = "Host"
        sheet["B1"] = "Date"
        sheet["C1"] = "Time"
        sheet["D1"] = "Value"
        sheet["E1"] = "Value2"

    # Append rows to the worksheet
    for row in data:
        converted_row = [convert_value(value) for value in row]
        time_index = 2  # Index of the 'Time' column
        time_value = converted_row[time_index]
        time_value = datetime.strptime(time_value, "%H:%M:%S")
        time_value += timedelta(hours=3)
        converted_row[time_index] = time_value.strftime("%H:%M:%S")
        sheet.append(converted_row)

    workbook.save("data.xlsx")


def hoster(port):
    host = InfluxQuery()
    rssi_data = host.query_rssi('RSSI_slot1', port)
    rssi_data2 = host.query_rssi('RSSI_slot2', port)
    formatted_data = [
        (
            line['host'],
            line['time'].strftime('%Y-%m-%d'),
            line['time'].strftime("%H:%M:%S"),
            line['value']
        )
        for line in rssi_data
    ]
    formatted_data2 = [
        (
            line['host'],
            line['time'].strftime('%Y-%m-%d'),
            line['time'].strftime("%H:%M:%S"),
            line['value']
        )
        for line in rssi_data2
    ]

    data_to_write = [
        (host, date, time, value, value2)
        for ((host, date, time, value), (_, _, _, value2)) in zip(formatted_data, formatted_data2)
    ]

    make_excel(data_to_write)
