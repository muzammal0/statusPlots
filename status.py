import pandas as pd
import datetime as dt
import pytz
import os
import csv


class status():

    def __init__(self):
        super().__init__()

        self.files = ['events_a', 'events_b', 'events_c', 'events_d', 'events_e']
        self.nodes = ['n1', 'n2', 'n3', 'n4', 'n5']
        self.user = os.getlogin()
        self.active = {"Date": [], "Duration": []}
        self.inactive = {"Date": [], "Duration": []}

    def status(self, file):
        K = pd.read_csv('/home/' + self.user + '/tz_' + file + '.csv')
        start_date = K['Date']
        state = K['State']
        header = ['Date_A', 'Date_B', 'Duration', 'State']
        with open('/home/' + self.user + '/status_' + file + '.csv', 'w+', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            # calculate time difference
            for i in range(len(start_date) - 1):
                df = start_date[i].split('.')[0]
                df2 = start_date[i + 1].split('.')[0]
                datetimeObj = dt.datetime.strptime(df, '%Y-%m-%d %H:%M:%S')
                datetimeObj2 = dt.datetime.strptime(df2, '%Y-%m-%d %H:%M:%S')
                diff = datetimeObj2 - datetimeObj
                # print(diff)
                data = [datetimeObj, datetimeObj2, diff, state[i]]
                writer.writerow(data)
            f.close()

    def tz_adjust(self, file, node):
        K = pd.read_csv('/home/' + self.user + '/' + file + '.csv')
        UTCtime = K['timestamp']
        s_type = K['type']
        devices = K['devices']
        state = K['state']
        header = ['Date', 'Devices', 'State']

        with open('/home/' + self.user + '/tz_' + file + ' ' + node + '.csv', 'a+', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            for i in reversed(range(len(UTCtime) - 1)):
                if s_type[i] == 'DEVICE_STATE':
                    if devices[i] == node:
                        df = UTCtime[i].replace('Z', '')
                        df2 = UTCtime[i + 1].replace('Z', '')
                        datetimeObj = dt.datetime.strptime(df, '%Y-%m-%dT%H:%M:%S.%f')
                        datetimeObj2 = dt.datetime.strptime(df2, '%Y-%m-%dT%H:%M:%S.%f')
                        local_tz = pytz.timezone('Asia/Karachi')
                        local_dt_a = datetimeObj.replace(tzinfo=pytz.utc).astimezone(local_tz)
                        local_dt_b = datetimeObj2.replace(tzinfo=pytz.utc).astimezone(local_tz)
                        # print(datetimeObj)
                        # print(datetimeObj2)
                        # diff = datetimeObj - datetimeObj2
                        # print(local_tz.normalize(local_dt).__format__('%Y-%m-%d'))
                        # print(local_tz.normalize(local_dt).__format__('%H:%M:%S'))
                        data = [local_dt_a, devices[i], state[i]]
                        writer.writerow(data)






if __name__ == "__main__":
    status = status()
    for i in range(len(status.files)):
        for j in range(len(status.nodes)):
            status.tz_adjust(status.files[i], str(status.nodes[j]))
    # status.status(status.files[i])
    # remove duplicates and merge all tz csv
