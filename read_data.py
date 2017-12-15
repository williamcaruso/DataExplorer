# William Caruso MAS.630 Fall 2017
# Affect as a Factor in Precision Performance
# read_files() adapted from code by Szymon Fedor

import pandas as pd
from datetime import datetime as dt
from dateutil import tz
from operator import add
import matplotlib.pyplot as plt


def find_marker_locations(stream, marker_times):

    marker_count = 0
    value_count = 0
    marker_locations = []

    for i in range(len(stream)):
        value = stream.ix[i]
        if marker_times[marker_count] in str(value):
            print("Value found at pos %i", value_count)
            marker_locations.append(value_count)
            marker_count += 1
        if marker_count == len(marker_times) - 1:
            break
        value_count += 1
    print(marker_locations)
    return marker_locations


def read_files (path, side='/left'):
    #identify filepaths
    eda_filepath = path + side +'/EDA.csv'
    acc_filepath = path + side +'/ACC.csv'
    hr_filepath = path + side +'/HR.csv'
    ibi_filepath = path + side +'/IBI.csv' 
    bvp_filepath = path + side +'/BVP.csv'
    tags_filepath = path + side +'/tags.csv'
    temp_filepath = path + side +'/TEMP.csv'
    shots_filepath = path + '/1010.csv'
    # shots
    print('Start Reading Shots file')
    shots_csv_stream = pd.read_csv(shots_filepath, header=None, usecols=[4, 6, 8, 9])
    # with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
    #     print(shots_csv_stream)
        

    #read eda file
    print('Start Reading EDA file')
    eda_csv_stream = pd.read_csv(eda_filepath, header=None, names=['eda'])
    eda_csv_initial_timestamp = dt.utcfromtimestamp(eda_csv_stream.ix[0, 'eda'])
    eda_csv_initial_timestamp = eda_csv_initial_timestamp.replace(tzinfo=tz.gettz('UTC'))
    eda_csv_initial_timestamp = eda_csv_initial_timestamp.astimezone(tz.gettz('America/New_York'))
    eda_csv_stream = eda_csv_stream.drop(eda_csv_stream.index[:2])
    # add index
    index_eda_1 = pd.date_range(start=eda_csv_initial_timestamp, periods=len(eda_csv_stream.index), freq='250L')
    eda_csv_stream.set_index(index_eda_1, inplace=True)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
    #     print(eda_csv_stream)

    # /////////////////////////////////////////////////////////////////
    # plot eda and shot markers
    shot_times = shots_csv_stream[shots_csv_stream.columns[1]].tolist()
    markers = [16196, 16456, 16644, 16756, 17168, 17340, 17440, 17520, 17612, 17720, 17812, 17920, 18012, 18148, 18260, 18352, 18456, 18548, 18640, 18848, 18940, 19028, 19116, 19212, 19396, 19480, 19576, 19684, 19796, 19908, 20016, 20104, 20228, 20564, 20676, 20808, 20940, 21044, 21136, 21240, 21548, 21668, 21756, 21860, 21952, 22040, 22804, 22884, 22968, 23056, 23140, 23276, 23368, 23432, 23500, 23568, 23656, 23744, 23824]#find_marker_locations(eda_csv_stream, shot_times)
    ax = eda_csv_stream.plot(markevery=markers, marker='o', markerfacecolor='black')
    # /////////////////////////////////////////////////////////////////


    # read acc file
    print('Start Reading ACC file')
    acc_csv_stream = pd.read_csv(acc_filepath, header=None, names=['x', 'y', 'z'])
    acc_csv_initial_timestamp = dt.utcfromtimestamp(acc_csv_stream.ix[0, 'x'])
    acc_csv_initial_timestamp = acc_csv_initial_timestamp.replace(tzinfo=tz.gettz('UTC'))
    acc_csv_initial_timestamp = acc_csv_initial_timestamp.astimezone(tz.gettz('America/New_York'))
    acc_csv_stream = acc_csv_stream.drop(acc_csv_stream.index[:2])
    index_acc = pd.date_range(start=acc_csv_initial_timestamp, periods=len(acc_csv_stream.index), freq='31250U')
    acc_csv_stream.set_index(index_acc, inplace=True)
    # acc_csv_stream.plot()
    # read ibi file
    print('Start Reading IBI file')
    ibi_csv_stream = pd.read_csv(ibi_filepath, header=None, names=['time_elapsed', 'ibi'])
    ibi_csv_initial_timestamp = dt.utcfromtimestamp(ibi_csv_stream.ix[0, 'time_elapsed'])
    ibi_csv_initial_timestamp = ibi_csv_initial_timestamp.replace(tzinfo=tz.gettz('UTC'))
    ibi_csv_initial_timestamp = ibi_csv_initial_timestamp.astimezone(tz.gettz('America/New_York'))
    ibi_csv_stream = ibi_csv_stream.drop(ibi_csv_stream.index[0])
    # add timestamps
    index_ibi = pd.to_timedelta(ibi_csv_stream.ix[:, 'time_elapsed'], unit='s')
    ibi_csv_initial_timestamp = pd.Timestamp(ibi_csv_initial_timestamp)
    # index_ibi = pd.TimedeltaIndex(index_ibi) + pd.DatetimeIndex([csv_initial_timestamp] * len(index_ibi))
    index_ibi = map(add, index_ibi, [ibi_csv_initial_timestamp] * len(index_ibi))
    se_ibi = pd.Series(data=ibi_csv_stream.ix[:, 'ibi'].values, index=index_ibi)
    se_ibi = se_ibi.convert_objects(convert_numeric=True)
    print('Start reading TEMP file')
    temp_csv_stream = pd.read_csv(temp_filepath, header=None, names=['temp'])
    temp_csv_initial_timestamp = dt.utcfromtimestamp(temp_csv_stream.ix[0, 'temp'])
    temp_csv_initial_timestamp = temp_csv_initial_timestamp.replace(tzinfo=tz.gettz('UTC'))
    temp_csv_initial_timestamp = temp_csv_initial_timestamp.astimezone(tz.gettz('America/New_York'))
    temp_csv_stream = temp_csv_stream.drop(temp_csv_stream.index[:2])
    # temp_csv_stream.plot()
    # add index
    index_temp = pd.date_range(start=temp_csv_initial_timestamp, periods=len(temp_csv_stream.index),
                               freq='250L')
    temp_csv_stream.set_index(index_temp, inplace=True)
    print('Start reading HR file')
    hr_csv_stream = pd.read_csv(hr_filepath, header=None, names=['hr'])
    hr_csv_initial_timestamp = dt.utcfromtimestamp(hr_csv_stream.ix[0, 'hr'])
    hr_csv_initial_timestamp = hr_csv_initial_timestamp.replace(tzinfo=tz.gettz('UTC'))
    hr_csv_initial_timestamp = hr_csv_initial_timestamp.astimezone(tz.gettz('America/New_York'))
    hr_csv_stream = hr_csv_stream.drop(hr_csv_stream.index[:2])
    # hr_csv_stream.plot()
    # add index
    index_hr = pd.date_range(start=hr_csv_initial_timestamp, periods=len(hr_csv_stream.index),
                         freq='1S')
    hr_csv_stream.set_index(index_hr, inplace=True)
    print('Start Reading tags file')
    tags_csv_stream = pd.read_csv(tags_filepath, header=None, names=['tag'])
    tags_csv_stream_as_datetime = pd.Series(
            index=pd.to_datetime(tags_csv_stream['tag'], unit='s'),
            data=[0] * len(tags_csv_stream['tag']))
    tags_csv_stream_as_datetime.index = tags_csv_stream_as_datetime.index.tz_localize(
            'UTC').tz_convert('America/New_York')
    # tags_csv_stream_as_datetime.plot()

 
    plt.show()


path = 'data/11-18/dylan'
read_files(path)