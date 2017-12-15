import pandas as pd
from datetime import datetime as dt
from dateutil import tz

def read_acc(path, side):
    acc_filepath = path + side + '/ACC.csv'

    # read acc file
    print('Start Reading ACC file')
    acc_csv_stream = pd.read_csv(acc_filepath, header=None, names=['x', 'y', 'z'])
    acc_csv_initial_timestamp = dt.utcfromtimestamp(acc_csv_stream.ix[0, 'x'])
    acc_csv_initial_timestamp = acc_csv_initial_timestamp.replace(tzinfo=tz.gettz('UTC'))
    acc_csv_initial_timestamp = acc_csv_initial_timestamp.astimezone(tz.gettz('America/New_York'))
    acc_csv_stream = acc_csv_stream.drop(acc_csv_stream.index[:2])
    index_acc = pd.date_range(start=acc_csv_initial_timestamp, periods=len(acc_csv_stream.index), freq='31250U')
    acc_csv_stream.set_index(index_acc, inplace=True)

    # calculate rolling avg. like Empatica Connect
    diffs_x = pd.rolling_apply(acc_csv_stream['x'], 2, lambda x: x[0] - x[1])
    diffs_y = pd.rolling_apply(acc_csv_stream['y'], 2, lambda x: x[0] - x[1])
    diffs_z = pd.rolling_apply(acc_csv_stream['z'], 2, lambda x: x[0] - x[1])


    maxed = pd.DataFrame([diffs_x, diffs_y, diffs_z]).max
    averaged = pd.rolling_sum(maxed, 1)
    return acc_csv_stream


print read_acc('data/11-18/dylan/','left')