import datetime

from RSSI.rssi_utils.dicts import timeslots_less
from RSSI.rssi_utils.influx import InfluxQuery, RSSITimeDict


class SensorUpdater:
    def __init__(self, sensors, day=None):
        self.sensors = sensors
        self.day = day

    def update_time_dicts(self):
        dicts = []
        for sensor in self.sensors:
            print(datetime.datetime.now(), f'start {sensor}')
            tri1 = InfluxQuery().query_rssi('RSSI_slot1', sensor, self.day)
            tri2 = InfluxQuery().query_rssi('RSSI_slot2', sensor, self.day)
            rssi_dict = RSSITimeDict(sensor)
            dicts.append(rssi_dict.update_time_dict(tri1, tri2))
        print(datetime.datetime.now(), 'stop')
        return dicts


def get_sensor(sensor, day=None):
    sensor = [sensor]
    sensor_updater = SensorUpdater(sensor)
    dicts = sensor_updater.update_time_dicts()
    lines, more = timeslots_less(dicts)
    return lines, more
